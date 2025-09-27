import io
import easyocr
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'])
    return _reader

def run_ocr(file_bytes: bytes) -> str:

    image = Image.open(io.BytesIO(file_bytes)).convert("L")
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    text = pytesseract.image_to_string(image)
    return text