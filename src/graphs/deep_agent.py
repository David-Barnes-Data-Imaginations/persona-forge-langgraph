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
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
    TASK_DESCRIPTION_PREFIX,
    PUBMED_RESEARCH_INSTRUCTIONS,
    GRAPH_ANALYSIS_INSTRUCTIONS,
    REPORT_WRITER_INSTRUCTIONS,
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


"""Sub Agent models for the workflow
- The reason for different models is to test parrallelism and specialisation of tasks
- Peon - basic tasks, file handling, simple tasks
- Scribe/SmolScribe - research, web searching, summarization
- Overseer - high level tasks, planning, analysis, report writing

"""
peon_model = ChatOllama(
    model=LLMConfigPeon.model_name,
    temperature=LLMConfigPeon.temperature,
    reasoning=LLMConfigPeon.reasoning,
)

scribe_model = ChatOllama(
    model=LLMConfigSmolScribe.model_name,
    temperature=LLMConfigSmolScribe.temperature,
    reasoning=LLMConfigSmolScribe.reasoning,
)

overseer_model = ChatOllama(
    model=LLMConfigOverseer.model_name,
    temperature=LLMConfigOverseer.temperature,
    reasoning=LLMConfigOverseer.reasoning,
)

"""*************************** Workflow order (i think)*********************************
The main deep agent is the architect. It queries how many 'QA Pairs' are in the graph,
calls the Graph Analysis Agent for each pair to extract the data and write the 
psychological for the pair to a file. 
The Report Writer creates a 'Progress Notes' style document for the psychologist to review.
The Architect then reviews the notes, makes any changes, and uses the Pubmed Researcher 
to provide an additional section for helpful suggestions or recent studies.

main deep agent (Architect)
├─ query_pair_numbers tool (tbc)
├─ built-in tools
│  ├─ ls tool
│  ├─ read file tool
│  ├─ write file tool
│  ├─ write todos tool
│  ├─ read todos tool
├─ task tool
├─ pub_med_research sub-agent (overseer)
│  ├─ tavily search tool
│  ├─ pubmed_search_tool (tbc)
│  ├─ think tool
├─ Graph Analyzer sub-agent(overseer)
│  ├─ graph search tool
│  ├─ write file tool
│  ├─ read file tool
│  ├─ think tool
├─ Report Writer sub-agent (overseer)
│  ├─ write tool
│  ├─ read tool
│  ├─ think tool

"""

# *************************** Tools and Sub-agents**************************************
# Set limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Core Admin Tools
built_in_tools = [ls, read_file, write_file, write_todos, read_todos, think_tool]

# create the tools to delegate to sub-agents
pubmed_research_tools = [
    tavily_search,
    built_in_tools,
]  # pubmed_search_tool (tbc), tavily search tool thrown in in-case i decide to use later
graph_analysis_tools = [built_in_tools]
report_writer_tools = [built_in_tools]

# *************************** Create web-research sub-agent ****************************
# Create the web_search_sub_agent tools
web_research_sub_agent_tools = [tavily_search, think_tool]

# create the web research sub-agent
pubmed_research_sub_agent = {
    "name": "pubmed-search-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": PUBMED_RESEARCH_INSTRUCTIONS,  # tbc
    "tools": ["pubmed_research_tools"],
}

# create the web research sub-agent
graph_analysis_sub_agent = {
    "name": "graph_analysis-agent",
    "description": "Request the Graph Agent to extract a specific 'QA Pair' and write the analysis to the file. Only give this researcher one topic at a time.",
    "prompt": GRAPH_ANALYSIS_INSTRUCTIONS,  # tbc
    "tools": ["graph_analysis_tools"],
}

# create the report writer sub-agent
report_writer_sub_agent = {
    "name": "pubmed-search-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": REPORT_WRITER_INSTRUCTIONS,
    "tools": ["report_writer_tools"],
}

# Create task tool for the Architect to delegate tasks to sub-agents
single_research_task_tool = _create_task_tool(
    pubmed_research_tools,
    [pubmed_research_sub_agent],
    LLMConfigSmolScribe.model_name,
    DeepAgentState,
)

single_graph_task_tool = _create_task_tool(
    graph_analysis_tools,
    [graph_analysis_sub_agent],
    LLMConfigSmolScribe.model_name,
    DeepAgentState,
)

single_report_task_tool = _create_task_tool(
    report_writer_tools,
    [research_sub_agent],
    LLMConfigSmolScribe.model_name,
    DeepAgentState,
)

all_tools = (
    built_in_tools
    + TASK_DESCRIPTION_PREFIX
    + [
        single_research_task_tool,
        single_graph_task_tool,
        single_report_task_tool,
    ]
)

"""**************************** A TODO note on files ***********************************
Note for implementation of file handling in agents.
Files are added to the agent using this format:
```
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Give me an overview of Model Context Protocol (MCP).",
            }
        ],
        "files": {},
    }
)
format_messages(result["messages"])
```


# or in the streaming case i 'think' like the below:

`result = self.agent.invoke({"messages": messages, "files": {}}, config=self.config)`


# *************************** Create Architects Tools **********************************

# Create task tool to delegate tasks to sub-agents
single_graph_task_tool = _create_task_tool(
    graph_analysis_tools,
    [pub_med_research_sub_agent],
    LLMConfigScribe.model_name,
    DeepAgentState,
)

delegation_tools = [web_task_tool]
all_tools = built_in_tools + delegation_tools
"""


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


def print_deep_agent_prompts():
    """Display key prompts used by the deep agent to terminal for debugging."""
    show_prompt(WRITE_TODOS_DESCRIPTION)
    show_prompt(READ_FILE_DESCRIPTION)
    show_prompt(LS_DESCRIPTION)
    show_prompt(WRITE_FILE_DESCRIPTION)
