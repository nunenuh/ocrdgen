# from dataclasses import dataclass
from typing import *
from pydantic import BaseModel
from pydantic.dataclasses import dataclass



class CharBox(BaseModel):
    seq_id: int
    char: str
    bbox: List
    
class WordBox(BaseModel):
    seq_id: int = 0
    text: str
    bbox: List
    chars: List[CharBox]
    label: str = ""
    line: int = 0
    
class TextBox(BaseModel):
    text: str
    bbox: List
    words: List[WordBox]
    label: str = ""
    linking: List = []
    id: int = 0
    
class TextGroup(BaseModel):
    name: str
    bbox: List
    texts: List[Text]
    label: str = ""
    linking: List = []
    id: int = 0
    
class Form(BaseModel):
    image_filename: str
    json_filename: str
    size: List
    objects: List[Union[Text, TextGroup]]
    
    
    
    
