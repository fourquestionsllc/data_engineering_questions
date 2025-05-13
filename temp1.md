## Project Overview & Use Cases

The AI tool developed for Citigroup enables users to efficiently search and explore Tableau financial dashboards using multiple search methods, including keyword search, semantic search, and database search. This tool leverages LLMs (Large Language Models) to interpret user questions, identify relevant Tableau views, and deliver precise, contextually accurate responses.

Typical user questions include:

* "Show me the 2024 financial outlook for CBNA."
* "Bring me the dashboards for internal sales and external sales in 2023."
* "I want to see the 2024 plan of expense by businesses."
* "Give me the dashboards of ROA and ROE of 2024."
* "I am interested in the expenses by segments in 4Q23."
* "I am looking for views with tables with P1 to P9 metrics."

The tool supports the following search methods:

* **Keyword Search:** Extracts keywords from user questions and matches them against the text content of Tableau dashboards to locate the most relevant views.
* **Semantic Search:** Converts user questions into embedding vectors and searches against pre-computed embeddings of Tableau view summaries for a more nuanced match.
* **Database Search:** Translates user questions into SQL queries to retrieve structured data from the Tableau metadata database, including views, workbooks, data sources, and revisions.

---

## Business Objectives

The primary goals of this AI tool are to:

* Enhance the speed and accuracy of data retrieval from Tableau financial dashboards.
* Improve user experience by allowing natural language interactions with financial data.
* Reduce dependency on manual dashboard navigation and search.
* Support business decision-making with quick access to critical financial insights.
* Enable flexible and context-aware responses to a wide range of financial data queries.

---

## User Personas & Scenarios

This tool is designed for a diverse set of users within Citigroup, including:

* **Financial Analysts:** Looking to quickly access and analyze specific financial metrics and reports.
* **Business Executives:** Seeking high-level overviews and financial insights for strategic decision-making.
* **Operations Managers:** Interested in operational efficiency metrics and financial health indicators.
* **Data Scientists:** Validating data integrity and extracting insights for further analysis.
* **Internal Auditors:** Quickly retrieving compliance and performance-related financial views.

Example use cases:

* A financial analyst searches for year-over-year revenue growth trends.
* An executive asks for the latest ROA and ROE metrics.
* An operations manager explores expense distributions by business units.

---

## Key Features & Functionalities

Key capabilities of the AI tool include:

* **Natural Language Processing:** Understands diverse financial terminology and phrases.
* **Keyword Search:** Rapid matching of keywords with dashboard content.
* **Semantic Search:** Deep understanding through vector-based similarity matching.
* **Database Search:** Structured data retrieval using auto-generated SQL queries.
* **Multi-Mode Response Generation:** Combines results from various search modes for comprehensive answers.
* **Context-Aware Responses:** Adjusts responses based on question context for higher accuracy.
* **Scalable Architecture:** Handles large volumes of queries efficiently.
* **Secure Data Handling:** Ensures compliance with Citigroup’s security policies.
* **Real-Time Performance:** Delivers insights quickly, even for complex queries.
