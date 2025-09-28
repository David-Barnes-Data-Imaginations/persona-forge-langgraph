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

from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from ..agent_utils.state import DeepAgentState, Todo
from ..agent_utils.deep_utils import show_prompt
from ..prompts.deep_prompts import WRITE_TODOS_DESCRIPTION

from langgraph.prebuilt.chat_agent_executor import AgentState

from ..io_py.edge.config import (
    LLMConfigVoice,
)  # this just contains basic info to see up gpt-oss
from ..tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from ..prompts.text_prompts import VOICE_SYSTEM_PROMPT
from ..tools.research_tools import RESEARCH_TOOLS

# Create agent using create_react_agent directly

SYSTEM_PROMPT = "You are a helpful AI agent that can use tools to assist with tasks. Use the provided tools to answer user queries."

tools = []


def get_new_deep_agent(
    config, short_term_memory, long_term_memory
) -> CompiledStateGraph:

    from langgraph.prebuilt import create_react_agent
    from langchain_ollama import ChatOllama

    model = ChatOllama(
        model=LLMConfigVoice.model_name,
        temperature=LLMConfigVoice.temperature,
        reasoning=LLMConfigVoice.reasoning,  # keep your config as-is
    )

    tools = PERSONA_FORGE_TOOLS

    deep_agent = create_react_agent(
        model,
        tools,
        prompt=VOICE_SYSTEM_PROMPT,
        checkpointer=short_term_memory,
        store=long_term_memory,
        state_schema=AgentState,
    ).with_config(
        {"recursion_limit": 20}
    )  # recursion_limit limits the number of steps the agent will run

    return deep_agent


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


def print_deep_agent_todos():
    """Prints the todo list to terminal for debugging.
    Format:
     Create and manage structured task lists for tracking progress through complex workflows.                         │
    │                                                                                                                 │
    │  ## When to Use                                                                                                 │
    │  - Multi-step or non-trivial tasks requiring coordination                                                       │
    │  - When user provides multiple tasks or explicitly requests todo list                                           │
    │  - Avoid for single, trivial actions unless directed otherwise                                                  │
    │                                                                                                                 │
    │  ## Structure                                                                                                   │
    │  - Maintain one list containing multiple todo objects (content, status, id)                                     │
    │  - Use clear, actionable content descriptions                                                                   │
    │  - Status must be: pending, in_progress, or completed                                                           │
    │                                                                                                                 │
    │  ## Best Practices                                                                                              │
    │  - Only one in_progress task at a time                                                                          │
    │  - Mark completed immediately when task is fully done                                                           │
    │  - Always send the full updated list when making changes                                                        │
    │  - Prune irrelevant items to keep list focused                                                                  │
    │                                                                                                                 │
    │  ## Progress Updates                                                                                            │
    │  - Call TodoWrite again to change task status or edit content                                                   │
    │  - Reflect real-time progress; don't batch completions                                                          │
    │  - If blocked, keep in_progress and add new task describing blocker                                             │
    │                                                                                                                 │
    │  ## Parameters                                                                                                  │
    │  - todos: List of TODO items with content and status fields                                                     │
    │                                                                                                                 │
    │  ## Returns                                                                                                     │
    │  Updates agent state with new todo list.
    """

    show_prompt(WRITE_TODOS_DESCRIPTION)
