import enum
from ocrdgen.font.font import FontManager
from ocrdgen.image.background import BgManager
from pathlib import Path
import numpy as np
from PIL import ImageDraw, Image
from ocrdgen.ops import boxes_ops
import cv2 as cv
from collections import OrderedDict

from .base import BaseDrawer
from ocrdgen import models


class WordDrawer(BaseDrawer):
    def __init__(self, image: Image, font, text, xy, align="left", anchor=None,
                 image_mode="RGBA", fill=(0,0,0)):
        super().__init__(image=image, font=font, text=text, xy=xy,
                         anchor=anchor, 
                         align=align, image_mode=image_mode, fill=fill)
        
        text_test = self.text.strip().split(" ")
        # print(len(text_split), text_split)
        assert len(text_test) == 1, f"Error, expected one word only, but more word is given!"
        
    def draw_text(self, image=None):
        if type(image) == type(None):
            image = self.image.copy()
        idraw = ImageDraw.Draw(image)
        idraw.text(self.xy, self.text, font=self.font, fill=self.fill)
        # idraw.textbbox()
        return image
    
    def draw_bbox(self, image, color=(255,0,0,255), thick=1):
        xmin, ymin, xmax, ymax = self.xymm_with_offset(self.text, self.x, self.y)
        np_img = cv.rectangle(np.array(image), (xmin, ymin), (xmax, ymax), color, thick)
        
        return Image.fromarray(np_img)
    
    def draw(self, image=None, draw_bbox=False, bbox_color=(255, 0, 0, 255), bbox_thick=1):
        image = self.draw_text(image)
        bbox = self.wordbbox()
        if draw_bbox:
            image = self.draw_bbox(image, color=bbox_color, thick=bbox_thick)
        return image, bbox
    
    def wordbbox(self):
        wordbox = models.WordBox(text=self.text, bbox=self.textbbox(), chars=self.charbbox())
        return wordbox
    
    def charbbox(self):
        data = []
        xmin, ymin = self.x, self.y
        for i in range(len(self.text)):
            if len(self.text[i])>0:
                xymm = self.xymm_with_offset(self.text[i], xmin, ymin)
                xywh = boxes_ops.xymm_to_xywh(xymm)
                dt = models.CharBox(char=self.text[i], bbox=xywh, seq_id=i)
                # dt = (self.text[i], xywh)
                _, _, xmax, _ = xymm
                xmin = xmax
                
                data.append(dt)
                
        return data
    
    def draw_char_text(self, image=None):
        image = self.draw_text(image)
        return image
    
    def draw_char_bbox(self, image, color=(0,255,0,255), thick=1):
        image: np.ndarray = np.array(image)
        charboxes = self.charbbox()
        for idx, charbox in enumerate(charboxes):
            char, xywh = charbox.char, charbox.bbox
            xmin,ymin,xmax,ymax = boxes_ops.xywh_to_xymm(xywh)
            if char!=" ":
            # xmin, ymin, xmax, ymax = self.xymm_with_offset(char, x, y)
                image = cv.rectangle(image, (xmin, ymin), (xmax, ymax), color, thick)
            
        image: Image = Image.fromarray(image)
        return image
    
    def draw_char(self, image=None, draw_bbox=False, bbox_color=(0,255,0,255), bbox_thick=1):
        image = self.draw_char_text(image)
        bbox = self.charbbox()
        if draw_bbox:
            image = self.draw_char_bbox(image, color=bbox_color, thick=bbox_thick)
        return image, bbox
    

    
    
    