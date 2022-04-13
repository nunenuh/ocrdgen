from ocrdgen.manager.font import FontManager
from ocrdgen.manager.background import BgManager
from pathlib import Path
import numpy as np
from PIL import ImageDraw, Image
from ocrdgen.ops import boxes_ops
import cv2 as cv
from collections import OrderedDict


class DrawWord:
    def __init__(self, image: np.ndarray, font, text, x, y, image_mode="RGBA", color=(0,0,0)):
        self.image = image.copy()
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.idraw = ImageDraw.Draw(self.image)
        self.image_mode = image_mode
        
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
    
    def draw(self, debug_draw=False, rcolor=(0,255,0,255), rthick=1):
        self.idraw.text((self.x, self.y), self.text, font=self.font, fill=self.color)
        if debug_draw:
            image = self._draw_rectangle(color=rcolor, thick=rthick)
            return image
        
        return self.image
    
    def bbox(self):
        xymm = self.xymm_bbox()
        xywh = boxes_ops.xymm_to_xywh(xymm)
        return xywh
    
        
    def char_bbox(self, otype=OrderedDict, debug_draw=False, color=(0,255,0,0), thick=1):
        image = self.image.copy()
        np_image = np.array(image)
        
        data = []
        xmin, ymin = self.x, self.y
        for i in range(len(self.text)):
            if len(self.text[i])>0:
                tw, th = self.font.getsize(self.text[i])
                ox, oy = self.font.getoffset(self.text[i])
                xmax, ymax = xmin + tw, ymin + th
                xminr, yminr = xmin + ox, ymin + oy
                
                if debug_draw: 
                    # print(self.text[i],f'{i}-iter')
                    image = Image.fromarray(np_image)
                    draw = ImageDraw.Draw(image)
                    draw.text((xmin,ymin), self.text[i], font=self.font, fill=self.color)
                    np_image = cv.rectangle(np.array(image), (xminr, yminr), (xmax, ymax), color, thick)
                    
                    
                xymm = [xminr, yminr, xmax, ymax]
                xywh = boxes_ops.xymm_to_xywh(xymm)
                points = boxes_ops.xywh_to_coord(xywh)
                xmin = xmax
                if otype==OrderedDict:
                    dt = OrderedDict({"char": self.text[i], "bbox": xywh})
                else:
                    dt = (self.text[i], xywh)
                data.append(dt)
                
        
        return data, Image.fromarray(np_image)
    
    
    def _draw_rectangle(self, color=(0,255,0), thick=3):
        xmin, ymin, xmax, ymax = self.xymm()
        ox, oy = self.font.getoffset(self.text)
        xminr, yminr = xmin + ox, ymin + oy
        
        # print(xmin, xminr, ymin, yminr)
        np_img = cv.rectangle(np.array(self.image.copy()), (xminr, yminr), (xmax, ymax), color, thick)
        
        return Image.fromarray(np_img)
    
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
