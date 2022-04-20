from ocrdgen.font.font import FontManager
from ocrdgen.image.background import BgManager
from pathlib import Path
import numpy as np
from PIL import ImageDraw, Image
from ocrdgen.ops import boxes_ops
import cv2 as cv
from collections import OrderedDict
from .word import WordDrawer
from .base import BaseDrawer
from ocrdgen import models



class TextDrawer(BaseDrawer):
    def __init__(self, image: np.ndarray, font, text, label, xy, anchor=None, index=0, linking=[], 
                 delimiter=" ", align="left", image_mode="RGBA", fill=(0,0,0),
                 *args, **kwargs):
        super().__init__(image=image, font=font, text=text, xy=xy, 
                         align=align, anchor=anchor, image_mode=image_mode, fill=fill)
        self.label = label
        self.index = index
        self.linking = linking
        self.delimiter = delimiter
    
    def delimiter_size(self):
        w, h = self.idraw.textsize(self.delimiter, self.font)
        return w,h
    
        
    def _build_draw_word(self, word, xy):
        return WordDrawer(image=self.image, font=self.font, 
                          text=word, xy=xy, 
                          anchor=self.anchor,
                          image_mode=self.image_mode, 
                          fill=self.fill)
    
    def custom_bbox(self):
        xywh = self.bbox()
        xmin, ymin, xmax, ymax = boxes_ops.xywh_to_xymm(xywh)
        ymax = self.textbbox()[3] 
        xymm = xmin,ymin,xmax,ymax
        xywh = boxes_ops.xymm_to_xywh(xymm)
        return xywh
    
    def draw_words_text(self, image, text, xy, label=None, line=0, draw_wordbbox=False, draw_charbbox=True):
        text = self._multiwords_split(text)
            
        dw, dh = self.delimiter_size()
        x, y = xy
        data = []
        for idx, txt in enumerate(text):
            
            dword: WordDrawer = self._build_draw_word(txt, (x,y))
            
            tw, th = dword.textsize()
            image, word_bbox = dword.draw(image, draw_bbox=draw_wordbbox)
            image, char_bbox  = dword.draw_char(image, draw_bbox=draw_charbbox)
            
            word_bbox.seq_id = idx
            word_bbox.line = line
            word_bbox.label = label
            
            data.append(word_bbox)

            x = x + tw + dw

        return data, image
    
    def draw_words_bbox(self, text, xy, label=None, line=0):
        text = self._multiwords_split(text)
            
        dw, dh = self.delimiter_size()
        x, y = xy
        data = []
        for idx, txt in enumerate(text):
            
            dword: WordDrawer = self._build_draw_word(txt, (x,y))
            
            tw, th = dword.textsize()
            word_bbox = dword.wordbbox()
            
            word_bbox.seq_id = idx
            word_bbox.line = line
            word_bbox.label = label
            
            data.append(word_bbox)
    
            x = x + tw + dw
            
        return data
    
    def draw_bbox(self, image, color=(0,0,255,255), thick=1):
        xywh = self.custom_bbox()
        xmin, ymin, xmax, ymax = boxes_ops.xywh_to_xymm(xywh)
        np_img = cv.rectangle(np.array(image.copy()), (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, thick)
        
        return Image.fromarray(np_img)
    
    def draw_text(self, draw_bbox=False, draw_wordbbox=False, draw_charbbox=False):
        image = self.image.copy()
        datas = []
        if self._multiline_check(self.text):
            lines = self._multiline_split(self.text)
            lines_info = self._multiline_coord()
            
            for idx, textline in enumerate(lines):
                xy = lines_info['xy'][idx]
                data, image = self.draw_words_text(image, textline, xy, line=idx, draw_wordbbox=draw_wordbbox, draw_charbbox=draw_charbbox)
                datas = datas + data
        else:
            data, image = self.draw_words_text(image, self.text, self.xy, draw_wordbbox=draw_wordbbox, draw_charbbox=draw_charbbox)
            datas = data
            
        if draw_bbox: image = self.draw_bbox(image)

        textbox = models.TextBox(text=self.text, bbox=self.custom_bbox(), words=datas)
            
        return textbox, image
    
    def draw(self, draw_bbox=False, draw_wordbbox=False, draw_charbbox=False):
        textbox, image = self.draw_text(draw_wordbbox=draw_wordbbox, draw_charbbox=draw_charbbox)
        if draw_bbox:
            image = self.draw_bbox(image)
        return textbox, image
    
    def textbox(self):
        datas = []
        if self._multiline_check(self.text):
            lines = self._multiline_split(self.text)
            lines_info = self._multiline_coord()
            
            for idx, textline in enumerate(lines):
                xy = lines_info['xy'][idx]
                data= self.draw_words_bbox(textline, xy, line=idx)
                datas = datas + data
        else:
            data = self.draw_words_bbox(self.text, self.xy)
            datas = data

        textbox = models.TextBox(text=self.text, bbox=self.custom_bbox(), words=datas)
            
        return textbox
    
    
    
   