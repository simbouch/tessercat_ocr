

# Tesseract OCR Streamlit App

**Prerequisites**  
- Python 3.8+  
- Tesseract + French data:  
  ```bash
  sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-fra

## Setup & Run
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run main.py
