#!/usr/bin/env python3
"""
Regenerate Cypher for a specific QA pair.
Useful when the LLM makes a mistake on one entry.

Usage:
    python3 regenerate_single_qa.py qa_pair_003
"""

import sys
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END, START
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages

# Load environment variables
load_dotenv()

# Import the prompts and tools
from src.prompts.text_prompts import CYPHER_QA_PAIR_PROMPT
from src.tools.text_graph_tools import submit_cypher
from src.io_py.edge.config import LLMConfigGraphs

# LLM configuration - supports LM Studio, Anthropic, and Gemini
LLM_PROVIDER = os.getenv("CYPHER_LLM_PROVIDER", "lmstudio").lower()

if LLM_PROVIDER == "anthropic":
    llm = ChatAnthropic(
        model=os.getenv("CYPHER_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.1,
        max_tokens=8192,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    print(f"Using Anthropic model: {os.getenv('CYPHER_ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')}")
elif LLM_PROVIDER == "gemini":
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("CYPHER_GEMINI_MODEL", "gemini-2.0-flash-exp"),
        temperature=0.1,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    print(f"Using Gemini model: {os.getenv('CYPHER_GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
else:
    # Use LM Studio (default) - using config
    llm = ChatOpenAI(
        model=LLMConfigGraphs.model_name,
        temperature=LLMConfigGraphs.temperature,
        max_tokens=LLMConfigGraphs.max_tokens,
        base_url="http://localhost:1234/v1",  # LM Studio's OpenAI-compatible endpoint
        api_key="lm-studio",  # LM Studio doesn't require a real key
    )
    print(f"Using LM Studio model: {LLMConfigGraphs.model_name}")

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable):
        self.runnable = runnable

    def __call__(self, state: State, config):
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

def find_qa_analysis(qa_id: str) -> dict:
    """
    Find the analysis for a specific QA ID from the master file.

    Args:
        qa_id: The QA ID to find (e.g., 'qa_pair_003')

    Returns:
        Dictionary with the analysis content
    """
    master_file = os.path.join(
        os.getcwd(),
        "output",
        "psychological_analysis",
        "psychological_analysis_master.txt",
    )

    if not os.path.exists(master_file):
        raise FileNotFoundError(f"Master file not found: {master_file}")

    with open(master_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by entry separators
    entries = re.split(r"={80,}\n(?:={80,}\n)?ANALYSIS ENTRY", content)

    # Find the entry with matching QA ID
    for entry in entries:
        if f"QA ID: {qa_id}" in entry:
            # Extract the analysis sections
            lines = entry.split('\n')

            # Find sections
            qa_id_line = None
            question = ""
            answer = ""
            analysis_text = ""

            for i, line in enumerate(lines):
                if line.startswith("QA ID:"):
                    qa_id_line = line.replace("QA ID:", "").strip()
                elif line.startswith("Original Question:"):
                    question = line.replace("Original Question:", "").strip()
                elif line.startswith("Original Answer:"):
                    # Multi-line answer
                    answer_lines = []
                    j = i
                    while j < len(lines) and not lines[j].startswith("Analysis"):
                        if j == i:
                            answer_lines.append(lines[j].replace("Original Answer:", "").strip())
                        else:
                            answer_lines.append(lines[j].strip())
                        j += 1
                    answer = " ".join([l for l in answer_lines if l])
                elif line.strip() == "Analysis" or line.strip() == "Analysis:":
                    # Everything from here onwards
                    analysis_text = "\n".join(lines[i:])
                    break

            return {
                "qa_id": qa_id_line,
                "question": question,
                "answer": answer,
                "content": analysis_text,
            }

    raise ValueError(f"QA ID '{qa_id}' not found in master file")


def regenerate_qa_cypher(qa_id: str, output_file: str = None):
    """
    Regenerate Cypher for a specific QA pair, including text chunks and embeddings.

    Args:
        qa_id: The QA ID to regenerate (e.g., 'qa_pair_003')
        output_file: Optional output file path
    """
    print(f"\n🔍 Searching for {qa_id}...")

    # Find the analysis
    try:
        analysis = find_qa_analysis(qa_id)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print(f"✅ Found analysis for {qa_id}")
    print(f"   Question: {analysis['question'][:100]}...")
    print(f"   Answer: {analysis['answer'][:100]}...")

    # Check content length and warn if very long
    answer_text = analysis['answer']
    content_text = analysis['content']

    if len(answer_text) > 5000:
        print(f"⚠️  Answer is very long ({len(answer_text)} chars)")
        print(f"   This may cause the LLM to fail generating Cypher.")
        print(f"   Proceeding anyway - you may need to manually create the Cypher for this entry.")

    if len(content_text) > 3000:
        print(f"⚠️  Analysis content is very long ({len(content_text)} chars)")

    # Include question and answer in the prompt
    qa_context = f"""
    Original Question: {analysis['question']}

    Original Answer: {answer_text}

    """

    # Use the standard Cypher QA pair prompt but adapted for single QA pair
    from src.prompts.text_prompts import CYPHER_QA_PAIR_PROMPT

    # Modify it slightly for single QA pair generation
    single_qa_system_prompt = CYPHER_QA_PAIR_PROMPT.replace(
        "From the provided analysis CHUNK (multiple QA pairs)",
        "From the provided SINGLE QA pair analysis"
    ).replace(
        "output ONE Cypher query that inserts ALL pairs",
        "output ONE Cypher query that inserts this ONE pair"
    )

    # Create the prompt
    prompt_text = f"""
    Generate Cypher for this QA pair:

    QA ID: {qa_id}
    {qa_context}
    Analysis:
    {analysis['content']}
    """

    # Build the graph
    from langchain_core.prompts import ChatPromptTemplate

    qa_pair_prompt = ChatPromptTemplate.from_messages([
        ("system", single_qa_system_prompt),
        ("placeholder", "{messages}"),
    ])

    tools = [submit_cypher]
    qa_pair_runnable = qa_pair_prompt | llm.bind_tools(tools)

    from src.graphs.create_kg import create_tool_node_with_fallback

    qa_pair_builder = StateGraph(State)
    qa_pair_builder.add_node("assistant", Assistant(qa_pair_runnable))
    qa_pair_builder.add_node("tools", create_tool_node_with_fallback(tools))
    qa_pair_builder.add_edge(START, "assistant")

    from langgraph.prebuilt import tools_condition
    qa_pair_builder.add_conditional_edges("assistant", tools_condition)
    qa_pair_builder.add_edge("tools", "assistant")
    qa_pair_graph = qa_pair_builder.compile()

    # Run the workflow
    print(f"\n🤖 Generating Cypher for {qa_id}...")

    initial_state = {"messages": [HumanMessage(content=prompt_text)]}

    config = {
        "recursion_limit": 50,
        "configurable": {
            "thread_id": f"regen_{qa_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        },
    }

    # Track whether submit_cypher was called
    cypher_generated = False

    result = qa_pair_graph.invoke(initial_state, config=config)

    # Check if the LLM actually called the submit_cypher tool
    cypher_content = None

    for message in result.get("messages", []):
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.get("name") == "submit_cypher":
                    cypher_generated = True
                    break
        # Check if LLM returned Cypher in content instead of calling tool (Gemini behavior)
        if hasattr(message, "content") and message.content and isinstance(message.content, str):
            # Extract Cypher from markdown code blocks if present
            if "```cypher" in message.content or "MATCH" in message.content or "MERGE" in message.content:
                # Extract from code block if present
                import re
                code_block_match = re.search(r'```(?:cypher)?\n(.*?)\n```', message.content, re.DOTALL)
                if code_block_match:
                    cypher_content = code_block_match.group(1).strip()
                else:
                    # Use the whole content
                    cypher_content = message.content.strip()

    if cypher_generated:
        print(f"✅ QA pair Cypher generated successfully!")
    elif cypher_content:
        print(f"⚠️  LLM returned Cypher as text instead of calling tool. Submitting manually...")
        # Manually submit the Cypher
        try:
            result = submit_cypher.invoke(cypher_content)
            print(f"✅ QA pair Cypher submitted successfully!")
            cypher_generated = True
        except Exception as e:
            print(f"❌ Error submitting Cypher: {e}")
    else:
        print(f"⚠️  WARNING: LLM did not generate QA pair Cypher!")
        print(f"   This may be due to content length or complexity.")
        print(f"   Only embeddings will be generated.")

    # Generate text chunks and embeddings
    print(f"\n📝 Generating text chunks and embeddings...")

    try:
        from src.graphs.create_kg import create_text_chunks_and_embeddings, generate_text_chunk_cypher

        # Parse the analysis to extract clinical sections
        analysis_content = analysis['content']

        # Extract sections (simplified - just use the full content for now)
        chunks_result = create_text_chunks_and_embeddings(
            qa_id,
            analysis['question'],
            analysis['answer'],
            "",  # subjective_analysis - could parse this from content
            "",  # objective_analysis
            "",  # assessment
            ""   # plan
        )

        if chunks_result.get("status") == "success" and chunks_result.get("chunks"):
            chunks = chunks_result["chunks"]
            chunk_cypher = generate_text_chunk_cypher(chunks)

            # Append to the same file by calling the tool directly
            combined_cypher = (
                f"// ============================================================================\n"
                f"// TEXT CHUNKS AND EMBEDDINGS FOR {qa_id.upper()}\n"
                f"// ============================================================================\n\n"
                f"{chunk_cypher}"
            )

            # Call the tool function directly (it's already imported at the top)
            result = submit_cypher.invoke(combined_cypher)
            print(f"   {result}")

            print(f"✅ Generated {len(chunks)} text chunks with embeddings")
        else:
            print(f"⚠️  Warning: Could not generate embeddings: {chunks_result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"⚠️  Warning: Error generating embeddings: {e}")
        import traceback
        traceback.print_exc()

    # If output file specified, save there
    if output_file:
        # Find the generated Cypher file and copy the relevant section
        print(f"💾 Saved to standard output location")
        print(f"\n💡 Check the latest Cypher file in output/psychological_analysis/graph_output/")

    print(f"\n✨ Done! You can now:")
    print(f"   1. Check the generated Cypher file")
    print(f"   2. Copy the {qa_id} section (including embeddings)")
    print(f"   3. Replace the broken entry in your main Cypher file")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 regenerate_single_qa.py <qa_id>")
        print("Example: python3 regenerate_single_qa.py qa_pair_003")
        sys.exit(1)

    qa_id = sys.argv[1]

    # Optional: output file
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    regenerate_qa_cypher(qa_id, output_file)
