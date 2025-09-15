import os
import re
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
from datetime import datetime

from ..prompts.text_prompts import SYSTEM_PROMPT, CYPHER_PROMPT
from ..utils.text_graph_tools import submit_cypher

# Add LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "cypher-generation"

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


# Create the prompt message from 'src/prompts/text_prompts.py'
assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CYPHER_PROMPT),
        ("placeholder", "{messages}"),
    ]
)

# SIMPLIFIED WORKFLOW - SAME AS YOUR WORKING CSV WORKFLOW
tools = [submit_cypher]
assistant_runnable = assistant_prompt | llm.bind_tools(tools)

builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,  # Use the same simple condition as your working CSV workflow
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
framework_graph = builder.compile()

# Set configuration for recursion limit
graph_config = {
    "recursion_limit": 50,  # Match your working CSV workflow
    "configurable": {}
}

"""
Functions for processing the psychological analysis master file
"""


def extract_analyses_from_master_file():
    """
    Extract individual analyses from the master file and return as chunks.
    """
    master_file = os.path.join(os.getcwd(), "output", "psychological_analysis", "psychological_analysis_master.txt")

    print(f"Debug: Looking for master file at: {master_file}")

    if not os.path.exists(master_file):
        print(f"Master file {master_file} doesn't exist!")
        return []

    with open(master_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Debug: Master file size: {len(content)} characters")
    print(f"Debug: File starts with: {repr(content[:200])}")

    # Split by the entry separators - look for the exact pattern in your file
    entries = re.split(r'={80}\n\n={80}\nANALYSIS ENTRY', content)
    print(f"Debug: Found {len(entries)} entries after split")

    analyses = []
    for i, entry in enumerate(entries):
        print(f"Debug: Processing entry {i}")
        print(f"Debug: Entry starts with: {repr(entry[:100])}")

        if 'Analysis:' in entry:  # This should match your file format
            # Clean up the entry
            entry = entry.strip()

            # Find where "Analysis:" starts
            lines = entry.split('\n')
            analysis_start = -1
            for j, line in enumerate(lines):
                if line.strip() == 'Analysis:':
                    analysis_start = j
                    break

            if analysis_start >= 0:
                # Take everything from "Analysis:" onwards
                analysis_text = '\n'.join(lines[analysis_start:]).strip()
                analyses.append({
                    'entry_number': len(analyses) + 1,
                    'content': analysis_text
                })
                print(f"Debug: Successfully extracted analysis {len(analyses)}")
                print(f"Debug: Analysis preview: {analysis_text[:100]}...")
            else:
                print(f"Debug: Could not find 'Analysis:' line in entry {i}")
                print(f"Debug: Available lines: {[line.strip() for line in lines[:10]]}")

    print(f"Debug: Total analyses extracted: {len(analyses)}")
    return analyses

def process_analysis_to_cypher(analysis: dict) -> dict:
    """
    Process a single analysis through the LangGraph workflow to generate Cypher.

    Args:
        analysis: Dictionary with entry_number and content

    Returns:
        Dictionary with processing results
    """
    try:
        # Create a unique thread_id for each analysis to ensure fresh state
        thread_id = f"analysis_{analysis['entry_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create the prompt for the LLM with the analysis data
        qa_pair_id = f"qa_pair_{str(analysis['entry_number']).zfill(3)}"
        prompt_text = f"""
        Please convert the following psychological analysis to a Cypher query:

        Analysis Entry #{analysis['entry_number']}:
        {analysis['content']}

        IMPORTANT ID STRUCTURE - Use these exact IDs:
        - Client ID: client_001
        - Session ID: session_001
        - QA_Pair ID: {qa_pair_id}

        Remember to call the submit_cypher tool with your generated Cypher query.
        """

        # Initial state with the prompt - create fresh state for each analysis
        initial_state = {
            "messages": [HumanMessage(content=prompt_text)]
        }

        # Update config with unique thread_id for LangSmith tracking
        analysis_config = {
            "recursion_limit": 50,
            "configurable": {
                "thread_id": thread_id,
                "analysis_id": analysis['entry_number']
            }
        }

        # Run the graph
        print(f"Processing analysis #{analysis['entry_number']}...")
        result = framework_graph.invoke(initial_state, config=analysis_config)

        return {
            "analysis_id": analysis['entry_number'],
            "thread_id": thread_id,
            "content": analysis['content'][:200] + "...",  # Truncated for brevity
            "messages_count": len(result.get('messages', [])),
            "status": "success"
        }

    except Exception as e:
        return {
            "analysis_id": analysis['entry_number'],
            "content": analysis['content'][:200] + "...",
            "error": str(e),
            "status": "error"
        }


def batch_process_master_file():
    """
    Process all analyses in the master file and generate Cypher queries.
    """
    analyses = extract_analyses_from_master_file()

    if not analyses:
        return {
            "error": "No analyses found in master file!",
            "status": "failed"
        }

    results = {
        "total_analyses": len(analyses),
        "successful": 0,
        "errors": 0,
        "results": [],
        "status": "completed"
    }

    for analysis in analyses:
        result = process_analysis_to_cypher(analysis)
        results["results"].append(result)

        if result['status'] == 'success':
            results["successful"] += 1
        else:
            results["errors"] += 1

    return results


def process_kg_creation() -> dict:
    """
    Main function to process the master file and create knowledge graph.
    This is what will be called from SentimentSuite.py
    """
    try:
        return batch_process_master_file()
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


if __name__ == "__main__":
    result = process_kg_creation()
    print(result)