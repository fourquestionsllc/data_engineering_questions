Here's a Python script that uploads a `.hyper` file to Tableau Server using the Tableau REST API. It follows the given reference to publish a data source.

This script:
1. Authenticates with Tableau Server to obtain a session token.
2. Constructs a multipart request to publish a `.hyper` file.
3. Uses the `overwrite=true` flag to replace existing data sources if needed.
