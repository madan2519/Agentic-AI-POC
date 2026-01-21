from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from tools import book_hotel, book_flight

# 1. Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Create specialized worker agents
# We give them clear names so the supervisor knows who is who
hotel_agent = create_react_agent(
    llm, 
    tools=[book_hotel], 
    name="hotel_specialist",
    prompt="You are a hotel specialist. Focus only on finding and booking accommodations."
)

flight_agent = create_react_agent(
    llm, 
    tools=[book_flight], 
    name="flight_specialist",
    prompt="You are a flight specialist. Focus only on airline bookings and travel routes."
)

# 4. Create the Supervisor Workflow
# This replaces your StateGraph and Router logic entirely
workflow = create_supervisor(
    [hotel_agent, flight_agent],
    model=llm,
    prompt=(
        "You are a travel supervisor. Based on the user's request, delegate work "
        "to either the hotel_specialist or the flight_specialist. "
        "If a user wants to 'stay' or needs 'accommodation', use the hotel_specialist. "
        "If they want to 'fly' or 'travel', use the flight_specialist. "

        "IMPORTANT:\n"
        "- After the specialist completes their task, read their final answer.\n"
        "- Return the specialist's final answer verbatim to the user.\n"
        "- Only say FINISH if there is nothing useful to return."
    )
)

# 5. Compile the app
app = workflow.compile()

from langchain_core.messages import HumanMessage

def run_travel_query(query: str):
    print(f"\n--- Processing Query: {query} ---")

    for event in app.stream(
        {"messages": [HumanMessage(content=query)]},
        stream_mode="updates"
    ):
        # Each event contains the full message history at that point
        for msg in event["messages"]:

            # ✅ Print every AI message returned by any LLM
            if msg.type == "ai":
                # print("\n[AI MESSAGE TRACE]")
                msg.pretty_print()

if __name__ == "__main__":
    # Test with natural language (no hardcoded 'hotel' keyword needed)
    run_travel_query("Find me a hotel in Paris for next weekend.")
    # run_travel_query("I need a nice place to stay in Rome and a way to get there from London.")