from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from src.server import get_mcp_server_tools
from ..utils.voice_tools import get_tools as get_datetime_tools
from langchain_ollama import ChatOllama
from ..io_py.edge.config import LLMConfigVoice
# This builds the cookie-cutter (copy paste) LangGraph agent
# The ReactAgent is new with 1.0, so not implemented in the other graph til i test it

# create agent
def get_new_agent(
        config, short_term_memory, long_term_memory
) -> CompiledStateGraph:
    """Build and return a new graph that defines the agent workflow."""

    # initialise the LLM
    model = ChatOllama(
        model=LLMConfigVoice.model_name,
        temperature=LLMConfigVoice.temperature,
        reasoning=LLMConfigVoice.reasoning
    )

    # initialise the tools that the agent will use
    server_tools = get_mcp_server_tools()

    tools = (
        get_datetime_tools()
        + server_tools
    )

    # build the agent workflow given the LLM, its tools and memory.
    agent_executor = create_react_agent(
        model,
        tools,
        checkpointer=short_term_memory,
        store=long_term_memory
    )

    return agent_executor

#  def get_response_stream(agent_executor: object, system_prompt_formatted: dict, user_query_formatted: dict):


