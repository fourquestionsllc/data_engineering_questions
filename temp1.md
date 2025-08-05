import streamlit as st
from pdf2image import convert_from_path

# Path to your PDF
pdf_path = "example.pdf"

# Convert first page to image
images = convert_from_path(pdf_path, first_page=1, last_page=1)

# Show image
st.image(images[0], caption="First page of PDF", use_column_width=True)
