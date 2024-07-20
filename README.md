# Ask Dad

Ask Dad is an AI-powered assistant application designed to provide users with reliable advice and answers on various topics.

## Goal
Provide an AI father figure that keeps up with the new and knows "everything".

## Example Query
**Question:** "How do I fix the hole in the wall?"  
**Answer from agent 1 (Research):**  
1. **Title:** [8 Frequently Asked Questions About Drywall Repair - Hole In The Wall](https://www.holeinthewall.com/8-frequently-asked-questions-about-drywall-repair/)
2. **Title:** [How To Fix a Hole in the Wall - This Old House](https://www.thisoldhouse.com/walls/21015080/how-to-fix-a-hole-in-the-wall)

**Answer agent 2 (Summarize):**  
- There are 8 questions to ask before you repair a drywall... Here is a general guide (sources).

**Answer agent 2 (Follow-up Question):**  
- ...

## Task Handling
The agents handle their tasks effectively by:
- Processing user queries using the OpenAI chat model.
- Invoking the Tavily search tool to augment the information retrieval process.

## Tech Stack

### Frontend
- React
- MUI
- Axios
- AWS S3

### Backend
- Python
- Django
- AWS EC2
- LangGraph: Utilize the LangGraph framework to build and design the workflow of the AI agents.
   - Useful resource: [AI Agentic course](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/)
- Tavily API: Employ the Tavily API to enhance the agents’ reliability, incorporating the idea of Retrieval-Augmented Generation (RAG) into your application.

## Workflow Breakdown

### Receiving a Query
The frontend sends a user query to the backend via a POST request.

### Processing the Query
1. The Django view (`query_view`) receives the query and calls the `handle_query` function.
2. The `handle_query` function sets up the initial state and invokes the LangGraph workflow.

### LangGraph Workflow
- **Model Agent (`call_model`)**: The OpenAI chat model processes the query and decides on the next action.
- **Tool Agent (`call_tool`)**: If the model decides to invoke a tool, the Tavily search tool is called to retrieve relevant information.
- **Looping and Decision Making**: The workflow loops between the model and tool agents until a stopping condition is met (defined by `should_continue`).
- **Returning the Response**: The final processed result is returned as a JSON response to the frontend.