from dataclasses import dataclass
from typing import *



    

class Words:
    text: str
    box: List[int, int, int, int]

@dataclass
class FormData:
    id: int
    box: List[int, int, int, int]
    text: str
    label: str
    words: List[Words]
    linking: List[List]
    
    
    
    
