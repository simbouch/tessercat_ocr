# app.py

import streamlit as st
from backend.ocr import preprocess_image, perform_ocr, parse_receipt
from frontend.display import show_uploaded_image, display_structured_data

st.title("Tesseract OCR Streamlit App")

# File uploader for image files (PNG, JPG, JPEG)
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Input for Tesseract language code (default is English)
lang = st.text_input("Tesseract Language", value="eng+fra")  # Use "fra" for French, "eng+fra" for both, etc.

# Options for image preprocessing
grayscale = st.checkbox("Convert to Grayscale", value=True)
threshold = st.checkbox("Apply Thresholding", value=False)

if uploaded_file:
    # Display the original image
    image = show_uploaded_image(uploaded_file, caption="Original Image")
    if image:
        # Preprocess the image based on user choices
        preprocessed_image = preprocess_image(image, grayscale=grayscale, threshold=threshold)
        st.image(preprocessed_image, caption="Preprocessed Image", use_container_width=True)
        
        # Extract text using Tesseract
        with st.spinner("Extracting text..."):
            extracted_text = perform_ocr(preprocessed_image, lang=lang)
        
        st.subheader("Extracted Text")
        st.text(extracted_text)
        
        # Parse the extracted text into structured data
        parsed_data = parse_receipt(extracted_text)
        st.subheader("Structured Receipt Data")
        display_structured_data(parsed_data)
