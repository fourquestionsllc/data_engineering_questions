from IPython.display import display
from PIL import Image
import io

# Convert binary data to an image
image = Image.open(io.BytesIO(binary_data))

# Display the image in Jupyter Notebook
display(image)
