import streamlit as st
from backend.ocr import preprocess_image, perform_ocr, parse_receipt
from frontend.display import show_uploaded_image, display_structured_data

# Set page config for a wider, professional layout
st.set_page_config(page_title="Receipt Scanner", layout="wide")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .title {
        font-size: 2.5em;
        color: #1B5E20;
        text-align: center;
        margin-bottom: 0.2em;
    }
    .subtitle {
        font-size: 1.2em;
        color: #455A64;
        text-align: center;
        margin-bottom: 1em;
    }
    .step {
        font-size: 1.1em;
        color: #1976D2;
        font-weight: bold;
        margin-top: 1em;
    }
    .stButton>button {
        background-color: #388E3C;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    .stExpander {
        border: 1px solid #B0BEC5;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">Receipt Scanner with Tesseract OCR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Easily extract and organize text from your receipts!</div>', unsafe_allow_html=True)

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Customize how we process your receipt:")
    lang = st.text_input("Language", value="eng+fra", help="Use 'eng' for English, 'fra' for French, or 'eng+fra' for both.")
    grayscale = st.checkbox("Grayscale", value=True, help="Converts image to black-and-white for better contrast.")
    threshold = st.checkbox("Thresholding", value=False, help="Makes image fully black or white to enhance text.")

# Step-by-Step Guidance
st.markdown('<div class="step">Step 1: Upload Your Receipt</div>', unsafe_allow_html=True)
st.write("Drop an image of your receipt below (PNG, JPG, or JPEG).")
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    # Step 2: Preview Images
    st.markdown('<div class="step">Step 2: Preview Your Images</div>', unsafe_allow_html=True)
    st.write("Check the original and processed versions of your receipt.")
    col1, col2 = st.columns(2)
    with col1:
        image = show_uploaded_image(uploaded_file, caption="Original Image")
    if image:
        with col2:
            preprocessed_image = preprocess_image(image, grayscale=grayscale, threshold=threshold)
            st.image(preprocessed_image, caption="Processed Image", use_column_width=True)
        
        # Step 3: Extract Text
        st.markdown('<div class="step">Step 3: Extract the Text</div>', unsafe_allow_html=True)
        st.write("Click the button to scan your receipt and see the results.")
        if st.button("Extract Text"):
            with st.spinner("Scanning your receipt..."):
                extracted_text = perform_ocr(preprocessed_image, lang=lang)
            st.subheader("Raw Extracted Text")
            st.write("This is the unprocessed text straight from the image:")
            st.code(extracted_text, language="text")
            
            parsed_data = parse_receipt(extracted_text)
            display_structured_data(parsed_data)
            st.success("🎉 Extraction complete! Scroll up to see the results.")
    else:
        st.warning("Please upload a valid image.")
else:
    st.info("Start by uploading an image above!")

# Footer
st.markdown("---")
st.write("Built with Tesseract OCR and Streamlit. Upload another receipt to try again!")