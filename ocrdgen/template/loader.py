
from pathlib import Path
from typing import *
from abc import ABC, abstractmethod
import pandas as pd
import yaml
from ocrdgen.models.template import *


class TemplateLoader:
    def __init__(self, file):
        self.file: Path = Path(file)
        
        assert self.exists(), f"File Not Exist on path {self.file}"
        assert self.isfile(), f"The file that you give is not file type on path {self.file}"
        assert self.extension()=="yaml", f'only yaml extension is acceptable as file format!'
        
        self.config = self._load(file)
        
    def exists(self):
        return self.file.exists()
    
    def isfile(self):
        return self.file.is_file()
    
    def extension(self):
        ext = self.file.suffix.strip(".")
        return ext
    
    def _load(self, file)->Dict:
        with open(file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    @property
    def name(self):
        return self.config.get("template").get("name")

    @property
    def type(self):
        return self.config.get("template").get("type") 
    
    @abstractmethod
    def _template_type_check(self):
        pass
    
    @abstractmethod
    def _default_setting_check(self):
        pass
    
    @abstractmethod
    def get(self):
        pass
    
    def _image_setting(self):
        dset = self.config.get("general_setting")
        imgset = dset.get("image")
        imgset = GeneralImageSetting(**imgset)
        return imgset
    
    def _font_setting(self):
        dset = self.config.get("general_setting")
        fset = dset.get("font")
        fset =  GeneralFontSetting(**fset)
        return fset
    
    def _margin_setting(self):
        dset = self.config.get("general_setting")
        mset = dset.get("margin")
        mset =  GeneralMarginSetting(**mset)
        return mset
    
    def _text_setting(self):
        dset = self.config.get("general_setting")
        tset = dset.get("text") 
        tset =  GeneralTextSetting(**tset)
        return tset
    
    def general_setting(self):
        image = self._image_setting()
        margin = self._margin_setting()
        font = self._font_setting()
        text = self._text_setting()
        general = GeneralSetting(
            image=image, margin=margin,
            font=font, text=text
        )
        return general
        

class FormTemplateLoader(TemplateLoader):
    def __init__(self, file):
        super().__init__(file)

    def objects(self):
        
        objects = self.config.get("objects")
        keys = list(objects.keys())
        for key in keys:
            objects[key]
            
    

class FreeTextTemplateLoader(TemplateLoader):
    def __init__(self, file):
        super().__init__(file)
    