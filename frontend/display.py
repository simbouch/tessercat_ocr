import streamlit as st
from PIL import Image

def show_uploaded_image(uploaded_file, caption="Uploaded Image") -> Image.Image:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption=caption, use_column_width=True)
        return image
    except Exception as e:
        st.error(f"Error opening image: {e}")
        return None

def display_structured_data(parsed_data: dict):
    st.markdown("### Organized Receipt Data")
    st.write("Here’s what we found in your receipt, split into three parts:")
    
    with st.expander("📋 Store Details (Header)", expanded=True):
        st.markdown("**What this is**: Information about the store, like name, address, or date.")
        if parsed_data.get("header"):
            for line in parsed_data["header"]:
                st.markdown(f"- {line}")
        else:
            st.info("No store details detected.")

    with st.expander("🛒 Purchased Items", expanded=True):
        st.markdown("**What this is**: The list of items you bought with their prices.")
        if parsed_data.get("items"):
            for i, line in enumerate(parsed_data["items"], 1):
                st.markdown(f"{i}. {line}")
        else:
            st.info("No items detected.")

    with st.expander("💰 Summary (Totals)", expanded=True):
        st.markdown("**What this is**: Total amounts, taxes, or payment details.")
        if parsed_data.get("totals"):
            for line in parsed_data["totals"]:
                st.markdown(f"- {line}")
        else:
            st.info("No totals detected.")