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
from ..tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from ..tools.todo_tools import write_todos, read_todos
from ..tools.research_tools import (
    tavily_search,
    pubmed_search,
    think_tool,
    get_today_str,
)
from ..tools.task_tool import _create_task_tool

from ..agent_utils.state import DeepAgentState, Todo
from ..agent_utils.deep_utils import show_prompt, stream_agent
from ..prompts.deep_prompts import (
    ARCHITECT_INSTRUCTIONS,
    RESEARCH_INSTRUCTIONS,
    GRAPH_INSTRUCTIONS,
    REPORT_INSTRUCTIONS,
    RESEARCH_ASSISTANT_INSTRUCTIONS,
    GRAPH_ASSISTANT_INSTRUCTIONS,
    READ_AGENT_INSTRUCTIONS,
    # READ_ASSISTANT_INSTRUCTIONS,
)

from langgraph.prebuilt.chat_agent_executor import AgentState

from ..io_py.edge.config import (
    LLMConfigArchitect,
    LLMConfigPeon,
    LLMConfigOverseer,
    LLMConfigScribe,
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
)

overseer_model = ChatOllama(
    model=LLMConfigOverseer.model_name,
    temperature=LLMConfigOverseer.temperature,
    reasoning=LLMConfigOverseer.reasoning,
)

# Remote model (mini-itx) - setup SSH tunnel first
if LLMConfigScribe.use_remote:
    from ..io_py.edge.ssh_tunnel import ensure_mini_tunnel

    ensure_mini_tunnel()  # Start SSH tunnel to mini-itx

    scribe_model = ChatOllama(
        model=LLMConfigScribe.model_name,  # aka 'Scribe'
        temperature=LLMConfigScribe.temperature,
        reasoning=LLMConfigScribe.reasoning,
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
    )

# Create agent using create_react_agent directly
anthropic_model = init_chat_model(
    model="anthropic:claude-3-5-sonnet-20241022", temperature=0.0
)
openai_model = init_chat_model(model="openai:gpt-4o-mini", temperature=0.0)

# Use ChatGoogleGenerativeAI directly instead of init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.0)

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
max_agent_iterations = 6
max_concurrent_local_agents = 2
max_concurrent_online_agents = 3

# Core Admin Tools
built_in_tools = [ls, read_file, write_file, write_todos, read_todos, think_tool]
save_tools = save_to_disk
# create the tools to delegate to sub-agents
research_tools = [
    tavily_search,
    pubmed_search,
] + built_in_tools  # PubMed for academic research, Tavily for general web search

graph_tools = built_in_tools + PERSONA_FORGE_TOOLS
report_tools = built_in_tools
architect_tools = built_in_tools
read_tools = built_in_tools
# *************************** Create Sub-Agents & Assign Tools****************************


# create the research sub-agent
research_agent = {
    "name": "research_agent",
    "description": "Delegate research to the sub-agent researcher. Provide this researcher with a description of your queries to delegate.",
    "prompt": RESEARCH_INSTRUCTIONS,
    "tools": [t.name for t in research_tools],
}

# create the research sub-agent

read_agent = {
    "name": "read_agent",
    "description": "Delegate reading, writing or summarizing to the read agent powered by a state of the art model. Only give this agent one task at a time.",
    "prompt": READ_AGENT_INSTRUCTIONS,
    "tools": [t.name for t in built_in_tools],
}

# create the research sub-agent
research_assistant = {
    "name": "research_assistant",
    "description": "Delegate research to the sub-agent Research Assistant, who will write the output to the specified file. Only give this researcher one topic at a time.",
    "prompt": RESEARCH_ASSISTANT_INSTRUCTIONS,
    "tools": [t.name for t in research_tools],
}

# create the web research sub-agent
graph_agent = {
    "name": "graph_agent",
    "description": "Request the Graph Agent starts the Graph Analysis workflow. Will write the analysis to the specified file.",
    "prompt": GRAPH_INSTRUCTIONS,
    "tools": [t.name for t in graph_tools],
}

# create the web research sub-agent
graph_assistant = {
    "name": "graph_assistant",
    "description": "Request the Graph Assistant to extract a specific query and write the output to the specified file. Only give this researcher one topic at a time.",
    "prompt": GRAPH_ASSISTANT_INSTRUCTIONS,
    "tools": [t.name for t in graph_tools],
}

# create the report writer sub-agent
report_agent = {
    "name": "report_agent",
    "description": "Delegate the report task to the sub-agent report-agent. Only give this researcher one report to write at a time.",
    "prompt": REPORT_INSTRUCTIONS,
    "tools": [t.name for t in report_tools],
}

# Create task tool for the Architect to delegate tasks to sub-agents

# The architects personal Read/Write Assistant
read_task = _create_task_tool(
    research_tools,
    [read_agent],
    gemini_model,
    DeepAgentState,
)

# Report Tasks
report_task = _create_task_tool(
    research_tools,
    [report_agent],
    scribe_model,
    DeepAgentState,
)
# Research Tasks
first_research_assistant_task = _create_task_tool(
    research_tools,
    [research_assistant],
    scribe_model,
    DeepAgentState,
)

second_research_assistant_task = _create_task_tool(
    research_tools,
    [research_assistant],
    alt_model,
    DeepAgentState,
)
first_graph_assistant_task = _create_task_tool(
    graph_tools,
    [graph_assistant],
    scribe_model,
    DeepAgentState,
)

second_graph_assistant_task = _create_task_tool(
    graph_tools,
    [graph_assistant],
    alt_model,
    DeepAgentState,
)


# *************************** Create Research Agents tools**********************************
research_agent_tools = research_tools + built_in_tools
research_supervisor_tools = [
    *research_agent_tools,  # Unpack the list with *
    first_research_assistant_task,
    second_research_assistant_task,
    read_task,
]
# *************************** Create Graph tools**********************************
graph_supervisor_tools = [
    *graph_tools,  # Unpack the list with *
    first_graph_assistant_task,
    second_graph_assistant_task,
    read_task,
]

# *************************** Create Second Level Agents tools**********************************


# Create task tool for the Architect to delegate tasks to sub-agents
research_task = _create_task_tool(
    research_supervisor_tools,
    [research_agent],
    overseer_model,
    DeepAgentState,
)

# Graph Tasks
graph_task = _create_task_tool(
    graph_supervisor_tools,
    [graph_agent],
    overseer_model,
    DeepAgentState,
)


# *************************** Create Architects delegation tools **********************************
delegation_tools = [
    research_task,
    read_task,
    graph_task,
    report_task,
]
all_architect_tools = architect_tools + delegation_tools


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
    )

    tools = all_architect_tools

    deep_agent = create_react_agent(
        model,
        tools,
        prompt=ARCHITECT_INSTRUCTIONS,
        checkpointer=short_term_memory,
        store=long_term_memory,
        state_schema=AgentState,
    ).with_config(
        {"recursion_limit": 150}
    )  # recursion_limit limits the number of steps the agent will run

    return deep_agent
