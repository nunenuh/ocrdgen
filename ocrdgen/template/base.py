from abc import ABC, abstractmethod
import yaml
from typing import *

class BaseWrapper:
    def __init__(self, file):
        self.config = self._load(file)
    
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