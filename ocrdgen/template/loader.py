
from pathlib import Path
import random
from typing import *
from abc import ABC, abstractmethod
import pandas as pd
import yaml
from ocrdgen.models.template import *
from ocrdgen.exception import *


class BaseLoader:
    def __init__(self, setting):
        self.setting = setting

    @abstractmethod
    def _load(self):
        pass
    
    @abstractmethod
    def _check(self):
        pass
    
    @abstractmethod
    def get(self):
        pass
    
class GeneralImageSettingLoader(BaseLoader):
    def __init__(self, setting:Dict):
        super().__init__(setting)
        self.setting = setting
        self.type = self.setting.get("type", None)
        self.root = self.setting.get("root", None)
        self.filename = self.setting.get("filename", None)
        self.filenames = self.setting.get("filenames", None)
        self.size = self.setting.get("size", None)
        self.mode = self.setting.get("mode", None)
        self.extension = self._extension()
        self.files = self._files()
        
        self.setting["extension"]=self.extension
        self.setting["files"]=self.files
        
        
        self._check()
        
        self.object = self._load()
        
        
    def get(self)->GeneralImageSetting:
        return self.object        

    def _load(self)->GeneralImageSetting:
        gimset = GeneralImageSetting(**self.setting)
        return gimset
    
    def _check_root(self):
        if type(self.root) == type(None):
            raise TemplateLoaderException("general_setting->image->root cannot be null")
    
    def _extension(self):
        ext = self.setting.get("extension", None)
        if type(ext)== type(None):
            ext = ["png","jpg","jpeg"]
        return ext
            
    def _files(self):
        if self.type == "random" and type(self.filenames) == type(None):
            files = []
            for ext in self.extension:
                glob = list(Path(self.root).glob(f'*.{ext}'))
                glob = [str(g) for g in glob]
                files = files + glob
        elif self.type == "random" and type(self.filenames) != type(None):
            files = []
            for fname in self.filenames:
                fpath = Path(self.root).joinpath(fname)
                # print(fpath.suffix.strip("."))
                if (fpath.exists() and 
                    fpath.is_file() and
                    fpath.suffix.strip(".") in self.extension):
                    files.append(str(fpath))
        elif self.type == "fixed" and type(self.filename) != type(None):
            files = []
            fpath = Path(self.root).joinpath(self.filename)
            if (fpath.exists() and 
                fpath.is_file() and
                fpath.suffix.strip(".") in self.extension):
                files.append(str(fpath))
        else:
            files = []
            
        return files
    
    def _check(self):
        self._type_null_check()
        self._type_value_check()
        self._type_to_filename_check()
        # self._type_to_filenames_check()
        
    def _type_null_check(self):
        if self.type==None: 
            raise TemplateLoaderException("image->type cannot be null")
        
    def _type_value_check(self):
        if not (self.type == "random" or self.type == "fixed"):
            raise TemplateLoaderException("general_setting->image->type must be set to random or fixed ")
    
    def _type_to_filename_check(self):
        if self.type=="fixed" and self.filename==None:
            raise TemplateLoaderException("general_setting->image->filename cannot be null when image->type set to fixed")
    
    def _type_to_filenames_check(self):    
        if self.type=="random" and self.filenames==None:
            raise TemplateLoaderException("general_setting->image->filenames cannot be null when image->type set to random")

class GeneralFontSettingLoader(BaseLoader):
    def __init__(self, setting:Dict):
        super().__init__(setting)
        self.setting = setting
        self.type = self.setting.get("type", None)
        self.root = self.setting.get("root", None)
        self.filename = self.setting.get("filename", None)
        self.filenames = self.setting.get("filenames", None)
        self.size = self.setting.get("size", None)
        self.encoding = self.setting.get("encoding", None)
        self.variant = self.setting.get("variant", None)
        
        self.extension = self._extension()
        self.files = self._files()
        
        self.setting["extension"]=self.extension
        self.setting["files"]=self.files
        
        self._check()
        
        self.object = self._load()
        
    def get(self)->GeneralFontSetting:
        return self.object        

    def _load(self)->GeneralFontSetting:
        gfontset = GeneralFontSetting(**self.setting)
        return gfontset
    
    def _extension(self):
        ext = self.setting.get("extension", None)
        if type(ext)== type(None):
            ext = ["ttf","otf"]
        return ext
            
    def _files(self):
        if self.type == "random" and type(self.filenames) == type(None):
            files = []
            for ext in self.extension:
                glob = list(Path(self.root).glob(f'*.{ext}'))
                glob = [str(g) for g in glob]
                files = files + glob
        elif self.type == "random" and type(self.filenames) != type(None):
            files = []
            for fname in self.filenames:
                fpath = Path(self.root).joinpath(fname)
                # print(fpath.suffix.strip("."))
                if (fpath.exists() and 
                    fpath.is_file() and
                    fpath.suffix.strip(".") in self.extension):
                    files.append(str(fpath))
        elif self.type == "fixed" and type(self.filename) != type(None):
            files = []
            fpath = Path(self.root).joinpath(self.filename)
            if (fpath.exists() and 
                fpath.is_file() and
                fpath.suffix.strip(".") in self.extension):
                files.append(str(fpath))
        else:
            files = []
            
        return files
    
    def _check(self):
        self._type_null_check()
        self._type_value_check()
        self._type_to_filename_check()
        # self._type_to_filenames_check()
        
    def _type_null_check(self):
        if self.type==None: 
            raise TemplateLoaderException("font->type cannot be null")
        
    def _type_value_check(self):
        if not (self.type == "random" or self.type == "fixed"):
            raise TemplateLoaderException("general_setting->font->type must be set to random orfixed ")
    
    def _type_to_filename_check(self):
        if self.type=="fixed" and self.filename==None:
            raise TemplateLoaderException("general_setting->font->filename cannot be null when general_setting->font->type set to fixed")
    
    def _type_to_filenames_check(self):    
        if self.type=="random" and self.filenames==None:
            raise TemplateLoaderException("general_setting->font->filenames cannot be null when general_setting->font->type set to random")


class GeneralMarginSettingLoader(BaseLoader):
    def __init__(self, setting:Dict):
        super().__init__(setting)
        self.setting = setting
        self.type = self.setting.get("type", "pixel")
        self.top = self.setting.get("top", 0)
        self.bottom = self.setting.get("bottom", 0)
        self.right = self.setting.get("right", 0)
        self.left = self.setting.get("left", 0)
        
        self._check()
        
        self.object = self._load()
        
    def get(self)->GeneralMarginSetting:
        return self.object        

    def _load(self)->GeneralMarginSetting:
        gmarset = GeneralMarginSetting(**self.setting)
        return gmarset
    
    def _check(self):
        self._type_null_check()
        self._type_value_check()
        
    def _type_null_check(self):
        if self.type==None: 
            raise TemplateLoaderException("general_setting->margin->type cannot be null")
        
    def _type_value_check(self):
        if not (self.type == "pixel" or self.type == "percent"):
            raise TemplateLoaderException("general_setting->margin->type must be set to pixel or percent ")
    
class GeneralTextSettingLoader(BaseLoader):
    def __init__(self, setting:Dict):
        super().__init__(setting)
        self.setting = setting
        self.align = self.setting.get("align", "left")
        self.spacing = self.setting.get("spacing", 4)
        self.fill = self.setting.get("fill", None)
        self.stroke_width = self.setting.get("stroke_width", 0)
        self.stroke_fill = self.setting.get("stroke_fill", None)
        self.anchor = self.setting.get("anchor", None)
        
        self._check()
        
        self.object = self._load()
        
    def get(self)->GeneralTextSetting:
        return self.object        

    def _load(self)->GeneralTextSetting:
        gmarset = GeneralTextSetting(**self.setting)
        return gmarset
    
    def _check(self):
       pass

class PositionLoader(BaseLoader):
    def __init__(self, setting:Dict):
        self.setting = setting
        self.x = self.setting.get("x", 0)
        self.y = self.setting.get("y", 0)
        self.xy = self.setting.get("xy",[0,0])
        self.width = self.setting.get("width", 0)
        self.height = self.setting.get("height", 0)
        
        self._check()
        
        self.object = self._load()

    def get(self)->Position:
        return self.object        

    def _load(self)->Position:
        pos = Position(**self.setting)
        return pos
    
    def _check(self):
        pass
    

class FontSettingLoader(BaseLoader):
    def __init__(self, setting:Dict, general:GeneralSetting):
        self.setting:Dict = setting
        self.general:GeneralSetting = general
        self.gfont:GeneralFontSetting = self.general.font

        self._init_attr()
        
        self._check()
        
        self.object = self._load()
        
    def get(self)->FontSetting:
        return self.object
    
    def _init_attr(self):
        if type(self.setting)==type(None):
            self.filename = self._get_filename()
            self.size = self.gfont.size
            self.path = self.gfont.root
        else:
            self.filename = self.setting.get("filename", self._get_filename())
            self.size = self.setting.get("size", self.gfont.size)
            self.path = self.setting.get("path", self.gfont.root)
    
    def _get_filename(self):
        if self.gfont.type=="fixed":
            filename = self.gfont.filename
        elif self.gfont.type=="random":
            filename = random.choice(self.gfont.filenames)
        return filename
        
    def _load(self)->FontSetting:
        fontset = FontSetting(filename=self.filename, size=self.size, path=self.path)
        return fontset
        
    def _check(self):
        # self._setting_check()
        pass
    
    def _setting_check(self):
        if self.setting!=None:
            raise TemplateLoaderException("objects->text_object->font_setting cannot be null")

class TextSettingLoader(BaseLoader):
    def __init__(self, setting:Dict, general:GeneralSetting):
        self.setting:Dict = setting
        self.general:GeneralSetting = general
        self.gtext:GeneralTextSetting = self.general.text
        
        self._check()
        
        self.object:TextSetting = self._load()
        
    def get(self)->TextSetting:
        return self.object
        
    def _load(self)->TextSetting:
        if type(self.setting)==type(None):
            textset = TextSetting(**self.gtext.dict())
            self.align = textset.align
            self.spacing = textset.spacing
            self.fill = textset.fill
            self.stroke_width = textset.stroke_width
            self.stroke_fill = textset.stroke_fill
            self.anchor = textset.anchor
        else:
            self.align = self.setting.get("align", self.gtext.align)
            self.spacing = self.setting.get("spacing", self.gtext.spacing)
            self.fill = self.setting.get("fill", self.gtext.fill)
            self.stroke_width = self.setting.get("stroke_width", self.gtext.stroke_width)
            self.stroke_fill = self.setting.get("stroke_fill", self.gtext.stroke_fill)
            self.anchor = self.setting.get("anchor", self.gtext.anchor)
            
            data = {"align": self.align, "spacing": self.spacing, 
                    "fill": self.fill, "stroke_width": self.stroke_width, 
                    "stroke_fill": self.stroke_fill, "anchor": self.anchor}
            textset = TextSetting(**data)
        return textset
        
    def _check(self):
        # self._setting_check()
        pass
    
    def _setting_check(self):
        if self.setting!=None:
            raise TemplateLoaderException("objects->text_object->font_setting cannot be null")

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

    def objects(self):
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

        obj['position'] = self._object_position(pos)
        obj['font_setting'] = self._object_font_setting(font)
        obj['text_setting'] = self._object_text_setting(text)

        form_text = FormTextObject(**obj)
        
        return form_text
    
    def _object_position(self, pos_dict):
        pos = PositionLoader(pos_dict)
        return pos.get()
    
    def _object_font_setting(self, fontset:Dict):
        fontset = FontSettingLoader(fontset, self.setting)
        return fontset.get()
    
    def _object_text_setting(self, textset:Dict):
        textset = TextSettingLoader(textset, self.setting)
        return textset.get()
    

class FreeTextTemplateLoader(TemplateLoader):
    def __init__(self, file):
        super().__init__(file)
        
    def objects(self):
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

        obj['position'] = self._object_position(pos)
        obj['font_setting'] = self._object_font_setting(font)
        obj['text_setting'] = self._object_text_setting(text)

        text_obj = TextObject(**obj)
        
        return text_obj
    
    def _object_position(self, pos_dict):
        pos = PositionLoader(pos_dict)
        return pos.get()
    
    def _object_font_setting(self, fontset:Dict):
        fontset = FontSettingLoader(fontset, self.setting)
        return fontset.get()
    
    def _object_text_setting(self, textset:Dict):
        textset = TextSettingLoader(textset, self.setting)
        return textset.get()
    