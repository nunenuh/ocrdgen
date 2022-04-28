import random
from functools import lru_cache
from pathlib import Path
from typing import List, Set, Tuple, Dict, Optional, Union

from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont
from fontTools.ttLib import TTFont, TTCollection
from loguru import logger

from ocrdgen.exception import PanicException
from ocrdgen.utils import load_chars_file

# base code developed and taken 
# from https://github.com/oh-my-ocr/text_renderer/blob/master/text_renderer/bg_manager.py

class FontLoader:
    def __init__(self, path:str, size:int):
        self.path = Path(path)
        self.size = size
        self.font_support_chars_cache: set = set()
        self.font_support_chars_intersection_with_chars = set()

        assert self.path.exists(),  PanicException(f"font file not exist: {self.path}")
        assert self.path.is_file(), PanicException(f"path you provide is not file : {self.path}")
        
        self._load_font_support_chars()
        
    def _load_font_support_chars(self):
        ttf = self._load_ttfont(str(self.path))

        chars_int = set()
        try:
            for table in ttf["cmap"].tables:
                for k, v in table.cmap.items():
                    chars_int.add(k)
        except AssertionError as e:
            logger.error(f"Load font file {self.path} failed, skip it. Error: {e}")

        supported_chars = set([chr(c_int) for c_int in chars_int])

        ttf.close()

        self.font_support_chars_cache = supported_chars
    
    def _load_ttfont(self, font_path: str) -> TTFont:
        """
        Read ttc, ttf, otf font file, return a TTFont object
        """

        # ttc is collection of ttf
        if font_path.endswith("ttc"):
            ttc = TTCollection(font_path)
            # assume all ttfs in ttc file have same supported chars
            return ttc.fonts[0]

        if (
            font_path.endswith("ttf")
            or font_path.endswith("TTF")
            or font_path.endswith("otf")
        ):
            ttf = TTFont(
                font_path, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1
            )

            return ttf
    
    
    @lru_cache()
    def _get_font(self, font_path: str, font_size: int) -> FreeTypeFont:
        font = ImageFont.truetype(font_path, font_size)
        return font
    
    def get_font(self) -> Tuple[FreeTypeFont, Set, str]:
        font = self._get_font(str(self.path), self.size)
        return font
    
    def support_chars(self):
        return self.font_support_chars_cache

    def update_font_support_chars(self, chars_file):
        """
        Although some fonts have a specific character in the cmap, the rendered text is blank on the image.

        Parameters
        ----------
        chars_file: Path
            one char per line
        """
        white_list = [" "]

        charset = load_chars_file(chars_file)
        removed_chars = []
        font = self._get_font(self.path, 10)
        chars = self.font_support_chars_cache[self.path].copy()
        for c in chars & charset:
            bbox = font.getmask(c).getbbox()
            if (
                c not in white_list
                and bbox is None
                and c in self.font_support_chars
            ):
                self.font_support_chars_cache.remove(c)
                removed_chars.append(c)

        if len(removed_chars) != 0:
            if len(removed_chars) > 10:
                logger.info(
                    f"Remove {len(removed_chars)} empty char mask from font [{self.path}]: {removed_chars[:10]}..."
                )
            else:
                logger.info(
                    f"Remove {len(removed_chars)} empty char mask from font [{self.path}]: {removed_chars}"
                )

        self.font_support_chars_intersection_with_chars = (
            self.font_support_chars_cache & chars
        )

    def check_support(self, text: str, chars: Set) -> Tuple[bool, Set]:
        # Check whether all chars in text exist in chars
        text_set = set(text)
        intersect = text_set - chars
        status = len(intersect) == 0

        return status, intersect

    

   