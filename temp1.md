import streamlit as st
import base64

# PDF file path
pdf_path = "example.pdf"

# Read the PDF file and encode in base64
with open(pdf_path, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

# Embed PDF in HTML
pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>
    """
st.components.v1.html(pdf_display, height=1000, scrolling=True)
