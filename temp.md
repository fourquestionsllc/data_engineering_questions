Here’s a Python script that reads your `test_cases.xlsx` file and converts it into the desired JSON format, including the `gremlin_query_to_prepare_test_data` field and properly structuring the alternating human/AI messages:

```python
import pandas as pd
import json

def convert_excel_to_json(excel_path: str, output_json_path: str):
    # Read Excel file
    df = pd.read_excel(excel_path)
    
    # Fill NaN values with empty strings to avoid issues
    df = df.fillna("")
    
    # Group by jira and description (since multiple rows can share same Jira)
    grouped = df.groupby(["jira", "description", "gremlin_query_to_prepare_test_data"])
    
    result = []
    
    for (jira, description, gremlin_query), group in grouped:
        conversation = []
        
        # Iterate through each row and collect message pairs
        for _, row in group.iterrows():
            # For each human/AI pair, add entries to the conversation list if non-empty
            if row.get("message_human_1"):
                conversation.append({
                    "message_type": "human",
                    "content": str(row["message_human_1"]).strip()
                })
            if row.get("message_ai_1"):
                conversation.append({
                    "message_type": "ai",
                    "content": str(row["message_ai_1"]).strip()
                })
            if row.get("message_human_2"):
                conversation.append({
                    "message_type": "human",
                    "content": str(row["message_human_2"]).strip()
                })
            if row.get("message_ai_2"):
                conversation.append({
                    "message_type": "ai",
                    "content": str(row["message_ai_2"]).strip()
                })
        
        result.append({
            "jira": jira,
            "description": description,
            "gremlin_query_to_prepare_test_data": gremlin_query,
            "conversation": conversation
        })
    
    # Write to JSON file with pretty formatting
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print(f"✅ JSON saved to {output_json_path}")


# Example usage
if __name__ == "__main__":
    convert_excel_to_json("test_cases.xlsx", "test_cases.json")
```

### ✅ Output Format Example

Given your input, the output JSON will look like this:

```json
[
    {
        "jira": "JHWP-2106",
        "description": "add fuzzy matching for fields and handle multiple matches",
        "gremlin_query_to_prepare_test_data": "",
        "conversation": [
            {
                "message_type": "human",
                "content": "Bring me the document details of a document with file name containing \"L-1285-01-S-23\""
            },
            {
                "message_type": "ai",
                "content": "Here are the details of the document with a file name containing \"L-1285-01-S-23\":\n\nID: L-1285-01-S-23-A ..."
            },
            {
                "message_type": "human",
                "content": "Bring me the details of a document with file name \"L-1285-01-S-23 - Label.pdf\" and title \" L-1285-01-S-23 REV A\"."
            },
            {
                "message_type": "ai",
                "content": "Here are the details of the document with the specified file name \"L-1285-01-S-23 - Label.pdf\" and title ..."
            }
        ]
    },
    ...
]
```

Would you like me to modify it so that multiple JIRAs (e.g., same ticket but different scenarios) get merged under a single `jira` entry with combined conversations?
