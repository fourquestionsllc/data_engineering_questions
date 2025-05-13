Project Overview & Use Cases

Business Objectives

User Personas & Scenarios

Key Features & Functionalities

Data Sources & Tableau View Structure

LLM Integration Architecture

Natural Language Query Flow

Semantic Search & Keyword Matching

Database Search Logic

Prompt Engineering & Fine-tuning

Model Management & Versioning

Tech Stack & Dependencies

Performance Optimization

Security & Compliance

Testing & Quality Assurance

Deployment Guide

Maintenance & Monitoring

Troubleshooting & Support

Future Enhancements

Reference Links & Resources

Appendix (Code Samples, API Specifications, etc.)



Certainly! Here's the rewritten **Data Sources** section, focusing specifically on the **logic**, **flow**, and **URL formats** for how data is collected via the Tableau REST API:

---

### Data Sources

The tool queries and compiles comprehensive Tableau metadata from all registered sites using Tableau’s REST API. The process extracts key entities including views, view images, workbooks, data sources, and workbook revisions. Each resource is fetched through authenticated HTTP requests, parsed from XML, and stored for downstream use. Below is a detailed explanation of how each type of data is obtained, including the URL format for each API call.

#### 1. **Views**

To retrieve all Tableau dashboard views:

* The script loops through each site retrieved from a database (`SELECT * FROM sites`).
* For each site, it paginates through the `/views` endpoint using a page size of 188 (maximum allowed by Tableau).
* **URL format:**

  ```
  https://{server_url}/api/{api_version}/sites/{site_id}/views?pagesize=188&pageNumber={page_number}
  ```
* Each response contains a batch of `<view>` elements, which are parsed and accumulated.
* Pagination continues until the API returns no more results.
* This ensures all dashboard views across all sites are fully captured.

#### 2. **View Images**

For each view retrieved:

* The tool attempts to locate a cached image locally; if not found, it downloads a fresh image from Tableau.
* Image is fetched as a binary stream using the `/views/{view_id}/image` endpoint.
* **URL format:**

  ```
  https://{server_url}/api/{api_version}/sites/{site_id}/views/{view_id}/image
  ```
* On success (HTTP 200), the image is saved locally (e.g., `images/image_{view_id}.png`).
* If the request fails (non-200), the error message is parsed and logged for inspection.

#### 3. **Workbooks**

To retrieve workbook metadata for each site:

* The script sends a GET request to the `/workbooks` endpoint, requesting up to 1000 items per site.
* **URL format:**

  ```
  https://{server_url}/api/{api_version}/sites/{site_id}/workbooks?pagesize=1000
  ```
* The returned XML is parsed into a DataFrame, and each workbook record is annotated with its site ID.
* This includes attributes such as workbook name, ID, project association, and modification date.

#### 4. **Data Sources**

Data sources connected to Tableau views are collected using:

* The `/datasources` endpoint, again paginated with a high page size to reduce the number of requests.
* **URL format:**

  ```
  https://{server_url}/api/{api_version}/sites/{site_id}/datasources?pagesize=1000
  ```
* The response provides detailed metadata including data source names, types, and project linkage.
* Each data source is tagged with the site it belongs to.

#### 5. **Workbook Revisions**

For version tracking, the tool retrieves all revisions for each workbook:

* The script iterates over all workbooks and calls the `/revisions` endpoint for each one.
* **URL format:**

  ```
  https://{server_url}/api/{api_version}/sites/{site_id}/workbooks/{workbook_id}/revisions
  ```
* The response may contain a single revision or a list of revisions, both of which are normalized into a flat structure.
* Each revision record is associated with its parent workbook for traceability.

---

This structured querying pipeline ensures the system captures a rich, hierarchical snapshot of the Tableau ecosystem, which is then used to support intelligent search through LLMs, semantic embedding models, keyword indexing, and direct SQL queries.
