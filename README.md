# 🤖 Snowflake Intelligence Agent

### An AI Agent That Thinks, Plans, and Acts — Inside Snowflake

This repository supports the demo from my article:

📄 **[“From Query to Action: How I Built a Snowflake Agent That Thinks, Plans, and Acts”](https://medium.com/@mattsreinsch/from-query-to-action-how-i-built-a-snowflake-agent-that-thinks-plans-and-acts-227f72b8428e)**

The purpose of this project is to showcase a **Snowflake-native AI agent** capable of executing complex workflows:
* Generating a step-by-step plan.
* Querying structured data.
* Processing unstructured documents.
* Synthesizing insights.
* Executing an action.

**All operations happen inside Snowflake using Snowpark, stages, and Cortex.**

---

## 🚀 Demo Capabilities

### 🧠 1. Agent Planning
The agent begins by generating a structured plan based on the user request.

**Example Plan Output:**
```json
[
  { "step": "1", "action": "find_structured_data", "parameters": { "po_number": "PO12345" } },
  { "step": "2", "action": "find_unstructured_data", "parameters": { "po_number": "PO12345" } },
  { "step": "3", "action": "calculate_risk", "parameters": {} },
  { "step": "4", "action": "notify_channel", "parameters": { "channel": "#supply-chain-alerts" } }
]
```
This step-based logic ensures interpretability and auditability.

### 📊 2. Structured Data Query
Using Snowpark, the agent reads from a table like `SHIPMENTS`, retrieves current statuses, and identifies high-risk POs (Purchase Orders).

### 📄 3. Unstructured Data Processing
The agent pulls a document from a Snowflake stage (e.g., `PO12345.pdf.txt`), extracts key fields (like total order value) using Cortex, and blends it with the structured data.

### 🔗 4. Insight Fusion
By marrying structured and unstructured sources, the agent arrives at actionable intelligence:
> *“Shipment #12345 is delayed with $1,000 at risk.”*

### 📢 5. Action Execution
Finally, a simulated notification triggers to close the gap between insight and operations:

```text
Automated Alert: High Risk – Shipment for PO12345 is delayed.
Total value at risk: $1,000.
```

---

## 📦 Repository Structure

```text
snowflake-intelligence-agent/
│
├── notebooks/
│   └── supply_chain_agent.ipynb   # Snowflake Notebook demo
│
├── src/
│   ├── agent_core.py              # Core agent logic
│   └── planning.py                # Optional plan generation layer
│
├── sql/
│   ├── setup.sql                  # Creates SHIPMENTS table + sample data
│   └── create_stages.sql          # Uploads or defines stage for unstructured data
│
├── data/
│   └── pdfs/
│       └── PO12345.pdf.txt        # Sample document used in demo
│
├── LICENSE                        # MIT License
└── README.md                      # Project Documentation
```

---

## 🛠️ Setup Guide (Snowflake)

### 1. Run the Setup SQL
Execute the contents of `sql/setup.sql` in a Snowsight Worksheet to create the table and dummy data.

```sql
-- Example content of setup.sql
CREATE OR REPLACE TABLE SHIPMENTS ...;
INSERT INTO SHIPMENTS ...;
```

### 2. Stage Upload
Create the stage for your documents:

```sql
CREATE OR REPLACE STAGE PDF_DOCUMENTS_STAGE;
```

* Upload `data/pdfs/PO12345.pdf.txt` to this stage using the Snowsight UI or SnowSQL.

### 3. Open the Notebook
1.  Import `notebooks/supply_chain_agent.ipynb` into Snowflake Notebooks.
2.  Update the `YOUR_DATABASE` and `YOUR_SCHEMA` variables at the top of the notebook.
3.  Select a warehouse and run all cells.

---

## 🧠 How the Agent Works

The demo illustrates how enterprise agents should behave:

1.  **Plan → Execute → Act**
2.  **Combine** structured & unstructured data
3.  **Fully governed** within Snowflake
4.  **Explainable, auditable, production-ready**

**Ideal for use cases in:**
* Supply chain / logistics
* Procurement risk detection
* Document-driven analytics
* Operational automation

---

## 🤝 Contributing & Extensions

You’re welcome to enhance this demo! Here are some ideas:

* Swap the simulated Cortex plan with `ai_instruct()`.
* Integrate real Slack/Teams notifications via External Access Policies.
* Expand to multi-tenant or multi-schema architectures.
* Add change detection (CDC) or SCD.
* Build a Streamlit dashboard to visualize agent metrics.

Feel free to fork, submit PRs, or open issues.

---

## 📬 Stay Connected

* 🔗 **[LinkedIn](https://www.linkedin.com/in/mattreinsch)**
* ✍️ **[Medium](https://medium.com/@mattsreinsch)**
* 📰 **[Newsletter (Data Drift)](https://mattreinsch.github.io/DataDrift)**
* 🌐 **[Website](https://mattreinsch.com)**

**⭐ Support:**
If you find this project useful:
* **Star** the repository.
* **Fork** it and build your use case.
* **Share** a project image on LinkedIn and tag me — I’d love to see what you create!
