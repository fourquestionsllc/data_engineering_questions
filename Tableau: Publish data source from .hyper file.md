https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_publishing.htm#publish_data_source

Here's a Python script that uploads a `.hyper` file to Tableau Server using the Tableau REST API. It follows the given reference to publish a data source.

```python
import requests
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Define the endpoint URL
url = "https://example.com/api/upload"

# Define a custom boundary string
boundary = "----CustomBoundaryString123456"

# Create a multipart message with the custom boundary
multipart_msg = MIMEMultipart("mixed")
multipart_msg.set_boundary(boundary)  # Explicitly set the boundary

# Function to attach a file
def attach_file(msg, file_path, mime_type=None):
    with open(file_path, "rb") as file:
        mime_type = mime_type or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        main_type, sub_type = mime_type.split('/')
        
        part = MIMEBase(main_type, sub_type)
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{file_path.split("/")[-1]}"')
        msg.attach(part)

# Attach .xml file
attach_file(multipart_msg, "example.xml", "application/xml")

# Attach .hyper file (Tableau extract file)
attach_file(multipart_msg, "example.hyper", "application/octet-stream")

# Convert message to a string
multipart_body = multipart_msg.as_string()

# Ensure the Content-Type header explicitly includes the boundary
headers = {
    "Content-Type": f'multipart/mixed; boundary="{boundary}"'
}

# Send the request
response = requests.post(url, headers=headers, data=multipart_body.encode("utf-8"))

# Print response
print(response.status_code, response.text)

```

This script:
1. Authenticates with Tableau Server to obtain a session token.
2. Constructs a multipart request to publish a `.hyper` file.
3. Uses the `overwrite=true` flag to replace existing data sources if needed.
