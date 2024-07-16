from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, FunctionMessage, BaseMessage, SystemMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import TypedDict, Annotated, Sequence
import operator
import json


SYSTEM_PROMPT = "You are playing the role of a knowledgeable and friendly dad. Your goal is to provide helpful and reliable advice on various topics, just like a wise father would."

# tools
tools = [TavilySearchResults(max_results=1)]
tool_executor = ToolExecutor(tools)

# model
model = ChatOpenAI(temperature=0, streaming=True)
functions = [convert_to_openai_function(t) for t in tools]
model = model.bind_functions(functions)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Define functions
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
    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=query)
        ]
    }
    result = app.invoke(initial_state)
    return result
