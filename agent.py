import os
from typing import Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

search_tool = TavilySearchResults(
    max_results=5,
    tavily_api_key=os.environ.get("TAVILY_API_KEY", "")
)
tools = [search_tool]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).bind_tools(tools)

system_prompt = SystemMessage(content="""
You are a research assistant. When given a topic:
1. Search for it using the search tool
2. Search again for more specific aspects if needed
3. Synthesize everything into a structured report with:
   - Summary
   - Key Findings (bullet points)
   - Sources

Always search at least twice before writing the report.
""")

def agent_node(state: AgentState):
    messages = [system_prompt] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

tool_node = ToolNode(tools)

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()

def run_research_stream(topic: str):
    inputs = {"messages": [HumanMessage(content=f"Research this topic thoroughly: {topic}")]}
    for step in app.stream(inputs, stream_mode="updates"):
        for node_name, update in step.items():
            messages = update.get("messages", [])
            for msg in messages:
                if node_name == "agent":
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            query = tc["args"].get("query", "")
                            yield ("search", f"Searching: {query}")
                    elif hasattr(msg, "content") and msg.content:
                        yield ("report", msg.content)
                elif node_name == "tools":
                    yield ("result", "Search complete, analyzing results...")

def run_research(topic: str):
    result = app.invoke({
        "messages": [HumanMessage(content=f"Research this topic thoroughly: {topic}")]
    })
    return result["messages"][-1].content
