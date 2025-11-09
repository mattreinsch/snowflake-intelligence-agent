from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import os

def cortex_agent_instruct(prompt):
    """Simulates calling the Cortex Agent's instruct function."""
    print(f"Cortex Agent Instruct Prompt: {prompt}")
    if "at risk" in prompt and "PO12345" in prompt:
        plan = [
            {'step': '1', 'action': 'find_structured_data', 'parameters': {'po_number': 'PO12345'}},
            {'step': '2', 'action': 'find_unstructured_data', 'parameters': {'po_number': 'PO12345'}},
            {'step': '3', 'action': 'calculate_risk', 'parameters': {}},
            {'step': '4', 'action': 'notify_channel', 'parameters': {'channel': '#supply-chain-alerts'}}
        ]
        print(f"Generated Plan: {plan}")
        return {"plan": plan}
    return {"plan": []}

def cortex_agent_query_unstructured(doc_id):
    """Simulates querying a single unstructured document from a Snowflake stage."""
    print(f"Querying unstructured document: {doc_id} from stage...")
    if doc_id == "PO12345":
        return {"total_value": 1000.00}
    return {"error": "Document not found"}

class SlackNotifier:
    def send_notification(self, message):
        print("Simulating sending message to Slack:")
        print(message)

class SupplyChainAgent:
    def __init__(self, session: Session, database: str, schema: str):
        self.session = session
        self.structured_data_df = self.session.table(f'\"{database}\".\"{schema}\".\"SHIPMENTS\"')
        self.notifier = SlackNotifier()

    def find_structured_data(self, po_number):
        print(f"Executing action: find_structured_data with params: {{'po_number': '{po_number}'}}")
        result_df = self.structured_data_df.filter(col("PO_NUMBER") == po_number)
        pandas_df = result_df.to_pandas()
        print("Found structured data:")
        print(pandas_df.to_string())
        return pandas_df

    def find_unstructured_data(self, po_number):
        print(f"Executing action: find_unstructured_data with params: {{'po_number': '{po_number}'}}")
        result = cortex_agent_query_unstructured(po_number)
        print(f"Found unstructured data: {result}")
        return result

    def calculate_risk(self, structured_data, unstructured_data):
        print("Executing action: calculate_risk")
        total_value = unstructured_data.get('total_value', 0)
        risk_assessment = "Low Risk"
        if not structured_data.empty:
            shipment_status = structured_data.iloc[0]['STATUS']
            if shipment_status == 'Delayed' and total_value > 0:
                risk_assessment = f"High Risk: Shipment for PO is delayed. Total value at risk: ${total_value}"
        print(f"Risk Assessment: {risk_assessment}")
        return risk_assessment

    def notify_channel(self, risk_assessment, channel):
        print(f"Executing action: notify_channel with params: {{'channel': '{channel}'}}")
        self.notifier.send_notification(f"Automated Alert: {risk_assessment}")

    def run(self, query):
        plan_response = cortex_agent_instruct(query)
        plan = plan_response.get("plan", [])
        if not plan: return

        results = {}
        for step in plan:
            action = step["action"]
            params = step["parameters"]
            if action == "find_structured_data":
                results['structured_data'] = self.find_structured_data(params['po_number'])
            elif action == "find_unstructured_data":
                results['unstructured_data'] = self.find_unstructured_data(params['po_number'])
            elif action == "calculate_risk":
                results['risk_assessment'] = self.calculate_risk(results.get('structured_data'), results.get('unstructured_data'))
            elif action == "notify_channel":
                self.notify_channel(results.get('risk_assessment'), params['channel'])