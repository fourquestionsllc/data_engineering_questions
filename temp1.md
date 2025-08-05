import streamlit as st

# Path to your PDF
pdf_file_path = "example.pdf"

# Read PDF in binary mode
with open(pdf_file_path, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")

# Embed PDF in HTML
pdf_display = f'''
    <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="700" 
        height="1000" 
        type="application/pdf">
    </iframe>
    '''

# Show PDF
import streamlit.components.v1 as components
components.html(pdf_display, height=1000)
