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
    
