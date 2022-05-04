from typing import *
from abc import ABC, abstractmethod

from ocrdgen.data.datasets import BaseDataset
from ocrdgen.template.loader import TemplateLoader


class BaseMixture:
    def __init__(self, dataset, template):
        self.dataset: BaseDataset = dataset
        self.template: TemplateLoader = template
    
    @abstractmethod
    def _mixture(self):
        pass
    
    @abstractmethod
    def __len__(self):
        pass
    
    @abstractmethod
    def __getitem__(self, idx):
        pass
    

    
    



