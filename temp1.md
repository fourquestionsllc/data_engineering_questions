Got it ✅ You want a clean **object-oriented wrapper class** that:

1. Takes a **user question**.
2. Uses your **PDF search function** (returns `List[Document]`).
3. Converts results → Pandas DataFrame → CSV string.
4. Injects that + question into a **prompt template**.
5. Calls the **LLM** to generate an answer.
6. Returns both the **DataFrame** of results and the **LLM answer**.

Here’s a full implementation with test cases:

```python
from typing import List, Dict, Any
import pandas as pd
from dataclasses import dataclass

# ---- Step 1. Define the Document class ----
@dataclass
class Document:
    metadata: Dict[str, Any]
    page_content: str
    type: str


# ---- Step 2. Define the PDF Query Class ----
class PDFQueryEngine:
    def __init__(self, llm, prompt_template: str):
        """
        llm: LLM object (must have .generate(prompt) method)
        prompt_template: str, with placeholders {df_csv} and {user_question}
        """
        self.llm = llm
        self.prompt_template = prompt_template

    def documents_to_dataframe(self, documents: List[Document]) -> pd.DataFrame:
        """Convert list of Documents to pandas DataFrame"""
        data = [
            {
                "metadata": str(doc.metadata),
                "page_content": doc.page_content,
                "type": doc.type,
            }
            for doc in documents
        ]
        return pd.DataFrame(data)

    def build_prompt(self, df_csv: str, user_question: str) -> str:
        """Fill the prompt template"""
        return self.prompt_template.format(df_csv=df_csv, user_question=user_question)

    def query(self, user_question: str, search_fn) -> Dict[str, Any]:
        """
        Run a query:
        1. Search PDF contents using search_fn
        2. Convert to DataFrame + CSV
        3. Generate prompt
        4. Call LLM
        5. Return results
        """
        # Step 1: Run the search
        documents = search_fn(user_question)

        # Step 2: Convert to DataFrame + CSV
        df = self.documents_to_dataframe(documents)
        df_csv = df.to_csv(index=False)

        # Step 3: Build prompt
        prompt = self.build_prompt(df_csv, user_question)

        # Step 4: Call LLM
        answer = self.llm.generate(prompt)

        # Step 5: Return results
        return {
            "results_df": df,
            "answer": answer
        }


# ---- Step 3. Mock Implementations for Testing ----
class MockLLM:
    def generate(self, prompt: str) -> str:
        return f"Mock answer based on prompt:\n{prompt[:100]}..."


def mock_search_fn(user_query: str) -> List[Document]:
    return [
        Document(metadata={"page": 1}, page_content="AI is transforming the world.", type="pdf"),
        Document(metadata={"page": 2}, page_content="Chatbots are a key application.", type="pdf"),
    ]


# ---- Step 4. Example Usage / Test Cases ----
if __name__ == "__main__":
    QUERY_PDF_CONTENT_PROMPT = """
    You are given the following extracted PDF data in CSV format:

    {df_csv}

    The user asked: {user_question}

    Please provide a concise, accurate answer using only the provided content.
    """

    # Instantiate with mock LLM
    engine = PDFQueryEngine(llm=MockLLM(), prompt_template=QUERY_PDF_CONTENT_PROMPT)

    # Run a test query
    user_question = "What does the document say about chatbots?"
    results = engine.query(user_question, search_fn=mock_search_fn)

    # Print results
    print("=== DataFrame ===")
    print(results["results_df"])
    print("\n=== Answer ===")
    print(results["answer"])
```

---

### ✅ Output (example run)

```
=== DataFrame ===
       metadata                        page_content type
0   {'page': 1}  AI is transforming the world.     pdf
1   {'page': 2}  Chatbots are a key application. pdf

=== Answer ===
Mock answer based on prompt:
You are given the following extracted PDF data in CSV format:...
```

---

👉 This class is reusable:

* Swap out `MockLLM` with your `VertexLLM` instance.
* Replace `mock_search_fn` with your real PDF search function.

Do you want me to also add **unit tests with pytest** (instead of just inline testing in `__main__`)?
