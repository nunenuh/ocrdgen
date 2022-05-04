
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

class RandomImageLoader(BaseImageLoader):
    def __init__(self,path, size:Union[Tuple[int, int], None]=None, 
                 safe_resize=False, extensions:List[str]=["png","PNG"],
                 glob_pattern='*.ext'):
        super().__init__(path, size, safe_resize, extensions)
        self.glob_pattern = glob_pattern
        self.files = self._files()
    
    def _files(self):
        files = []
        for ext in self.extensions:
            pattern = self.glob_pattern.replace("ext", ext)
            files = files + list(self.path.glob(pattern))
        
        if len(files)<=0:
            raise Exception(f"No image found in {self.path}")
        
        return files
    
    @lru_cache(maxsize=32)
    def _load(self, path:Path, convert="RGBA")->Image:
        self._check_onload(path)
        
        im = Image.open(str(path))
        if type(self.size) != type(None):
            im = self._resize(im, self.size, self.safe_resize)
        im.convert(convert)

        return im
        
    def _check_onload(self, path):
        if not (self._exist(path)):
            raise Exception(f"File Not Exist on path {self.path}")
        
        if not self._is_file(path):
            raise Exception(f"The file that you give is not file type on path {self.path}")
        
        if not self._is_image(path):
            raise Exception(f"{path} is not an image")
        
        if self._is_image(path) and not self._is_ext_allowed(path):
            raise Exception(f"{path} is not an allowed extension")
    
    
    def load(self, idx:int):
        path = self.files[idx]
        return self._load(path)
    
    def __len__(self):
        return len(self.files)
        
    def get_image(self)->Image:
        path = random.choice(self.files)
        image = self._load(path)
        return image 
    
    def get(self):
        return self.get_image()