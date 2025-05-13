Certainly. Here's a detailed and focused subsection for your project documentation that exclusively describes the **view image data** for Tableau dashboards:

---

### 3.4 Tableau View Image Structure

This subsection defines the structure and management of **Tableau view images**, which are static PNG screenshots of financial dashboards. These images are used as a visual reference for various analytical operations in the AI tool.

#### 3.4.1 Definition

View images are high-resolution **PNG** files representing static snapshots of Tableau dashboards. Each image corresponds to a unique Tableau **view** (either a dashboard or worksheet). These screenshots capture the full visual layout of the dashboards at the time they were exported and are used for display, indexing, and visual context retrieval.

#### 3.4.2 Storage and Format

Each view image is saved as an individual file in `.png` format. The images are stored in a structured directory or a storage service (e.g., file system, object storage, or database-backed blob storage). The file path is recorded and associated with the corresponding Tableau view metadata in a dedicated database table.

#### 3.4.3 Database Table: `view_images`

The metadata for each view image is stored in the table `view_images`. This table maintains the relationship between a Tableau view and its corresponding image file.

**Table Schema:**

| Column Name       | Data Type | Description                                                 |
| ----------------- | --------- | ----------------------------------------------------------- |
| `view_id`         | STRING    | A unique identifier for the Tableau view (foreign key)      |
| `view_image_path` | STRING    | File path (relative or absolute) to the stored `.png` image |

* `view_id` uniquely identifies the Tableau view. It corresponds to the primary identifier used in other view-related tables (e.g., workbooks, data sources).
* `view_image_path` stores the path to the screenshot image file. This path may be local (e.g., `/images/1234_view.png`) or remote (e.g., `s3://tableau-snapshots/1234_view.png`).

#### 3.4.4 File Naming Convention

Images are stored using a consistent and descriptive naming scheme to ensure clarity and traceability:

```
<view_id>_<optional_dashboard_name>_<timestamp>.png
```

Example:

```
a789_market_summary_20250510.png
```

This convention helps uniquely identify each screenshot and tie it back to its originating dashboard.

#### 3.4.5 Image Consistency and Versioning

Each view image reflects a specific point in time. The system does not currently maintain version history for images, so any updates to dashboards should be accompanied by a replacement of the corresponding image and update of the `view_image_path`.

To ensure consistency:

* All images should reflect the latest published state of the dashboard.
* Image updates must overwrite the existing file or update the metadata record accordingly.

---

Let me know if you'd like this formatted into a particular style (e.g., Markdown, technical spec template), or if you need a companion schema for SQL creation.



Here is a well-structured documentation section describing the **Tableau View Structure** in your AI tool project for CitiGroup:

---

## 📊 Tableau View Structure

The **Tableau View Structure** is the foundation of how the AI tool interacts with and searches through Tableau dashboards. Each *view* represents a specific visual component or page within a Tableau workbook, such as a dashboard, chart, or sheet. These views are extracted, processed, and stored in a structured **SQLite database** to support efficient retrieval using keyword search, semantic similarity, and direct database querying.

### 🔸 Data Source

All view-related metadata is persisted in a local **SQLite database** table, containing a structured schema that reflects key aspects of Tableau's view configuration.

---

### 🧱 Schema Details

Each record in the views table corresponds to a Tableau view and contains the following fields:

| Field Name     | Description                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `view_id`      | A **UUID** representing the unique identifier of the view within Tableau. Used as a primary key.                              |
| `view_name`    | The **title or label** of the view, typically shown in Tableau dashboards.                                                    |
| `@contentUrl`  | A **relative path** within the Tableau site pointing to the view location. Example: `EMEAExpenseDashboard/sheets/Navigation`. |
| `@createdAt`   | **Timestamp** when the view was created in Tableau, in ISO 8601 format (e.g., `2023-08-11T16:48:58Z`).                        |
| `@updatedAt`   | **Timestamp** when the view was last updated. Useful for tracking stale or recently modified dashboards.                      |
| `@viewUrlName` | A simplified **URL-friendly name** of the view, often identical or similar to `view_name`, used in constructing full URLs.    |
| `workbook`     | A nested object representing the **parent workbook** that contains the view. It includes the workbook ID and metadata.        |
| `owner`        | A nested object representing the **creator or owner** of the view. Includes a user ID and metadata.                           |
| `project`      | A nested object indicating the **project folder** in Tableau where the workbook/view resides.                                 |
| `tags`         | Any user-defined **tags or labels** assigned to the view for classification. Often `None` unless explicitly tagged.           |
| `location`     | A JSON-like object representing the **hierarchical location** of the view inside Tableau (site, project, workbook).           |
| `site_id`      | The **unique identifier of the Tableau site** where the view is hosted.                                                       |
| `project_id`   | The **ID of the Tableau project folder** associated with the view.                                                            |
| `workbook_id`  | The **ID of the workbook** containing this view, used to link views to broader dashboard collections.                         |

---

### 🧾 Sample Data Illustration

From the attached sample, the structure of each entry is illustrated with real examples:

* **Navigation View**

  * `view_id`: `0fb50cd3-4dc8-488d-8ed9-6cccf73a484b`
  * `view_name`: `Navigation`
  * `@contentUrl`: `EMEAExpenseDashboard/sheets/Navigation`
  * `workbook_id`: `8f12f3a6-a26e-43e5-ad8f-f6c2ee495aa`
  * `project_id`: `0b1e4d15-78a4-492b-9fa0-e1718a1fa165`
  * `site_id`: `3d72ddde-8497-4e47-994c-4465d93ccd6f`

This shows how the AI tool can trace each view back to its location, ownership, and last modification date.

---

### 🧠 Role in AI Tool Architecture

The view metadata is used by all three search modes in the AI tool:

* **Keyword Search**: Matches user-extracted keywords against `view_name`, `@contentUrl`, `tags`, and potentially embedded summaries of the view content.
* **Semantic Search**: Uses the view's content summary embedding to compare against the vectorized user query, returning views with the highest similarity.
* **Database Search**: Executes SQL-like queries directly over this view table to fetch matching views by any attribute (e.g., find all views created after a certain date by a specific owner or in a certain project).

---

### 🧩 Benefits of This Structure

* **Scalability**: Easily supports thousands of views across multiple Tableau projects and sites.
* **Traceability**: View linkage to workbook, owner, and site ensures complete traceability.
* **Flexibility**: The schema allows extending with additional metadata (e.g., summary embeddings, access permissions, or usage statistics).

---

Let me know if you'd like a section describing how the embeddings are stored or linked to these views for semantic search.



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
