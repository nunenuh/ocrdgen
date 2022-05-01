
from pathlib import Path
from typing import *
from abc import ABC, abstractmethod
import pandas as pd

from ocrdgen.data.base import BaseData 
import random


from ocrdgen.exception import *

T_co = TypeVar('T_co', covariant=True)
T = TypeVar('T')

class BaseDataset(Generic[T]):
    def __init__(self, filepath):
        self.filepath: Path = Path(filepath)
        
        assert self.exists(), f"File Not Exist on path {self.filepath}"
        assert self.isfile(), f"The filepath that you give is not file type on path {self.filepath}"
        
    def exists(self)->bool:
        return self.filepath.exists()
    
    def isfile(self)->bool:
        return self.filepath.is_file()
    
    @abstractmethod
    def _load_file(self):
        pass
    
    @abstractmethod
    def __len__(self):
        pass
    
    @abstractmethod
    def __getitem__(self, idx):
        pass
    
    @abstractmethod
    def get(self):
        pass


class TextDataset(BaseDataset):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.dframe = self._load_file()
        self.data = self.dframe['text'].to_list()
        
    def _load_file(self):
        lines = pd.read_fwf(str(self.filepath), names=["text"])
        return lines

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx)->T_co:
        return self.data[idx]
    
    def get(self):
        return self.data
    
    
class CSVDataset(BaseDataset):
    def __init__(self, filepath, delimiter=","):
        super().__init__(filepath)
        self.delimiter = delimiter
        self.data = self._load_file()
        
    def _load_file(self):
        csv = pd.read_csv(str(self.filepath), delimiter=self.delimiter)
        return csv

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        return row
    
    def get(self):
        return self.data
    
    def get_by(self, field, idx):
        return self.data[field].iloc[idx]
    
    
class IDCardDataset(BaseDataset):
    def __init__(self, filepath, face_dir, delimiter=","):
        super().__init__(filepath)
        self.delimiter = delimiter
        self.face_dir = face_dir
        self.data = self._load_file()
        self.face_files = self._load_face_dirs()
        
    def _load_file(self):
        csv = pd.read_csv(str(self.filepath), delimiter=self.delimiter)
        return csv
    
    def _load_face_dirs(self):
        self._check_face_dirs_sanity()
        male_files = list(Path(self.face_dir).joinpath('male').glob("*.png"))
        female_files = list(Path(self.face_dir).joinpath('female').glob("*.png"))
        face_files = {
            'male': male_files,
            'female': female_files
        }
        
        return face_files
        
    def _check_face_dirs_sanity(self):
        main_path = Path(self.face_dir)
        male = Path(self.face_dir).joinpath('male')
        female = Path(self.face_dir).joinpath('female')
        
        if not main_path.exists():
            raise DatasetException(f"Directory {self.face_dir} does not exist ")
        
        if not main_path.is_dir():
            raise DatasetException(f"The path {self.face_dir} is not directory")
        
        if not male.exists():
            raise DatasetException(f"Directory male does not exist in path {self.face_dir}")
        
        if not male.is_dir():
            raise DatasetException(f"male is not Directory in path {self.face_dir}")
        
        if len(list(male.glob('*.png')))<=0:
            raise DatasetException(f"there is no jpg data in path {male}")
        
        if not female.exists():
            raise DatasetException(f"Directory female does not exist in path {self.face_dir}")
        
        if not female.is_dir():
            raise DatasetException(f"female is not Directory in path {self.face_dir}")
        
        if len(list(female.glob('*.png')))<=0:
            raise DatasetException(f"there is no jpg data in path {female}")
    
    def _get_random_face(self, gender)->str:
        return random.choice(self.face_files[gender])
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        raw = self.data.iloc[idx]
        row = raw.to_dict()
        
        raw_gender = row['gender']
        if raw_gender=="PEREMPUAN":
            gender = "female"
        else:
            gender = "male"
        
        row['photo'] = str(self._get_random_face(gender))
        return row
    
    def get(self):
        return self.data
    
    def get_by(self, field, idx):
        return self.data[field].iloc[idx]
        
        
        
if __name__ == "__main__":
    ...