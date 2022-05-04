from typing import *
from abc import ABC, abstractmethod

from ocrdgen.data.datasets import BaseDataset, CSVDataset
from ocrdgen.models.template import FormTemplateModel
from ocrdgen.template.loader import TemplateLoader, FormTemplateLoader
from ocrdgen.mixture.base import BaseMixture



class FormMixture(BaseMixture):
    def __init__(self, dataset, template):
        super().__init__(dataset, template)
        self.dataset: CSVDataset = dataset
        self.template: FormTemplateLoader = template
        
    def _mixture(self, idx)->FormTemplateModel:
        row = self.dataset[idx]
        keys = list(row.keys())
        for idx, obj in enumerate(self.template.objects):
            if obj.field_type == 'value' and obj.field_name in keys:
                obj.text = row[obj.field_name]
                
            self.template.objects[idx] = obj
        
        return self.template.get()
    
    
    def __len__(self):
        return len(self.dataset)
        
    def __getitem__(self, idx)->FormTemplateModel:
        ftm = self._mixture(idx)
        return ftm


class FreeMixture(BaseMixture):
    def __init__(self, dataset, template):
        super().__init__(dataset, template)
        
        
    def _mixture(self, idx):
        pass
    
    def __getitem__(self, idx):
        pass
    