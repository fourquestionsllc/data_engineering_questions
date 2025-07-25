import ipywidgets as widgets
from IPython.display import display

# Create a text box
text_box = widgets.Text(
    value='',
    placeholder='Type something',
    description='Input:',
    disabled=False
)

# Function to handle input change
def on_submit(change):
    print("You entered:", change.value)

# Attach the function to the text box
text_box.on_submit(on_submit)

# Display the text box
display(text_box)
