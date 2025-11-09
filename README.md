# From Query to Action: A Snowflake AI Agent Demo

This repository contains the code for the "From Query to Action: How I Built a Snowflake Agent That Thinks, Plans, and Acts" article. It demonstrates a Snowflake-native AI agent that can reason, plan, and execute actions by interacting with structured and unstructured data.

## How to Run the Demo in Snowflake

This demo is designed to be run in a Snowflake Notebook.

### 1. Set Up Your Snowflake Environment

Before running the notebook, you need to create the `SHIPMENTS` table in your Snowflake account.

*   Open a new Snowflake worksheet.
*   Copy and paste the content of `setup.sql` into your worksheet and run it. This will create the `SHIPMENTS` table and populate it with sample data.

### 2. Upload Unstructured Data to a Stage

The agent needs access to a PDF document (represented as a text file in this demo).

*   In your Snowflake worksheet, create a stage:
    ```sql
    CREATE OR REPLACE STAGE PDF_DOCUMENTS_STAGE;
    ```
*   Upload the `data/pdfs/PO12345.pdf.txt` file to this stage. You can do this using the Snowsight UI or SnowSQL.

### 3. Run the Snowflake Notebook

*   Open the `notebooks/supply_chain_agent.ipynb` notebook in your Snowflake account.
*   In the notebook, locate the cell where `YOUR_DATABASE` and `YOUR_SCHEMA` are defined. Update these variables with the database and schema where you created the `SHIPMENTS` table.
*   Run all the cells in the notebook to see the agent in action.

## Repository Structure

*   `notebooks/supply_chain_agent.ipynb`: The main Snowflake Notebook that demonstrates the agent's workflow.
*   `src/agent_core.py`: Contains the core logic for the `SupplyChainAgent`.
*   `setup.sql`: SQL script to set up the necessary tables in Snowflake.
*   `data/`: Contains the sample structured and unstructured data used in the demo.

## Conceptual Overview

This demo simulates a sophisticated AI agent using Snowflake's capabilities:

*   **Planning:** The agent first generates a multi-step plan using a simulated call to Snowflake Cortex.
*   **Execution:** It then executes this plan by:
    *   Querying the `SHIPMENTS` table for structured data using Snowpark.
    *   Accessing a document from a Snowflake stage to get unstructured data.
*   **Action:** Finally, it calculates the risk and simulates sending a notification.

This entire process is orchestrated within Snowflake, showcasing how to build powerful, explainable, and governable AI agents.