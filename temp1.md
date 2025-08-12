Here’s a quick Python example to load a `.env` file into environment variables:

```python
import os
from dotenv import load_dotenv

# Load the .env file into environment variables
load_dotenv(dotenv_path=".env")  # defaults to ".env" in current dir

# Access variables
server_url = os.getenv("server_url")
api_version = os.getenv("api_version")
token_name = os.getenv("token_name")
token_value = os.getenv("token_value")
site_id = os.getenv("site_id")

print(server_url, api_version, site_id)
```

**Requirements:**

```bash
pip install python-dotenv
```

**Notes:**

* If your `.env` file is in another directory, pass its path to `load_dotenv()`.
* This method does not overwrite existing environment variables unless you set `override=True`.

If you want, I can also show you a **one-liner way** without installing any packages.
