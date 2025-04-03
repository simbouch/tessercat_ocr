# frontend/display.py

import streamlit as st
from PIL import Image

def show_uploaded_image(uploaded_file, caption="Uploaded Image") -> Image.Image:
    """
    Open and display the uploaded image in the Streamlit app.
    
    Parameters:
        uploaded_file: The file uploaded via Streamlit.
        caption (str): Caption to display with the image.
        
    Returns:
        PIL.Image.Image: The opened image, or None if an error occurs.
    """
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption=caption, use_container_width=True)
        return image
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return None

def display_structured_data(parsed_data: dict):
    """
    Display the parsed receipt data in a structured format.
    
    Parameters:
        parsed_data (dict): Dictionary with keys "header", "items", and "totals".
    """
    st.subheader("Header Information")
    for line in parsed_data.get("header", []):
        st.write(line)
        
    st.subheader("Items")
    for line in parsed_data.get("items", []):
        st.write(line)
        
    st.subheader("Totals")
    for line in parsed_data.get("totals", []):
        st.write(line)
