from .base import BaseWrapper
from typing import *



class FreeTextWrapper(BaseWrapper):
    def __init__(self, file):
        super().__init__(file)
        
    def _template_type_check(self):
        pass
    
    def _default_setting_check(self):
        pass