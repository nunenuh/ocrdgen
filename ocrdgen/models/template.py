# from dataclasses import dataclass
from typing import *
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class GeneralImageSetting(BaseModel):
    type: str
    root: str
    filenames: List
    size: List
    mode: Dict
    
class GeneralMarginSetting(BaseModel):
    type: str
    top: int
    bottom: int
    right: int
    left: int

class GeneralFontSetting(BaseModel):
    type: str
    root: str
    filenames: List
    size: int
    encoding: Optional[Union[str, None]] = None
    variant: Optional[Union[str, None]] = None

class GeneralTextSetting(BaseModel):
    align: Optional[Union[str, None]] = 'left'
    spacing: Optional[int] = 4
    fill: Optional[Union[List, None]] = None
    stroke_width: Optional[int] = 0
    stroke_fill: Optional[List] = None
    anchor: Optional[str] = None
    
class GeneralSetting(BaseModel):
    image: GeneralImageSetting
    margin: GeneralMarginSetting
    font: GeneralFontSetting
    text: GeneralTextSetting
    
class Position(BaseModel):
    x: Optional[int] = 0
    y: Optional[int] = 0
    xy: Optional[list] = [0,0]
    width: Optional[Union[int, None]] = None
    height: Optional[Union[int, None]] = None
    
class FontSetting(BaseModel):
    name: str
    size: int
    path: Optional[Union[str, None]] = None

class TextSetting(BaseModel):
    align: Optional[Union[str, None]] = 'left'
    spacing: Optional[int] = 4
    fill: Optional[Union[List, None]] = None
    stroke_width: Optional[int] = 0
    stroke_fill: Optional[List] = None
    anchor: Optional[str] = None

class TextObject(BaseModel):
    type: str = "text"
    name: str
    position: Position
    font: Optional[Union[FontSetting, None]] = None
    text: Optional[Union[FontSetting, None]] = None
    
class FormTextObject(TextObject):
    label: str
    classname: str
    linked: List