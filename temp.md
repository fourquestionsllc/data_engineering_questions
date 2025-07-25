```
import ipywidgets as widgets
from IPython.display import display

view_url_input = widgets.Text(
    value='',
    placeholder='Enter Tableau view URL',
    description='View URL:',
    disabled=False
)

def handle_input(change):
    global view_url
    view_url = change['new']
    print("URL received:", view_url)

view_url_input.observe(handle_input, names='value')
display(view_url_input)

```
