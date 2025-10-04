from re import sub
from IPython.display import Image, display
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from regex import P
from ..agent_utils.deep_utils import format_messages
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

from ..tools.file_tools import ls, read_file, write_file, save_to_disk
from ..tools.deep_rag_tools import (
    DEEP_PERSONA_FORGE_TOOLS,
)  # Use wrappers that save to files
from ..tools.todo_tools import write_todos, read_todos
from ..tools.research_tools import (
    tavily_search,
    pubmed_search,
    think_tool,
    get_today_str,
)
from ..tools.task_tool import _create_task_tool

from ..agent_utils.state import DeepAgentState, Todo
from ..prompts.deep_prompts import (
    ARCHITECT_INSTRUCTIONS,
    SUBAGENT_INSTRUCTIONS,
    # READ_ASSISTANT_INSTRUCTIONS,
)

from langgraph.prebuilt.chat_agent_executor import AgentState

from ..io_py.edge.config import (
    LLMConfigArchitect,
    LLMConfigPeon,
    LLMConfigOverseer,
    LLMConfigScribe,
)


"""Sub Agent models for the workflow
- The reason for different models is to test parrallelism and specialisation of tasks
- Peon (aka 'Alt') - Used as a parrallel agent to the scribe for diversity of answers
- Scribe/SmolScribe - research, web searching, summarization (RUNS ON MINI-ITX)
- Overseer - high level tasks, planning, analysis, report writing

"""
# Local models (main PC)
alt_model = ChatOllama(
    model=LLMConfigPeon.model_name,  # aka 'alt'
    temperature=LLMConfigPeon.temperature,
    reasoning=LLMConfigPeon.reasoning,
    num_predict=LLMConfigPeon.max_tokens,
)

overseer_model = ChatOllama(
    model=LLMConfigOverseer.model_name,
    temperature=LLMConfigOverseer.temperature,
    reasoning=LLMConfigOverseer.reasoning,
    num_predict=LLMConfigOverseer.max_tokens,
)

# Remote model (mini-itx) - setup SSH tunnel first
if LLMConfigScribe.use_remote:
    from ..io_py.edge.ssh_tunnel import ensure_mini_tunnel

    ensure_mini_tunnel()  # Start SSH tunnel to mini-itx

    scribe_model = ChatOllama(
        model=LLMConfigScribe.model_name,  # aka 'Scribe'
        temperature=LLMConfigScribe.temperature,
        reasoning=LLMConfigScribe.reasoning,
        num_predict=LLMConfigScribe.max_tokens,
        base_url=f"http://localhost:{LLMConfigScribe.remote_port}",  # Use tunneled port
    )
    print(
        f"✅ Scribe model configured for remote execution on {LLMConfigScribe.remote_host}"
    )
else:
    scribe_model = ChatOllama(
        model=LLMConfigScribe.model_name,
        temperature=LLMConfigScribe.temperature,
        reasoning=LLMConfigScribe.reasoning,
        num_predict=LLMConfigScribe.max_tokens,
    )

# Online models for testing (commented out - not currently used)
# anthropic_model = init_chat_model(
#     model="anthropic:claude-3-5-sonnet-20241022", temperature=0.0
# )
# openai_model = init_chat_model(model="openai:gpt-4o-mini", temperature=0.0)
#
# # Use ChatGoogleGenerativeAI directly instead of init_chat_model
# from langchain_google_genai import ChatGoogleGenerativeAI
#
# gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.0)

"""*************************** Workflow*************************************************
The main deep agent is the architect. Oversight of report and writes the plan.
The Architect has three direct reports: 'Graph Agent', 'Reporting Agent' and 'Research Agent.
The 'Graph Agent' is called using queries such as:
- "Find me the extreme values in the Graph"
The The Graph Agent then fires two 'Graph Assistant' to run seperate or parralel queries
The graph Assistants extract the data and writes the psychological analysis for the pair to a file. 
Graph Agent checks and loops until analysis complete, then sends the draft analysis to the Architect.
The Architect sends the file to the 'Report Writer Agent', who drafts a 'Therapy SOAP note'.
Once Report Writer is finished, the Architect reviews and edits.
The Architect calls the Research Agent to gather additional information or recent studies from Pubmed API and/or Tavily Web Search.
The Research Agent fires two 'Research Assistants' to run seperate or parralel queries
The Research Agent writes the psychological research to the file. 
Research Agent checks and loops until analysis complete,
The Architects final report is then saved to a file (it has terminal access with 'Human in the loop' for approval).

Return calls are made via the 'Think' tool, which allows the agent to call other tools or agents as needed.

<Architect>
├─ <research sub-agent> (overseer)
│  │  ├─<assistant research sub-agent> (peon)
├─ <Graph sub-agent(overseer)>
│  │  ├─ <Graph Analyzer sub-agent(peon)>
├─ <Report Writer sub-agent (scribe)>

"""

# *************************** Tools and Sub-agents**************************************
# Set limits
max_concurrent_agent_units = 5
max_researcher_iterations = 6
max_concurrent_local_agents = 3
max_concurrent_online_agents = 3

# Core Admin Tools
built_in_tools = [
    ls,
    read_file,
    write_file,
    write_todos,
    read_todos,
    think_tool,
    save_to_disk,
]
# create the tools to delegate to sub-agents
sub_agent_tools = [
    tavily_search,
    pubmed_search,
] + built_in_tools  # PubMed for academic research, Tavily for general web search

assistant_tools = DEEP_PERSONA_FORGE_TOOLS + sub_agent_tools

# *************************** Create Sub-Agents & Assign Tools****************************


# create the research sub-agent
assistant = {
    "name": "assistant",
    "description": "Delegate a task to the assistant. Provide this sub-agent with a description of your queries to delegate.",
    "prompt": SUBAGENT_INSTRUCTIONS,
    "tools": [t.name for t in assistant_tools],
}

# Create task tool for the Architect to delegate tasks to sub-agents

# Research Tasks - Each with unique name
first_assistant_task_tool = _create_task_tool(
    assistant_tools,
    [assistant],
    scribe_model,
    DeepAgentState,
    tool_name="delegate_to_write_assistant",
)

second_assistant_task_tool = _create_task_tool(
    assistant_tools,
    [assistant],
    overseer_model,
    DeepAgentState,
    tool_name="delegate_to_graph_assistant",
)

third_assistant_task_tool = _create_task_tool(
    assistant_tools,
    [assistant],
    alt_model,
    DeepAgentState,
    tool_name="delegate_to_flex_assistant",
)

# *************************** Create Sub-Agents tools**********************************
delegation_tools = [
    first_assistant_task_tool,
    second_assistant_task_tool,
    third_assistant_task_tool,
]

# Give architect visibility into all tools (following langchain academy pattern)
# This allows the architect to understand what assistants can do when delegating
all_architect_tools = DEEP_PERSONA_FORGE_TOOLS + sub_agent_tools + delegation_tools


# *************************** Create The Architect  ************************************
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
        num_predict=LLMConfigArchitect.max_tokens,  # Ollama parameter for max output tokens
    )

    tools = all_architect_tools

    deep_agent = create_react_agent(
        model,
        tools,
        prompt=ARCHITECT_INSTRUCTIONS,
        checkpointer=short_term_memory,
        store=long_term_memory,
        state_schema=DeepAgentState,
    ).with_config(
        {
            "recursion_limit": 50
        }  # 150 because the 'thinking' is counting as steps and taking them all up
    )  # recursion_limit limits the number of steps the agent will run

    return deep_agent
