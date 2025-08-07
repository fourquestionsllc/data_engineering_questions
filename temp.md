To store and load your Tableau API credentials securely in Python, you can follow these steps:

---

### ✅ Step 1: Create the `.env` File

Create a file named `.env` in your project directory with the following content:

```env
SERVER_URL=dev.forecastvisualanalytics.citigroup.net
API_VERSION=3.19
TOKEN_NAME=fpna-jingyan
TOKEN_VALUE=cwY67X+bRLaJwuogUNUdyw==:30Lg7GgBBB93i6MicI7s5]cpIOpWDA2u
SITE_ID=3d72ddde-8497-4e47-994c-4465d93ccd6f
```

---

### ✅ Step 2: Install `python-dotenv` (if not already)

```bash
pip install python-dotenv
```

---

### ✅ Step 3: Load `.env` Variables in Python

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Assign to variables
server_url = os.getenv("SERVER_URL")
api_version = os.getenv("API_VERSION")
token_name = os.getenv("TOKEN_NAME")
token_value = os.getenv("TOKEN_VALUE")
site_id = os.getenv("SITE_ID")

# Print to verify (optional)
print("Server URL:", server_url)
print("API Version:", api_version)
print("Token Name:", token_name)
print("Token Value:", token_value)
print("Site ID:", site_id)
```

---

### 🔒 Security Tips

* Add `.env` to your `.gitignore` file to avoid committing credentials to version control.
* Rotate secrets periodically, especially if they’ve been shared or exposed.

Let me know if you want to validate connection to Tableau with these values next.
