Here's a detailed documentation section you can include to describe the **SQL-based Tableau dashboard search** capability of your AI tool at CitiGroup:

---

## SQL Query-Based Tableau Dashboard Search

The **SQL-based search module** provides a powerful mechanism to retrieve Tableau dashboards and related metadata by directly querying the underlying database schema. This approach is ideal when users’ questions refer to structural elements such as **project names**, **workbook revisions**, **datasource links**, **URLs**, or **specific fields** like dashboard summaries and sizes.

It complements keyword and semantic search by enabling **structured, precise, and data-driven access** to Tableau assets.

---

### Overview

This method works by translating a user's natural language question into an executable **SQL query** using a large language model (LLM). The query is run against a SQLite database that mirrors the structure and content of Tableau views, workbooks, projects, data sources, and more. The resulting records are then used to construct answers for the user.

---

### Step-by-Step Process

#### 1. **Schema Awareness and Aliases**

Before generating the SQL, the system initializes the schema and provides it to the LLM in the prompt. The prompt explicitly describes the structure of the following tables:

* **projects** – Contains project-level metadata.
* **workbooks** – Contains workbook name, description, URLs, summaries, and default view IDs.
* **datasources** – Stores data source names and their associated project/site.
* **workbook\_datasource\_connection** – (Used for workbook-to-datasource mappings).
* **revisions** – Contains workbook revision history including publisher, publish time, and size.
* **view\_keywords** – Associates view IDs with manually or automatically assigned keywords.

To enhance natural language flexibility, synonyms for commonly used terms are embedded into the prompt. For example:

* *View* may be called: slide, page, chart, graph, diagram, table, or tag.
* *Workbook* may be called: report, dashboard, visualization, story, canvas, or collection.

This ensures that even vague or colloquial user questions can be mapped to the correct SQL logic.

---

#### 2. **Keyword & Field Extraction (Optional Enhancement)**

To guide the SQL generation, the system may first extract **field-level concepts or entity names** from the user's question using a lightweight keyword extraction function powered by LLM. These values (e.g., workbook names, view IDs, known keywords) are inserted into the SQL generation prompt to improve accuracy and reduce ambiguity.

---

#### 3. **LLM-Based SQL Generation**

The natural language question, available field values, and database schema are passed to the LLM using a structured instruction prompt:

```text
"In the sqlite db we have the following tables with the schema as follows..."
```

The LLM is instructed to:

* Generate **only the SQL code**, with no extra text.
* Select appropriate fields depending on what the user asked.
* Always include informative columns such as name, URL, summary, and image path if specific fields are not mentioned.
* Handle synonyms and rephrased terms gracefully.

Sample questions:

* *"Show dashboards about credit risk analysis"* → SQL to search workbook descriptions or summaries.
* *"Get me the size of the latest revisions for project Alpha"* → SQL to query the `revisions` table filtered by `project name`.
* *"Which reports are using datasource X?"* → SQL joining `datasources` and `workbooks`.

---

#### 4. **Query Execution and Result Formatting**

Once the SQL is generated:

* It is **sanitized** to remove any leading/trailing characters.
* Executed via `pandas.read_sql()` over the connected SQLite database.
* The result is converted to:

  * A **DataFrame** (`result_df`) for programmatic use,
  * A **JSON string** (`result_json`) for rendering in downstream applications,
  * A list of **candidate entity names** used in the SQL, for traceability or user feedback.

All results contain fields like:

* `view name`, `workbook name`, `URL`, `summary`, and `image path` (when available),
* Fields explicitly requested by the user (e.g., publish time, revision size).

---

### Example

**User Query**:

> *"Which dashboards under project Retail have more than 3 revisions and who published the last one?"*

**Generated SQL** (simplified):

```sql
SELECT workbooks.workbook_name, revisions.revision_publisher_name
FROM workbooks
JOIN revisions ON workbooks.workbook_id = revisions.workbook_id
WHERE workbooks.project_name = 'Retail'
GROUP BY workbooks.workbook_name
HAVING COUNT(revisions.workbook_revision_number) > 3
```

---

### Benefits

* **Precision**: Direct access to structured fields (e.g., workbook size, revision number).
* **Explainability**: Clear SQL logic that can be logged, audited, or manually refined.
* **Coverage**: Useful when the question is about metadata or structural attributes not captured in text summaries (e.g., revision history, URL paths).

---

### Summary

The SQL-based dashboard search module enables **deep and accurate** retrieval of Tableau content by translating natural language into executable SQL. It is especially valuable when:

* The user is asking about **specific database fields**,
* The question references **data lineage**, **publishing metadata**, or **entity relationships**,
* Or when the other methods (semantic/keyword search) may return overly broad results.

By using an LLM guided with strict schema constraints and structured instructions, the system ensures reliable SQL generation and meaningful Tableau insights.

---

Let me know if you'd like me to create visual flow diagrams or add usage examples for each table.



Here's a well-written and detailed section you can include in your documentation to describe the **semantic search** functionality in your AI tool for querying Tableau financial dashboards at CitiGroup:

---

## Semantic Search-Based Tableau Dashboard Retrieval

The **semantic search module** allows users to query financial dashboards in Tableau using natural language questions, even when there's no exact keyword overlap between the question and the dashboard content. This is achieved by embedding both the user queries and the dashboard summaries into a shared high-dimensional vector space and retrieving the most semantically similar matches.

### Overview

Semantic search works by computing vector embeddings for:

1. **User questions**.
2. **Synthetic questions** derived from each Tableau dashboard's summary (via LLM-based reverse engineering).

The semantic similarity is then measured by computing the **dot product** between these embeddings. The top-matching dashboards are returned based on this similarity score.

---

### Step-by-Step Process

#### 1. **Synthetic Question Generation from View Summaries**

Each Tableau dashboard has a descriptive **summary** that is reverse-engineered into a list of questions that someone might ask to retrieve the dashboard.

* A large language model (LLM) is prompted with each dashboard summary using the following instruction:

```plaintext
"Below are the text of summary of a Tableau view. Pretending you do not know the existence of the view yet, 
but when you ask some questions or make some requests, we need to bring this view up because it has the answer. 
Generate such questions which can bring this view up from many views, such as: 
'Which view contains ...' or 'Show me the dashboard of ...'"
```

* The LLM responds with a list of relevant, high-quality questions per dashboard summary, e.g.:

```python
["Which view shows Q4 trends for institutional clients?", 
 "Show me the dashboard with investment banking revenue breakdown",
 "Where can I find data on regional operating income?"]
```

These synthetic questions serve as semantic anchors to enable retrieval later.

#### 2. **Embedding Synthetic Questions**

The generated questions are embedded using the **`gte-large-en-v1.5`** model, accessed via the Stellar API (`StellarEmbeddings`). This model converts each question into a 768-dimensional dense vector, optimized for semantic similarity tasks in English.

* The resulting embeddings are stored in a PostgreSQL (or compatible) table along with metadata:

  * `text_id` (hash of the question),
  * `embedding` (stored as a JSON string),
  * `embedding_model` (to support future model upgrades),
  * `original text` (question).

This forms the searchable semantic index.

#### 3. **Embedding the User Query**

When a user submits a question, it is also embedded using the same **`gte-large-en-v1.5`** model to ensure consistency in the vector space. The embedding is compared against the stored question embeddings from the dashboards.

#### 4. **Semantic Matching via Dot Product**

The user query vector is multiplied (dot product) with each stored question embedding to compute similarity scores. This yields a ranked list of dashboard-related questions most semantically similar to the user’s query.

* The helper function `top_k_above_threshold()` filters and selects the **top-k matches** that exceed a similarity threshold (default: 450). It returns the indices of the best-matching synthetic questions.

#### 5. **Retrieving Matched Dashboards**

Once the top matching synthetic questions are identified:

* Their associated **question IDs** are hashed using `md5()`.
* These IDs are used to query a relational database table (`view_summary_questions`) to retrieve metadata about the corresponding Tableau views:

  * `view_name`
  * `view_url`
  * `view_summary`
  * `view_image_path`

The final output includes:

* A dataframe (`df`) with full metadata on all matched views,
* A list of records (for display),
* The matched synthetic questions that triggered the retrieval.

---

### Embedding Model Highlight

* **Model Used**: `gte-large-en-v1.5`
* **Provider**: Stellar AI via `StellarEmbeddings`
* **Embedding Dimension**: 768
* **Characteristics**:

  * Trained for **general-purpose English sentence embeddings**.
  * Strong performance in semantic similarity and dense retrieval tasks.
  * Lightweight enough for fast inference, yet robust for enterprise-scale search scenarios.

Using a high-quality embedding model ensures that the system can effectively match user intent to relevant dashboards, even if the user's terminology differs from the text in the dashboards.

---

### Summary

The semantic search component significantly enhances the system's flexibility and user-friendliness by enabling **context-aware**, **meaning-driven** retrieval of Tableau dashboards. By generating synthetic questions for each dashboard and embedding them using the same model as user queries, this approach ensures that dashboards can be discovered even when there's little or no keyword overlap—bridging the gap between natural language and structured enterprise content.

Let me know if you'd like to see a diagram for this flow or an internal engineering summary version.



Here is a well-structured and detailed documentation section describing the keyword-based Tableau dashboard search mechanism, based on your code and process:

---

## Keyword-Based Tableau Dashboard Search

This section outlines the implementation of the **keyword-based search system** used to retrieve relevant Tableau dashboards from within CitiGroup’s financial reporting ecosystem. This approach leverages both traditional keyword matching and synonym expansion to semantically align user queries with dashboard content.

### 1. **User Query Preprocessing and Keyword Extraction**

When a user submits a natural language question, the system initiates a multi-step keyword extraction process:

* **LLM-Based Extraction**: The query is passed to a large language model (LLM), prompting it to return a Python list of relevant keywords. These keywords are intended to capture the key financial terms or entities that are likely to appear in Tableau dashboard content.

  ```python
  ## User query: "Show me Q4 revenue for institutional banking"
  ## Keywords: ['Q4', 'revenue', 'institutional banking']
  ```

* **Error Handling**: If keyword extraction fails for any reason, the system gracefully falls back to an empty list, avoiding runtime crashes.

### 2. **Keyword Normalization**

To improve keyword-text matching reliability, keywords are normalized using the function:

```python
insert_space_around_symbols(text: str) -> str
```

This function:

* Temporarily protects numbers with commas or decimal points,
* Adds whitespace around special characters,
* Normalizes whitespace,
* Restores protected numerical formats.

This ensures consistent matching between keywords and document text segments regardless of formatting inconsistencies.

### 3. **Synonym and Abbreviation Expansion**

To boost recall, especially in the finance and banking context, the system optionally augments each keyword with its **top three synonyms, abbreviations, or full forms** using a domain-specific LLM prompt. This includes variants such as:

* 'Q4' → \['Quarter 4', 'Qtr 4', 'Fourth Quarter']
* 'revenue' → \['income', 'sales', 'turnover']

These synonyms are cached using a local dictionary and stored via `pickle` for reuse, reducing redundant LLM calls and improving performance.

### 4. **Matching Keywords to Dashboard Text**

Each keyword and its synonyms are matched against the text content extracted from Tableau dashboard views using fuzzy matching:

* **Fuzzy Matching (partial\_ratio)**: The system applies `fuzz.partial_ratio` (from the `fuzzywuzzy` library) to compute similarity scores between the normalized keyword/synonym and text segments from each dashboard.
* **Thresholding**: Only matches exceeding a configurable threshold (default: 85) are considered relevant.
* **Scoring**: Matched entries are stored along with their score, the original keyword, the matched synonym, and the matched document text.

### 5. **Scoring and Aggregation**

After all keyword matches are processed, the following steps are executed:

* **Deduplication**: For each (keyword, document) pair, only the highest scoring match is retained.
* **Aggregation**: The system groups results by document (`doc`) and:

  * Aggregates all matched keywords and synonyms into lists,
  * Sums the individual match scores into a total relevance score.

### 6. **Filtering and Ranking**

The results are then:

* **Filtered**: Only documents where the total score exceeds `len(keywords) * 70` are retained.
* **Ranked**: Documents are sorted by total score in descending order.
* **Joined with Metadata**: Dashboard attributes such as `view name`, `summary`, and `URL` are merged from the metadata index (`view_text_attributes`).
* **Deduplicated by View ID**: Ensures that each Tableau view appears only once in the final results.

### 7. **Final Output**

The final result is returned in two parts:

* `records`: A concise list of top 5 dashboards (name, URL, and summary) ready for user display.
* `result`: A full dataframe including all relevant metadata, keywords, synonyms, match scores, and the image path to the dashboard.

---

## Summary

This keyword-based search module provides an efficient and semantically rich way to query Tableau dashboards using natural language. By combining LLM-powered keyword extraction and synonym generation with traditional keyword matching and fuzzy search, it strikes a balance between **precision** and **recall**, ensuring relevant dashboards are surfaced even with varied terminology and phrasing.

Let me know if you'd like this written in a more technical format (e.g. for internal engineering docs), or with a visual flowchart.


Here's a detailed section you can include in your project documentation under **“Tableau View Image Processing Using Vision Model of LLM”**:

---

## Tableau View Image Processing Using Vision Model of LLM

To enhance the discoverability and semantic indexing of financial dashboards built in Tableau at CitiGroup, we implemented an image processing pipeline using a Vision-Language model (VLM). This module automatically generates textual summaries of Tableau view screenshots, allowing users to search and retrieve dashboards based on visual content and context. This capability is essential when dashboard metadata is sparse, inconsistent, or missing.

### Objective

The primary objective is to extract meaningful semantic summaries from Tableau view images (screenshots of dashboards) using a Large Language Model with vision capabilities. These summaries serve as enriched metadata to power semantic search, LLM-assisted querying, and view recommendation systems.

---

### Implementation Details

#### 1. **Architecture Overview**

The image processing component is a standalone module integrated into the main AI dashboard search system. It leverages an OpenAI-compatible Vision model, wrapped inside a callable API to generate human-readable summaries of the dashboard screenshots.

#### 2. **Function Overview**

We use the `generate_with_image` function, which takes in a prompt and the path to a screenshot image, sends a vision query to the model, and receives a concise and context-aware summary.

##### Function Signature:

```python
def generate_with_image(self, prompt: str, image_path: str, stop: Union[str, None, List[str]] = None, use_case: str = None, **kwargs) -> str:
```

##### Key Steps:

* **Token Management**:

  * Uses `R2D2Env.token_roller` to securely fetch API tokens for authentication.

* **Image Encoding**:

  * Converts the image at `image_path` into a base64-encoded PNG format using `self.encode_image(image_path)`.

* **Payload Construction**:

  * A `content` list is constructed with both text and image modalities:

    ```json
    [
      {"type": "text", "text": prompt},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..." }}
    ]
    ```
  * This hybrid prompt instructs the LLM to describe the content of the dashboard.

* **OpenAI Chat API Call**:

  * Sends the multimodal prompt to the LLM endpoint using `client.chat.completions.create()`.
  * Parameters include:

    * `model=self.model_name`
    * `temperature=self.temperature`
    * `max_tokens=10000` (for verbose summaries)

* **Response Parsing**:

  * Extracts the natural language description from `response.choices[0].message.content`.

##### Example Prompt:

```python
prompt = "Please describe the content and layout of this Tableau financial dashboard in a detailed summary."
```

#### 3. **Output Example**

Example output from the Vision model:

```text
The image presents a comprehensive financial dashboard, titled "VAR Dashboard", which provides an in-depth analysis of various financial metrics across different quarters. The dashboard is organized into columns representing different quarters (Q1 to Q4) and rows categorizing various financial accounts, including assets, liabilities, and equity. Each cell contains specific data points such as actual values, constants, and variances, enabling a detailed examination of financial trends and performance over time.
```

#### 4. **Benefits**

* **Improved Search Indexing**:

  * Each dashboard view receives a rich, text-based summary for use in vector and keyword search indexes.

* **Contextual Understanding**:

  * Even dashboards with cryptic names or missing metadata can be discovered based on their visual layout and content.

* **Enhanced User Experience**:

  * Summaries are used in UI previews and autocomplete suggestions when querying dashboards using natural language.

---

### Operational Considerations

* **Performance**:

  * Image processing is conducted asynchronously and cached. Summaries are persisted in the metadata database under fields like `view_summary`.

* **Security**:

  * All API communications are SSL-encrypted using `R2D2Env.ssl_cert_file`.

* **Scalability**:

  * The vision-based processing is designed to run in batch mode to pre-process dashboards and during user queries for on-demand processing.

---

### Future Enhancements

* Add OCR-based extraction to identify text within the dashboard that can complement the vision-based summary.
* Fine-tune prompt templates to generate summaries for different use cases: financial review, compliance checks, executive summaries, etc.
* Use visual embeddings for similarity-based dashboard clustering.

---

Let me know if you'd like a diagram of the flow, or integration details with vector search or keyword indexing.



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
