from ocrdgen.manager.font import FontManager
from ocrdgen.manager.background import BgManager
from pathlib import Path
import numpy as np
from PIL import ImageDraw, Image
from ocrdgen.ops import boxes_ops
import cv2 as cv
from collections import OrderedDict
from .word import DrawWord


class DrawText:
    def __init__(self, image: np.ndarray, font, text, label,  x, y, index=0, linking=[], delimiter=" ", image_mode="RGBA", color=(0,0,0)):
        self.image = image.copy()
        self.font = font
        self.text = text
        self.label = label
        self.index = index
        self.linking = linking
        self.x = x
        self.y = y
        self.color = color
        self.image_mode = image_mode
        self.delimiter = delimiter
        self.idraw = ImageDraw.Draw(self.image)
        
    def image_size(self):
        h,w = np.array(self.image).shape[:2]
        return w,h
        
    def textsize(self):
        w, h = self.idraw.textsize(self.text, self.font)
        return w,h
    
    def position(self):
        iw, ih = self.image_size()
        tw, th = self.textsize()
        w, h = (iw - tw) / 2, (ih - th) / 2
        return w,h
    
    def delimiter_size(self):
        w, h = self.idraw.textsize(self.delimiter, self.font)
        return w,h
    
    def _clean_split_text(self, text):
        cleaned_text = []
        text_split = text.split(self.delimiter)
        for txt in text_split:
            txt = txt.strip()
            if len(txt)>0:
                cleaned_text.append(txt)
        text_split = cleaned_text
        return text_split
    
    def _build_draw_word(self, word, x,y):
        return DrawWord(image=self.image, font=self.font, 
                        text=word, x=x,y=y, 
                        image_mode=self.image_mode, 
                        color=self.color)
    
    def draw(self, debug_draw=False):
        words_data, image = self.draw_words(debug_draw=debug_draw)
        data = OrderedDict({
            "text": self.text, 
            "bbox": self.bbox(), 
            "linking": self.linking, 
            "words": words_data,
            "id": self.index
        })
        
        return data, image
        
    
    def draw_words(self, debug_draw=False):
        text_list = self._clean_split_text(self.text)
        
        dw, dh = self.delimiter_size()
        x, y = self.x, self.y
        
        data = []
        for idx, txt in enumerate(text_list):
            dword = self._build_draw_word(txt, x=x, y=y)
            tw, th = dword.textsize()
            self.image = dword.draw(debug_draw=debug_draw)
            bbox = dword.bbox()
            char_bbox, _ = dword.char_bbox(debug_draw=debug_draw)
            odt = OrderedDict({"word":txt, "bbox":bbox, "chars":char_bbox, "sequence_idx": idx })
            data.append(odt)
            
            x = x + tw + dw
            
            
        return data, self.image 
    
    
    def bbox(self):
        xymm = self.xymm_bbox()
        xywh = boxes_ops.xymm_to_xywh(xymm)
        return xywh
    
    def xymm_bbox(self):
        ox, oy = self.font.getoffset(self.text)
        xmin, ymin, xmax, ymax = self.xymm()
        xmin, ymin = xmin + ox, ymin + oy
        return xmin, ymin, xmax, ymax
        
    def xywh(self):
        w, h = self.textsize()
        return self.x, self.y, w, h
    
    def xymm(self):
        return boxes_ops.xywh_to_xymm(self.xywh())
    
    def coordinate(self):
        return boxes_ops.xymm_to_coord(self.xywh())

            
            