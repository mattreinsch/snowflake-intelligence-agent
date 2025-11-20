"""
This is the main entry point for running the Supply Chain Agent.
"""
import os
from agent import SupplyChainAgent

def main():
    """
    Initializes and runs the agent with a sample query.
    """
    # Path to the structured data
    structured_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'structured_data', 'shipments.csv')

    # Initialize the agent
    agent = SupplyChainAgent(structured_data_path=structured_data_path)

    # Define a sample query
    query = "What is the total purchase order value at risk for PO12345?"

    # Run the agent
    agent.run(query)

if __name__ == "__main__":
    main()
