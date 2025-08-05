import streamlit as st
from PIL import Image

# Load image from local file
image = Image.open("example.png")

# Display image
st.image(image, caption='Example PNG', use_column_width=True)
