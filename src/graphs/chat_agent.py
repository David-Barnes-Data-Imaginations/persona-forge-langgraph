# src/graphs/chat_agent.py
from langgraph.graph.state import CompiledStateGraph


from ..io_py.edge.config import (
    LLMConfigVoice,
)  # this just contains basic info to see up gpt-oss
from ..tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from ..prompts.text_prompts import VOICE_SYSTEM_PROMPT


def get_new_agent(config, short_term_memory, long_term_memory) -> CompiledStateGraph:
    from langgraph.prebuilt import create_react_agent
    from langchain_ollama import ChatOllama

    model = ChatOllama(
        model=LLMConfigVoice.model_name,
        temperature=LLMConfigVoice.temperature,
        reasoning=LLMConfigVoice.reasoning,  # keep your config as-is
    )

    tools = PERSONA_FORGE_TOOLS

    agent_executor = create_react_agent(
        model,
        tools,
        prompt=VOICE_SYSTEM_PROMPT,
        checkpointer=short_term_memory,
        store=long_term_memory,
    )
    return agent_executor
