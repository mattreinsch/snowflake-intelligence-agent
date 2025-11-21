from snowflake.snowpark import Session
from snowflake.snowpark.functions import col


def cortex_agent_instruct(prompt: str) -> dict:
    """
    Simulates calling a Cortex Agent-style planning function.

    In a real implementation, this would call Snowflake Cortex to create a tool-using plan.
    For the demo query about PO12345, we return a hard-coded, interpretable plan.
    """
    print(f"Cortex Agent Instruct Prompt: {prompt}")
    if "at risk" in prompt and "PO12345" in prompt:
        plan = [
            {"step": "1", "action": "find_structured_data", "parameters": {"po_number": "PO12345"}},
            {"step": "2", "action": "find_unstructured_data", "parameters": {"po_number": "PO12345"}},
            {"step": "3", "action": "calculate_risk", "parameters": {}},
            {"step": "4", "action": "notify_channel", "parameters": {"channel": "#supply-chain-alerts"}},
        ]
        print(f"Generated Plan: {plan}")
        return {"plan": plan}

    # Default: no plan for unknown queries
    print("No matching plan found for this query.")
    return {"plan": []}


def cortex_agent_query_unstructured(po_number: str) -> dict:
    """
    Simulates querying a single unstructured document from a Snowflake stage.

    In a real implementation, this would:
      - Look up a file in a stage (e.g. PDF_DOCUMENTS_STAGE)
      - Parse it via external functions / container services
      - Extract structured fields such as total value

    For PO12345, we return a hard-coded total; otherwise we simulate a missing doc.
    """
    print(f"Querying unstructured document: {po_number} from stage...")
    if po_number == "PO12345":
        return {"total_value": 1000.00}
    return {"error": "Document not found or value not extracted"}


class SlackNotifier:
    """
    Simple Slack notifier abstraction.

    In Snowflake Notebooks we can't make direct HTTP calls, so by default
    this just prints to stdout to simulate a Slack message.
    """

    def send_notification(self, message: str) -> None:
        print("Simulating sending message to Slack:")
        print(message)


class SupplyChainAgent:
    """
    A Snowflake-native agent that:
      - Generates a multi-step plan
      - Queries structured data from SHIPMENTS
      - Simulates unstructured PO lookup
      - Calculates a business risk assessment
      - Sends a notification

    This mirrors the workflow described in:
    “From Query to Action: How I Built a Snowflake Agent That Thinks, Plans, and Acts”
    """

    def __init__(self, session: Session, database: str, schema: str):
        self.session = session
        self.database = database
        self.schema = schema

        full_table_name = f"{self.database}.{self.schema}.SHIPMENTS"
        print(f"Initializing SupplyChainAgent with table: {full_table_name}")
        self.structured_data_df = self.session.table(full_table_name)
        self.notifier = SlackNotifier()

    # -------------------------
    # Tool: Structured Data
    # -------------------------
    def find_structured_data(self, po_number: str):
        """
        Finds structured data for a given purchase order from SHIPMENTS.
        """
        print(f"Executing action: find_structured_data with params: {{'po_number': '{po_number}'}}")
        result_df = self.structured_data_df.filter(col("PO_NUMBER") == po_number)
        pandas_df = result_df.to_pandas()

        print("Found structured data:")
        if pandas_df.empty:
            print("  (no rows found)")
        else:
            print(pandas_df.to_string(index=False))

        return pandas_df

    # -------------------------
    # Tool: Unstructured Data
    # -------------------------
    def find_unstructured_data(self, po_number: str) -> dict:
        """
        Fetches unstructured PO context (simulated).
        """
        print(f"Executing action: find_unstructured_data with params: {{'po_number': '{po_number}'}}")
        result = cortex_agent_query_unstructured(po_number)
        print(f"Found unstructured data: {result}")
        return result

    # -------------------------
    # Tool: Risk Calculation
    # -------------------------
    def calculate_risk(self, structured_data, unstructured_data: dict) -> str:
        """
        Combines structured + unstructured signals into a risk assessment.
        """
        print("Executing action: calculate_risk")

        total_value = 0.0
        if isinstance(unstructured_data, dict):
            total_value = float(unstructured_data.get("total_value", 0.0))

        shipment_status = "Unknown"
        if structured_data is not None and not structured_data.empty:
            shipment_status = structured_data.iloc[0].get("STATUS", "Unknown")

        if shipment_status == "Delayed" and total_value > 0:
            risk_assessment = f"High Risk: Shipment for PO is delayed. Total value at risk: ${total_value:,.2f}"
        else:
            risk_assessment = "Low Risk"

        print(f"Risk Assessment: {risk_assessment}")
        return risk_assessment

    # -------------------------
    # Tool: Notification
    # -------------------------
    def notify_channel(self, risk_assessment: str, channel: str) -> None:
        """
        Sends a notification with the risk assessment (simulated Slack).
        """
        print(f"Executing action: notify_channel with params: {{'channel': '{channel}'}}")
        self.notifier.send_notification(f"[{channel}] Automated Alert: {risk_assessment}")

    # -------------------------
    # Orchestrator
    # -------------------------
    def run(self, query: str) -> dict:
        """
        Runs the full agent workflow:

          1. Ask Cortex (simulated) for a plan
          2. Execute each step (tools) in order
          3. Return all intermediate results in a dictionary
        """
        print(f"--- Running Agent with Query: '{query}' ---")
        plan_response = cortex_agent_instruct(query)
        plan = plan_response.get("plan", [])

        if not plan:
            print("No plan generated; aborting.")
            return {}

        results: dict = {}

        for step in plan:
            action = step.get("action")
            params = step.get("parameters", {})

            if action == "find_structured_data":
                po_number = params.get("po_number")
                results["structured_data"] = self.find_structured_data(po_number)

            elif action == "find_unstructured_data":
                po_number = params.get("po_number")
                results["unstructured_data"] = self.find_unstructured_data(po_number)

            elif action == "calculate_risk":
                structured = results.get("structured_data")
                unstructured = results.get("unstructured_data", {})
                results["risk_assessment"] = self.calculate_risk(structured, unstructured)

            elif action == "notify_channel":
                risk = results.get("risk_assessment", "No risk assessment available.")
                channel = params.get("channel", "#supply-chain-alerts")
                self.notify_channel(risk, channel)

            else:
                print(f"Unknown action: {action}")

        print("--- Agent Run Complete ---")
        return results