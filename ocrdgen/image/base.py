import random
from re import L
from typing import *
from pathlib import Path
from PIL import Image
from functools import lru_cache
from abc import ABC, abstractmethod

IMAGE_EXTENSIONS = ['jpg', 'JPG', 'jpeg', 'JPEG', 
                   'png', 'PNG', 'bmp','BMP']


class BaseImageLoader:
    def __init__(self, path, size:Union[List[int], None]=None, 
                 safe_resize=False, extensions:List[str] = ["png","PNG"]):
        self.path:Path = Path(path)
        self.size = size
        self.safe_resize = safe_resize
        self.extensions = extensions
        self.image = None
        
    def _exist(self, path:Path = None)->bool:
        if type(path)==type(None):
            return self.path.exists()
        else:
            return path.exists()
    
    def _is_file(self, path:Path = None)->bool:
        if type(path)==type(None):
            return self.path.is_file()
        else:
            return path.is_file()
    
    def _is_dir(self, path:Path = None)->bool:
        if type(path)==type(None):
            return self.path.is_dir()
        else:
            return path.is_dir()
    
    def _is_image(self, path:Path = None)->bool:
        if type(path)==type(None):
            if self.path.suffix.strip(".") in IMAGE_EXTENSIONS:
                return True
            return False
        else:
            if path.suffix.strip(".") in IMAGE_EXTENSIONS:
                return True
            return False
    
    def _is_ext_allowed(self, path:Path = None)->bool:
        if type(path)==type(None):
            if self.path.suffix.strip(".") in self.extensions:
                return True
            return False
        else:
            if path.suffix.strip(".") in self.extensions:
                return True
            return False
        
    def _resize(self, image:Image, size: Tuple[int, int], safe_resize:bool=False)->Image:
        """
        make sure background size is large than input size
        """
        
        if safe_resize:
            rwidth, rheight = size
            iwidth, iheight = image.size
            
            # prevent image smaller than size
            scale = max(rwidth / iwidth, rheight / iheight)
            if scale > 1:
                swidth, sheight = int(iwidth * scale), int(iheight * scale)
                image = image.resize((swidth, sheight))
                # print(f"resize image to {swidth}x{sheight}")
            # print(f'scale: {scale}')
        else:
            rwidth, rheight = size
            image = image.resize((rwidth, rheight))
            # print(f'image resize to {rwidth}x{rheight}')

        return image
    
    @abstractmethod
    def _load(self):
        pass
    
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def get(self):
        pass
    
    @abstractmethod
    def get_image(self):
        pass
    