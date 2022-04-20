from typing import *
import numpy as np
from ocrdgen.ops import boxes_ops
from dataclasses import dataclass

# from dataclasses import dataclass
from typing import *
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


#types
Point = Tuple[int,int]

@dataclass
class BBox(BaseModel):
    x: int
    y: int
    w: int
    h: int
    
    @property
    def xmin(self)->int:
        return int(self.x)

    @property
    def ymin(self)->int:
        return int(self.y)

    @property
    def xmax(self)->int:
        return int(self.x + self.w)
    
    @property
    def ymax(self)->int:
        return int(self.y + self.h)
    
    @property
    def width(self):
        return self.w
    
    @property
    def height(self):
        return self.h
    
    @property
    def size(self):
        return self.width, self.height
    
    def to_coordinate(self)->np.ndarray:
        xywh = self.x, self.y, self.w, self.h
        coord = boxes_ops.xywh_to_coord(xywh)
        return coord
    
    def to_xyminmax(self)->np.ndarray:
        xywh = self.x, self.y, self.w, self.h
        xymm = boxes_ops.xywh_to_xymm(xywh)
        return xymm
    
    def to_list(self):
        return [self.x, self.y, self.w, self.h]
    
    def copy(self)->"BBox":
        return BBox(self.x, self.y, self.w, self.h)
    


    

    