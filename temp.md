# Convert binary data to an image
image = Image.open(io.BytesIO(binary_data))

# Display the image in Jupyter Notebook
display(image)
