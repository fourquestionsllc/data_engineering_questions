To create a text box in a **Jupyter Notebook** for user input, you can use the `ipywidgets` library. Here's how to do it:

---

### ✅ Example with `ipywidgets.Text`:

```python
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
```

---

### 💡 What This Does

* Shows a textbox labeled "Input:"
* When the user hits Enter, it triggers `on_submit()` and prints the entered value.

---

### 🛠 Install `ipywidgets` if needed

If it’s not installed yet:

```bash
pip install ipywidgets
```

And enable it for Jupyter:

```bash
jupyter nbextension enable --py widgetsnbextension
```

Let me know if you want dropdowns, sliders, or more interactive forms too.
