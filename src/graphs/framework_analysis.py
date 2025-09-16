import pandas as pd
from typing import Annotated, Optional
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition

from ..prompts.text_prompts import SYSTEM_PROMPT
from ..utils.text_graph_tools import submit_analysis

# LLM
llm = ChatOllama(
    model="gpt-oss:20b",
    temperature=0.1,
    # other params...
)
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please retry, make sure not to include any erroneous characters as that can trip the error. Thanks!",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }
def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{messages}"),
    ]
)


tools = [submit_analysis]
assistant_runnable = assistant_prompt | llm.bind_tools(tools)

builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
framework_graph = builder.compile()

# Set configuration for recursion limit
graph_config = {
    "recursion_limit": 50,  # Increased from default 25
    "configurable": {}
}

def parse_therapy_csv(csv_content: str) -> list:
    """
    Parse the therapy CSV and extract QA pairs for processing.
    
    Args:
        csv_content: Raw CSV content as string
        
    Returns:
        List of QA pair dictionaries with question, answer, and message_id
    """
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_content))
        
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        
        # Verify required columns
        required_cols = ['Therapist', 'Client', 'message_id']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"CSV must contain columns: {required_cols}")
        
        qa_pairs = []
        for _, row in df.iterrows():
            # Skip rows with missing data
            if pd.isna(row['Therapist']) or pd.isna(row['Client']) or pd.isna(row['message_id']):
                continue
                
            qa_pair = {
                'question': str(row['Therapist']).strip(),
                'answer': str(row['Client']).strip(),
                'message_id': str(row['message_id']).strip()
            }
            qa_pairs.append(qa_pair)
        
        return qa_pairs
    
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")

def process_qa_pair(qa_pair: dict) -> dict:
    """
    Process a single QA pair through the LangGraph workflow.
    
    Args:
        qa_pair: Dictionary with question, answer, message_id
        
    Returns:
        Dictionary with processing results
    """
    try:
        # Create the prompt for the LLM with the QA pair data
        prompt_text = f"""
        Please analyze the following QA pair from a therapy session:
        
        Question: {qa_pair['question']}
        Answer: {qa_pair['answer']}
        Message ID: {qa_pair['message_id']}
        
        Analyze ONLY the Client's answer and return the psychological analysis on its own without the Question and Answer.
        """
        
        # Initial state with the prompt
        initial_state = {
            "messages": [HumanMessage(content=prompt_text)]
        }
        
        # Run the graph with increased recursion limit
        result = framework_graph.invoke(initial_state, config=graph_config)
        
        return {
            "qa_id": qa_pair['message_id'],
            "question": qa_pair['question'],
            "answer": qa_pair['answer'],
            "result": result,
            "status": "success"
        }
    
    except Exception as e:
        return {
            "qa_id": qa_pair['message_id'],
            "question": qa_pair['question'],
            "answer": qa_pair['answer'],
            "error": str(e),
            "status": "error"
        }

def process_therapy_session(csv_content: str) -> dict:
    """
    Process entire therapy session CSV through the LangGraph workflow.
    
    Args:
        csv_content: Raw CSV content as string
        
    Returns:
        Dictionary with processing results and statistics
    """
    try:
        qa_pairs = parse_therapy_csv(csv_content)
        
        results = []
        successful_count = 0
        error_count = 0
        
        for qa_pair in qa_pairs:
            result = process_qa_pair(qa_pair)
            results.append(result)
            
            if result['status'] == 'success':
                successful_count += 1
            else:
                error_count += 1
        
        return {
            "total_pairs": len(qa_pairs),
            "successful": successful_count,
            "errors": error_count,
            "results": results,
            "status": "completed"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }

