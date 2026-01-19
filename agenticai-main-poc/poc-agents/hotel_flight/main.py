from langchain_core.messages import HumanMessage
from agents import app

# def run_workflow(query: str):
#     inputs = {"messages": [HumanMessage(content=query)]}
    
#     # Using stream_mode="values" to see the results
#     for event in app.stream(inputs, stream_mode="values"):
#         # This will print every message as it is added to the state
#         message = event["messages"][-1]
#         if message.type != "human": # Skip printing the question again
#             message.pretty_print()

# def main():
#     print("--- Hotel Request ---")
#     # run_workflow("I want to book a hotel in Paris")
#     run_workflow("I want to book a flight to Canada")


def run_workflow(query: str):
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # We use 'updates' mode to clearly see which node is executing
    print(f"\n--- Starting Sequential Workflow for: '{query}' ---")
    
    for chunk in app.stream(inputs, stream_mode="updates"):
        for node_name, state_update in chunk.items():
            print(f"\n[NODE COMPLETED: {node_name}]")
            
            # Print the new messages added by this specific node
            if "messages" in state_update:
                for msg in state_update["messages"]:
                    msg.pretty_print()

def main():
    # Example: This will go to Flight Agent FIRST, then Hotel Agent
    run_workflow("I'm planning a trip to Tokyo.")

if __name__ == "__main__":
    main()
