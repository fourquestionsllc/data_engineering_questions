**Acceptance Criteria – Financial Query Entity Extraction**

**Overall Description**
The system shall accurately extract six contextual entity types from user queries related to banking and finance. Extracted entities must be normalized into a consistent schema, enabling downstream analytics or data retrieval. The result must contain the identified entity type, raw text span, and standardized value. Partial matches or misclassifications are unacceptable.

---

### **Entity Definitions & Examples**

1. **Managed Segment**
   Definition: Legal or organizational entities managed under Citi, including its major business segments or groups.
   Examples:

   * “Citi Group” → Managed Segment: Citi Group
   * “Citi Institutional Clients Group” → Managed Segment: ICG
   * “Citi Personal Banking” → Managed Segment: Personal Banking
   * “Citibank NA” → Managed Segment: Citibank NA

2. **Geography**
   Definition: Geopolitical regions or countries representing business locations or market focus.
   Examples:

   * “US” → Geography: United States
   * “Middle East” → Geography: Middle East
   * “Europe” → Geography: Europe
   * “India” → Geography: India

3. **Account Line**
   Definition: Financial reporting line items measuring specific business performance metrics.
   Examples:

   * “revenue” → Account Line: Revenue
   * “interest income” → Account Line: Interest Income
   * “net income” → Account Line: Net Income
   * “operating expenses” → Account Line: Operating Expenses

4. **Product**
   Definition: Types of financial products, services, or offerings provided by Citi.
   Examples:

   * “loan” → Product: Loan
   * “credit card” → Product: Credit Card
   * “banking service” → Product: Banking Services
   * “wealth management” → Product: Wealth Management

5. **Scenario**
   Definition: Temporal or analytical perspectives describing the nature of requested data.
   Examples:

   * “outlook” → Scenario: Forecast/Outlook
   * “forecasting” → Scenario: Forecast
   * “actual” → Scenario: Actual
   * “historical” → Scenario: Historical

6. **Fiscal Period**
   Definition: Time-bound financial periods represented by year, quarter, or month.
   Examples:

   * “2025’Q4” → Fiscal Period: 2025-Q4
   * “FY2024” → Fiscal Period: 2024-FY
   * “Q1 2023” → Fiscal Period: 2023-Q1
   * “December 2022” → Fiscal Period: 2022-12

---

### **Use Cases & Expected Results**

1. “Show revenue of Citi Group in 2025’Q4” → {Managed Segment: Citi Group, Account Line: Revenue, Fiscal Period: 2025-Q4}
2. “Forecast net income of Personal Banking for 2024” → {Managed Segment: Personal Banking, Account Line: Net Income, Scenario: Forecast, Fiscal Period: 2024-FY}
3. “Actual operating expenses of Citibank NA in Europe” → {Managed Segment: Citibank NA, Account Line: Operating Expenses, Scenario: Actual, Geography: Europe}
4. “Interest income outlook in US” → {Account Line: Interest Income, Scenario: Outlook, Geography: US}
5. “Loan revenue forecast for 2025’Q3” → {Product: Loan, Account Line: Revenue, Scenario: Forecast, Fiscal Period: 2025-Q3}
6. “Banking services net income in India” → {Product: Banking Services, Account Line: Net Income, Geography: India}
7. “Historical wealth management revenue” → {Product: Wealth Management, Scenario: Historical, Account Line: Revenue}
8. “Operating expenses forecast for Citi Institutional Clients Group” → {Managed Segment: ICG, Account Line: Operating Expenses, Scenario: Forecast}
9. “Q2 2024 interest income of Citi Group in Middle East” → {...}
10. “Outlook of credit card revenue for FY2023” → {...}
11. “Historical net income of Citi Group” → {...}
12. “Forecast banking service revenue in Europe” → {...}
13. “Actual revenue of Personal Banking in US” → {...}
14. “December 2022 operating expenses” → {...}
15. “Forecast loan interest income for 2025’Q1” → {...}
16. “Wealth management revenue in India 2023” → {...}

**Acceptance:** Extraction is correct if all entities present are identified with proper type and normalized values.
