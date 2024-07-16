from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, FunctionMessage
from typing import TypedDict, Annotated, Sequence
import operator
import json

# Define tools
tools = [TavilySearchResults(max_results=1)]
tool_executor = ToolExecutor(tools)

# Define model
model = ChatOpenAI(temperature=0, streaming=True)
functions = [format_tool_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)

# Define agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Define functions for nodes
def should_continue(state):
    last_message = state['messages'][-1]
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

def call_model(state):
    response = model.invoke(state['messages'])
    return {"messages": [response]}

def call_tool(state):
    last_message = state['messages'][-1]
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"])
    )
    response = tool_executor.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    return {"messages": [function_message]}

# Define graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"continue": "action", "end": END})
workflow.add_edge('action', 'agent')
app = workflow.compile()

def handle_query(query):
    inputs = {"messages": [HumanMessage(content=query)]}
    result = app.invoke(inputs)
    return result
