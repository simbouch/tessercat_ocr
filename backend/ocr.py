# backend/ocr.py

import pytesseract
from PIL import Image, ImageOps
import re

def preprocess_image(image: Image.Image, grayscale: bool = True, threshold: bool = False) -> Image.Image:
    """
    Preprocess the image to improve OCR accuracy.
    
    Parameters:
        image (PIL.Image.Image): Input image.
        grayscale (bool): If True, convert image to grayscale.
        threshold (bool): If True, apply binary thresholding.
        
    Returns:
        PIL.Image.Image: The processed image.
    """
    if grayscale:
        image = ImageOps.grayscale(image)
    if threshold:
        # Apply binary thresholding with a cutoff (adjust 128 as needed)
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
    return image

def perform_ocr(image: Image.Image, lang: str = "eng") -> str:
    """
    Use Tesseract to perform OCR on the provided image.
    
    Parameters:
        image (PIL.Image.Image): The image to process.
        lang (str): Tesseract language code (e.g., "eng", "fra", or "eng+fra").
        
    Returns:
        str: The raw text extracted from the image.
    """
    text = pytesseract.image_to_string(image, lang=lang)
    return text

def parse_receipt(text: str) -> dict:
    """
    Parse the extracted receipt text into structured data.
    
    Parameters:
        text (str): The raw OCR text extracted from a receipt.
    
    Returns:
        dict: A dictionary with keys "header", "items", and "totals".
    """
    # Split text into lines
    lines = text.splitlines()
    parsed_data = {
        "header": [],
        "items": [],
        "totals": []
    }
    
    # Regex pattern to detect price formats (e.g., "12,34")
    price_pattern = re.compile(r"\d+,\d{2}")
    
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            continue
        # If line includes keywords indicating totals or tax information
        if any(keyword in stripped_line.upper() for keyword in ["TOTAL", "TVA", "TTC", "HT"]):
            parsed_data["totals"].append(stripped_line)
        # If the line contains a price, consider it an item line
        elif price_pattern.search(stripped_line):
            parsed_data["items"].append(stripped_line)
        else:
            parsed_data["header"].append(stripped_line)
            
    return parsed_data
