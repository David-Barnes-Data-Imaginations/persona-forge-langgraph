# src/graphs/chat_agent.py
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from ..tools.hybrid_rag_tools import PERSONA_FORGE_TOOLS
from ..prompts.text_prompts import VOICE_SYSTEM_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI

import os

gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.3,
    api_key=os.environ.get("GEMINI_API_KEY"),
)


def get_new_agent(config, short_term_memory, long_term_memory) -> CompiledStateGraph:
    tools = PERSONA_FORGE_TOOLS

    agent_executor = create_react_agent(
        gemini_model,
        tools,
        prompt=VOICE_SYSTEM_PROMPT,
        checkpointer=short_term_memory,
        store=long_term_memory,
    )
    return agent_executor
