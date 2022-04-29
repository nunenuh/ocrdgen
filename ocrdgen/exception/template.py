# taken from https://github.com/oh-my-ocr/text_renderer/blob/8fe3260ec952128d4d1b18dd41a7a82efa8f50c4/text_renderer/utils/errors.py
# with small modification

class TemplateLoaderException(Exception):
    """If this error raised, render process should stop because some non-random error has occurred"""
    pass

