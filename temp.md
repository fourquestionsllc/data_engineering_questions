import pandas as pd
import json

# Load Excel file
df = pd.read_excel("test_cases.xlsx")

# Drop completely empty rows (if any)
df = df.dropna(how="all")

# Prepare final JSON structure
records = []

# Iterate through rows
for _, row in df.iterrows():
    jira = str(row.get("jira", "")).strip()
    description = str(row.get("description", "")).strip()
    gremlin_query = str(row.get("gremlin_query_to_prepare_test_data", "")).strip()
    
    # Build the conversation sequence dynamically
    conversation = []
    for i in range(1, 10):  # Up to 10 message pairs just in case
        human_col = f"message_human_{i}"
        ai_col = f"message_ai_{i}"
        
        human_msg = row.get(human_col)
        ai_msg = row.get(ai_col)
        
        if pd.notna(human_msg) and str(human_msg).strip():
            conversation.append({
                "message_type": "human",
                "content": str(human_msg).strip()
            })
        if pd.notna(ai_msg) and str(ai_msg).strip():
            conversation.append({
                "message_type": "ai",
                "content": str(ai_msg).strip()
            })
    
    # Create record for each row
    record = {
        "jira": jira,
        "description": description,
        "gremlin_query_to_prepare_test_data": gremlin_query,
        "conversation": conversation
    }
    
    records.append(record)

# Save to JSON file
with open("test_cases.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("✅ Conversion complete! Output saved to test_cases.json")
