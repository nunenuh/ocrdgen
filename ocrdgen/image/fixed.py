import random
from re import L
from typing import *
from pathlib import Path
from PIL import Image
from functools import lru_cache
from abc import ABC, abstractmethod

from ocrdgen.image.base import BaseImageLoader

IMAGE_EXTENSIONS = ['jpg', 'JPG', 'jpeg', 'JPEG', 
                   'png', 'PNG', 'bmp','BMP']


class FixedImageLoader(BaseImageLoader):
    def __init__(self, path, size:Union[List[int], None]=None, 
                 safe_resize=False, extensions:List[str]=["png","PNG"]):
        super().__init__(path, size, safe_resize, extensions)
        self.image = None
    
    def _check_onload(self):
        if not (self._exist()):
            raise Exception(f"File Not Exist on path {self.path}")
        
        if not self._is_file():
            raise Exception(f"The file that you give is not file type on path {self.path}")
        
        if not self._is_image():
            raise Exception(f"The file that you give is not image type on path {self.path}")
            
        if not self._is_ext_allowed():
            raise Exception(f"The file that you give is not allowed ext type on path {self.path}")
               
        
    def _load(self, path:Path, convert="RGBA"):
        self._check_onload()
        im = Image.open(str(path))
        if type(self.size) != type(None):
            im = self._resize(im, self.size, self.safe_resize)
        im.convert(convert)

        return im
        
    def __len__(self):
        return 1
        
    def load(self, path:Path)->Image:
        image = self._load(path)
        return image
    
    def get_image(self)->Image:
        self.image = self.load(self.path)
        return self.image

    def get(self)->Image:
        return self.get_image()
    