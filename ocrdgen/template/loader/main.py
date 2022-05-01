
from pathlib import Path
import random
from typing import *
from abc import ABC, abstractmethod
import pandas as pd
import yaml
from ocrdgen.models.template import *
from ocrdgen.exception import *
from .base import BaseLoader
from .sub import (
    GeneralImageSettingLoader, 
    GeneralMarginSettingLoader, 
    GeneralFontSettingLoader,
    GeneralTextSettingLoader
)



class TemplateLoader:
    def __init__(self, file):
        self.file: Path = Path(file)
        
        assert self.exists(), f"File Not Exist on path {self.file}"
        assert self.isfile(), f"The file that you give is not file type on path {self.file}"
        assert self.extension()=="yaml", f'only yaml extension is acceptable as file format!'
        
        self.config = self._load(file)
        gset = self.config.get("general_setting", None)
        if type(gset) == type(None):
            raise TemplateLoaderException("general_setting cannot be null!")
        
        self.header: TemplateHeader = self._template_header()
        self.image = self._image_setting()
        self.margin = self._margin_setting()
        self.font = self._font_setting()
        self.text = self._text_setting()
        self.setting: GeneralSetting = self._general_setting() 
        
    def exists(self)->bool:
        return self.file.exists()
    
    def isfile(self)->bool:
        return self.file.is_file()
    
    def extension(self)->str:
        ext = self.file.suffix.strip(".")
        return ext
    
    def _load(self, file)->Dict:
        with open(file, 'r') as file:
            config = yaml.safe_load(file)
        return config

    @abstractmethod
    def _template_type_check(self):
        pass
    
    @abstractmethod
    def _default_setting_check(self):
        pass
    
    @abstractmethod
    def get(self):
        pass
    
    def _template_header(self)->TemplateHeader:
        header = self.config.get("template")
        header = TemplateHeader(**header)
        return header 
    
    def _image_setting(self)->GeneralImageSetting:
        imgset = self.config.get("general_setting").get("image")
        imgset = GeneralImageSettingLoader(imgset)
        return imgset.get()
    
    def _margin_setting(self)->GeneralMarginSetting:
        mset = self.config.get("general_setting").get('margin')
        mset =  GeneralMarginSettingLoader(mset)
        return mset.get()
    
    def _font_setting(self)->GeneralFontSetting:
        fset = self.config.get("general_setting").get("font")
        fset =  GeneralFontSettingLoader(fset)
        return fset.get()
    
    def _text_setting(self)->GeneralTextSetting:
        tset = self.config.get("general_setting").get("text") 
        tset =  GeneralTextSettingLoader(tset)
        return tset.get()
    
    def _general_setting(self)->GeneralSetting:
        general = GeneralSetting(
            image=self.image, margin=self.margin, font=self.font, text=self.text
        )
        return general
    
class FormTemplateLoader(TemplateLoader):
    def __init__(self, file):
        super().__init__(file)
        self.objects = self._objects()
    
    def _objects(self):
        new_objects = []
        objects:Dict = self.config.get("objects")
        keys = list(objects.keys())
        for key in keys:
            obj_dict = objects.get(key)
            text_object = self._parse_text_object(key, obj_dict)
            new_objects.append(text_object)       
        return new_objects

    def _parse_text_object(self, name, obj):
        obj['name'] = name
        pos = obj.get("position", None)
        font = obj.get("font_setting", None)
        text = obj.get("text_setting", None)
        
        # if type(pos) == type(None): 
        obj['position'] = self._object_position(pos)
        # if type(font) == type(None):
        obj['font_setting'] = self._object_font_setting(font)
        # if type(text) == type(None):
        obj['text_setting'] = self._object_text_setting(text)

        form_text = FormTextObject(**obj)
        
        return form_text
    
    def _object_position(self, pos_dict):
        pos = PositionLoader(pos_dict)
        return pos.get()
    
    def _object_font_setting(self, fontset:Dict):
        fontset = FontSettingLoader(fontset, self.setting)
        print(fontset)
        return fontset.get()
    
    def _object_text_setting(self, textset:Dict):
        textset = TextSettingLoader(textset, self.setting)
        return textset.get()
    

class FreeTemplateLoader(TemplateLoader):
    def __init__(self, file):
        super().__init__(file)
        self.objects = self._objects()
    
    def _objects(self):
        new_objects = []
        objects:Dict = self.config.get("objects")
        keys = list(objects.keys())
        for key in keys:
            obj_dict = objects.get(key)
            text_object = self._parse_text_object(key, obj_dict)
            new_objects.append(text_object)       
        return new_objects

    def _parse_text_object(self, name, obj):
        obj['name'] = name
        pos = obj.get("position", None)
        font = obj.get("font_setting", None)
        text = obj.get("text_setting", None)
        
        # if type(pos) == type(None): 
        obj['position'] = self._object_position(pos)
        # if type(font) == type(None):
        obj['font_setting'] = self._object_font_setting(font)
        # if type(text) == type(None):
        obj['text_setting'] = self._object_text_setting(text)

        form_text = TextObject(**obj)
        
        return form_text
    
    def _object_position(self, pos_dict):
        pos = PositionLoader(pos_dict)
        return pos.get()
    
    def _object_font_setting(self, fontset:Dict):
        fontset = FontSettingLoader(fontset, self.setting)
        print(fontset)
        return fontset.get()
    
    def _object_text_setting(self, textset:Dict):
        textset = TextSettingLoader(textset, self.setting)
        return textset.get()
    