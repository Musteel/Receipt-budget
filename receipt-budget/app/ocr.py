import io
import easyocr
from PIL import Image
import pytesseract
import numpy as np

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'])
    return _reader

def run_ocr(image_bytes: bytes) -> str:
    try:
        reader = _get_reader()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        results = reader.readtext(np.array(image), detail=0)
        text = "\n".join(results)
        if len(text.strip()) > 10:
            return text
    except Exception as e:
        pass

    # Fallback to pytesseract
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('L')
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return ""