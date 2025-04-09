import pytesseract
from PIL import Image, ImageOps
import re

def preprocess_image(image: Image.Image, grayscale: bool = True, threshold: bool = False) -> Image.Image:
    if grayscale:
        image = ImageOps.grayscale(image)
    if threshold:
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
    return image

def perform_ocr(image: Image.Image, lang: str = "eng") -> str:
    text = pytesseract.image_to_string(image, lang=lang)
    return text

def parse_receipt(text: str) -> dict:
    lines = text.splitlines()
    parsed_data = {
        "header": [],
        "items": [],
        "totals": []
    }
    price_pattern = re.compile(r"\d+,\d{2}")
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if any(keyword in stripped_line.upper() for keyword in ["TOTAL", "TVA", "TTC", "HT"]):
            parsed_data["totals"].append(stripped_line)
        elif price_pattern.search(stripped_line):
            parsed_data["items"].append(stripped_line)
        else:
            parsed_data["header"].append(stripped_line)
            
    return parsed_data