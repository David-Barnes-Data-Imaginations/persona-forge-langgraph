from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph
from sympy import false
from ..io_py.edge.server import get_mcp_server_tools
from ..utils.voice_tools import get_tools as get_datetime_tools

# This builds the cookie-cutter (copy paste) LangGraph agent
# The ReactAgent is new with 1.0, so not implemented in the other graph til i test it

# create agent
def get_new_agent(
        config, short_term_memory, long_term_memory
) -> CompiledStateGraph:
    """Build and return a new graph that defines the agent workflow."""

    # initialise the LLM
    model = ChatOllama(
        model="gemma3:1b",
        temperature=0,
        reasoning=false
    )


    # initialise the tools that the agent will use
    server_tools = await get_mcp_server_tools()

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

user_query = "Hello world!"
user_query_formatted = {
    "role": "user",
    "content": user_query
}

system_prompt_formatted = {
    "role": "system",
    "content": (
        "You are a voice assistant called Delamain."
        + " Keep your responses as short as possible."
        + "Do not format your responses using markdown, such as **bold** or _italics. ",
    )
}

response = agent_executor.invoke(
    {"messages" : [system_prompt_formatted, user_query_formatted]},
)

output_stream = agent_executor.stream(
    {"messages" : [system_prompt_formatted, user_query_formatted]},
    stream_mode="messages"
)
