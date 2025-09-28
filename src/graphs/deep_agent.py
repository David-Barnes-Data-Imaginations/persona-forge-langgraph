from IPython.display import Image, display
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from utils import format_messages
from langgraph.graph.state import CompiledStateGraph
from langchain_ollama import ChatOllama
from IPython.display import JSON
from langchain_core.messages import messages_to_dict
from typing import Annotated, Literal, NotRequired
from typing_extensions import TypedDict
from datetime import datetime

from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from ..tools.file_tools import ls, read_file, write_file
from ..tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from ..tools.todo_tools import write_todos, read_todos
from ..tools.research_tools import tavily_search, think_tool, get_today_str
from ..tools.task_tool import _create_task_tool

from ..agent_utils.state import DeepAgentState, Todo
from ..agent_utils.deep_utils import show_prompt, stream_agent
from ..prompts.deep_prompts import (
    WRITE_TODOS_DESCRIPTION,
    ARCHITECT_INSTRUCTIONS,
    RESEARCH_OVERSEER_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
)

from langgraph.prebuilt.chat_agent_executor import AgentState

from ..io_py.edge.config import (
    LLMConfigArchitect,
    LLMConfigPeon,
    LLMConfigOverseer,
    LLMConfigScribe,
    LLMConfigSmolScribe,
)

from ..prompts.deep_prompts import (
    LS_DESCRIPTION,
    READ_FILE_DESCRIPTION,
    WRITE_FILE_DESCRIPTION,
)

# Create agent using create_react_agent directly

SYSTEM_PROMPT = "You are a helpful AI agent that can use tools to assist with tasks. Use the provided tools to answer user queries."

# Tools
sub_agent_tools = [tavily_search, think_tool]
built_in_tools = [ls, read_file, write_file, write_todos, read_todos, think_tool]

# Set limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Create task tool to delegate tasks to sub-agents
task_tool = _create_task_tool(
    sub_agent_tools,
    [research_sub_agent],
    LLMConfigSmolScribe.model_name,
    DeepAgentState,
)
delegation_tools = [task_tool]
all_tools = (
    sub_agent_tools + built_in_tools + delegation_tools
)  # search available to main agent for trivial cases


# The architect is the main deep agent to lead the overseers, peons and scribes
# One agent to rule them all, one agent to find them, one agent to bring them all and in the darkness bind them.
def get_new_deep_agent(
    config, short_term_memory, long_term_memory
) -> CompiledStateGraph:

    from langgraph.prebuilt import create_react_agent
    from langchain_ollama import ChatOllama

    model = ChatOllama(
        model=LLMConfigArchitect.model_name,
        temperature=LLMConfigArchitect.temperature,
        reasoning=LLMConfigArchitect.reasoning,
    )

    tools = all_tools

    deep_agent = create_react_agent(
        model,
        tools,
        prompt=ARCHITECT_INSTRUCTIONS,
        checkpointer=short_term_memory,
        store=long_term_memory,
        state_schema=AgentState,
    ).with_config(
        {"recursion_limit": 50}
    )  # recursion_limit limits the number of steps the agent will run

    return deep_agent


"""Sub Agents for the Research workflow"""
peon_model = ChatOllama(
    model=LLMConfigPeon.model_name,
    temperature=LLMConfigPeon.temperature,
    reasoning=LLMConfigPeon.reasoning,
)

scribe_model = ChatOllama(
    model=LLMConfigScribe.model_name,
    temperature=LLMConfigScribe.temperature,
    reasoning=LLMConfigScribe.reasoning,
)

overseer_model = ChatOllama(
    model=LLMConfigOverseer.model_name,
    temperature=LLMConfigOverseer.temperature,
    reasoning=LLMConfigOverseer.reasoning,
)

# Create research sub-agent
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCH_OVERSEER_INSTRUCTIONS,
    "tools": [tavily_search],
}

# Create the Task Agent

# Tools
delegation_tools = [task_tool]

# Create agent with
agent = create_react_agent(
    LLMConfigSmolScribe.model_name,
    delegation_tools,
    prompt=SUBAGENT_USAGE_INSTRUCTIONS.format(
        max_concurrent_research_units=max_concurrent_research_units,
        max_researcher_iterations=max_researcher_iterations,
        date=datetime.now().strftime("%a %b %-d, %Y"),
    ),
    state_schema=DeepAgentState,
)

# TODO - create agents: graph_retriever (peon), pub_med_searcher (scribe), reviewer (scribe), psychologist (overseer)
"""State management for deep agents with TODO tracking and virtual file systems.

This module defines the extended agent state structure that supports:
- Task planning and progress tracking through TODO lists
- Context offloading through a virtual file system stored in state
- Efficient state merging with reducer functions
"""


class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows.

    Attributes:
        content: Short, specific description of the task
        status: Current state - pending, in_progress, or completed
    """

    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left, right):
    """Merge two file dictionaries, with right side taking precedence.

    Used as a reducer function for the files field in agent state,
    allowing incremental updates to the virtual file system.

    Args:
        left: Left side dictionary (existing files)
        right: Right side dictionary (new/updated files)

    Returns:
        Merged dictionary with right values overriding left values
    """
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class DeepAgentState(AgentState):
    """Extended agent state that includes task tracking and virtual file system.

    Inherits from LangGraph's AgentState and adds:
    - todos: List of Todo items for task planning and progress tracking
    - files: Virtual file system stored as dict mapping filenames to content
    """

    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]


def print_deep_agent_prompts():
    """Display key prompts used by the deep agent to terminal for debugging."""
    show_prompt(WRITE_TODOS_DESCRIPTION)
    show_prompt(READ_FILE_DESCRIPTION)
    show_prompt(LS_DESCRIPTION)
    show_prompt(WRITE_FILE_DESCRIPTION)
