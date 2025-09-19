from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from langchain_ollama import ChatOllama
from ..io_py.edge.config import LLMConfigVoice # this just contains basic info to see up gpt-oss
from ..utils.hybrid_rag_tools import PERSONA_FORGE_TOOLS

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


    tools = PERSONA_FORGE_TOOLS

    # build the agent workflow given the LLM, its tools and memory.
    agent_executor = create_react_agent(
        model,
        tools,
        checkpointer=short_term_memory,
        store=long_term_memory
    )

    return agent_executor

# This block would go in the main file:
async def main():


    user_query = "Hello world!"
    user_query_formatted = {
        "role": "user",
        "content": user_query
    }

    system_prompt_formatted = {
        "role": "system",
        "content": (
            "You are a helpful assistant"
        )
    }
