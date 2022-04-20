import random
import numpy as np
from typing import *
from loguru import logger
from ..exception import PanicException

SPACE_CHAR = " "


# taken from https://github.com/oh-my-ocr/text_renderer/blob/8fe3260ec952128d4d1b18dd41a7a82efa8f50c4/text_renderer/utils/utils.py#L12
# with modification
def probability(percent: float, low:float=0, high:float=1):
    assert low <= percent <= high
    if np.random.uniform(low=low, high=high) <= percent:
        return True
    return False

# taken from https://github.com/oh-my-ocr/text_renderer/blob/8fe3260ec952128d4d1b18dd41a7a82efa8f50c4/text_renderer/utils/utils.py#L22
# with some modification
def random_choice(items: list, size=1):
    choices = []
    for i in range(size):
        n = np.random.randint(0, len(items))
        choices.append(items[n])
    if size == 1:
        return choices[0]
    return choices
    
    
#taken from https://github.com/oh-my-ocr/text_renderer/blob/8fe3260ec952128d4d1b18dd41a7a82efa8f50c4/text_renderer/utils/utils.py#L136
def load_chars_file(chars_file, log=False):
    """

    Args:
        chars_file (Path): one char per line
        log (bool): Whether to print log

    Returns:
        Set: chars in file

    """
    assumed_space = False
    with open(str(chars_file), "r", encoding="utf-8") as f:
        lines = f.readlines()
        _lines = []
        for i, line in enumerate(lines):
            line_striped = line.strip()
            if len(line_striped) > 1:
                raise PanicException(
                    f"Line {i} in {chars_file} is invalid, make sure one char one line"
                )

            if len(line_striped) == 0 and SPACE_CHAR in line:
                if assumed_space is True:
                    raise PanicException(f"Find two space in {chars_file}")

                if log:
                    logger.info(f"Find space in line {i} when load {chars_file}")
                assumed_space = True
                _lines.append(SPACE_CHAR)
                continue

            _lines.append(line_striped)

        lines = _lines
        chars = set("".join(lines))
    if log:
        logger.info(f"load {len(chars)} chars from: {chars_file}")
    return chars
