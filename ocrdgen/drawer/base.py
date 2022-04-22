import numpy as np
from typing import *
from ocrdgen.font.font import FontManager
from ocrdgen.image.background import BgManager
from pathlib import Path
import numpy as np
from PIL import ImageDraw, Image
from ocrdgen.ops import boxes_ops
import cv2 as cv
from collections import OrderedDict
from abc import ABC, abstractmethod
from PIL.ImageFont import FreeTypeFont
import string
import textwrap
from textwrap import wrap

class BaseDrawer:
    def __init__(self, image: Image, font: FreeTypeFont, text: str, xy: tuple,
                 fill=(0,0,0), image_mode:str="RGBA",
                 anchor:Union[str, None]=None, spacing:int=4, align:str="left", 
                 direction=None, features=None, language=None,
                 stroke_width:int=0, stroke_fill:Union[tuple, None]=None,
                 *args, **kwargs):
        self.image = image.copy()
        self.font = font
        self.text = text.strip()
        self.xy = xy
        self.x, self.y = xy[0], xy[1]
        self.fill = fill
        self.image_mode = image_mode
        self.anchor = anchor
        self.spacing = spacing
        self.align = align
        self.direction = direction
        self.features = features
        self.language = language
        self.stroke_width = stroke_width
        self.stroke_fill = stroke_fill

        self.idraw = ImageDraw.Draw(self.image)

    @abstractmethod
    def draw_text(self):
        pass
    
    @abstractmethod
    def draw_bbox(self, image, color=(0,255,0,255), thick=1):
        pass
    
    @abstractmethod
    def draw(self, draw_bbox=False, bbox_color=(0,255,0,255), bbox_thick=1):
        pass
       
    def image_size(self):
        h,w = np.array(self.image).shape[:2]
        return w,h
        
    def textsize(self):
        w, h = self.idraw.textsize(self.text, self.font)
        return w,h
    
    def xywh(self):
        w, h = self.textsize()
        return self.x, self.y, w, h
    
    def xymm(self):
        return boxes_ops.xywh_to_xymm(self.xywh())
    
    def coordinate(self):
        return boxes_ops.xymm_to_coord(self.xywh())
    
    def position(self):
        iw, ih = self.image_size()
        tw, th = self.textsize()
        w, h = (iw - tw) / 2, (ih - th) / 2
        return w, h
    
    def xymm_bbox(self):
        xmin, ymin, xmax, ymax = self.xymm()
        ox, oy = self.font.getoffset(self.text)
        xmin, ymin = xmin + ox, ymin + oy
        return xmin, ymin, xmax, ymax
    
    def xymm_with_offset(self, text, xmin, ymin):
        # xmin, ymin, xmax, ymax = self.xymm()
        tw, th = self.font.getsize(text)
        ox, oy = self.font.getoffset(text)
        xmax, ymax = xmin + tw, ymin + th
        xminr, yminr = xmin + ox, ymin + oy
        xymm = xminr, yminr, xmax, ymax
        
        return xymm
    
    def bbox(self):
        xymm = self.xymm_bbox()
        xywh = boxes_ops.xymm_to_xywh(xymm)
        return xywh
    
    def textbbox(self):
        return self.idraw.textbbox(xy=self.xy, text=self.text, 
                                   font=self.font, align=self.align)
    
    def multiline_textbbox(self):
        return self.idraw.multiline_textbbox(xy=self.xy, text=self.text, 
                                             font=self.font, align=self.align)
        
    def _multiline_check(self, text):
        """Draw text."""
        split_character = "\n" if isinstance(text, str) else b"\n"

        return split_character in text

    def _multiline_split(self, text):
        split_character = "\n" if isinstance(text, str) else b"\n"

        return text.split(split_character)
    
    def _multiwords_check(self, text, delimiter: str = " "):
        split_delimiter = delimiter if isinstance(text, str) else bytes(delimiter, "utf-8")
        
        return split_delimiter in text
    
    def _multiwords_split(self, text, delimiter: str = " "):
        word_list = [txt.strip() for txt in text.split(delimiter) if len(txt.strip())> 0]
        return word_list
    
    def _multiline_coord(self):
        
        if self.direction == "ttb":
            raise ValueError("ttb direction is unsupported for multiline text")

        if self.anchor is None:
            self.anchor = "la"
        elif len(self.anchor) != 2:
            raise ValueError("anchor must be a 2 character string")
        elif self.anchor[1] in "tb":
            raise ValueError("anchor not supported for multiline text")
        
        widths = []
        max_width = 0
        lines = self._multiline_split(self.text)
        line_spacing = (
            self.idraw.textsize("A", font=self.font, stroke_width=self.stroke_width)[1] + self.spacing
        )
        
        for line in lines:
            line_width = self.idraw.textlength(
                line, self.font, direction=self.direction, features=self.features, language=self.language
            )
            widths.append(int(line_width))
            max_width = max(max_width, line_width)
            
        top = self.xy[1]
        if self.anchor[1] == "m":
            top -= (len(lines) - 1) * line_spacing / 2.0
        elif self.anchor[1] == "d":
            top -= (len(lines) - 1) * line_spacing
        
        lines_xy = []
        for idx, line in enumerate(lines):
            left = self.xy[0]
            width_difference = max_width - widths[idx]

            # first align left by anchor
            if self.anchor[0] == "m":
                left -= width_difference / 2.0
            elif self.anchor[0] == "r":
                left -= width_difference

            # then align by align parameter
            if self.align == "left":
                pass
            elif self.align == "center":
                left += width_difference / 2.0
            elif self.align == "right":
                left += width_difference
            else:
                raise ValueError('align must be "left", "center" or "right"')

            # draw text here if you want to draw it
            
            new_xy  = (int(left), int(top))
            lines_xy.append(new_xy)
            
            top += line_spacing
        
        return {
            'xy': lines_xy,
            'width': widths,
            'max_width': int(max_width),
            'line_spacing': line_spacing,
        }
        
    def textwrap(self, text, max_width=0, max_height=0):
        mw, mh = self._safe_max_size()
        if max_width == 0 : max_width = mw
        if max_height == 0: max_height = mh
        
        mean = self._mean_char_length()
        line_width = max_width/mean
        lines = wrap(text, width=line_width)
        return lines
    
    
    def _mean_char_length(self):
        data = [self.idraw.textlength(c, font=self.font) for c in string.ascii_letters]
        return np.array(data).mean()
    
    def _safe_max_size(self, xy=None):
        imsize = self.image_size()
        if xy==None:
            mw = imsize[0] - self.x
            mh = imsize[1] - self.y
        else:
            mw = imsize[0] - xy[0]
            mh = imsize[1] - xy[1]
        return mw,mh
            
        