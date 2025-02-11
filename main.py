from fastapi import FastAPI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

app=FastAPI()

# Define the tools for the agent to use
@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


tools = [search]
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()
agent = create_react_agent(model, tools, checkpointer=checkpointer)
print("agent created")
# Use the agent
@app.post("/chat")
async def invoke_agent(input_data: dict):
    final_state = agent.invoke(
        {"messages": input_data["messages"]},
        config={"configurable": {"thread_id": 42}}
    )
    return {"response": final_state["messages"][-1].content}
