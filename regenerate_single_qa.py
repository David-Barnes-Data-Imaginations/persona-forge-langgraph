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
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
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

# LLM configuration - supports both Ollama and Anthropic
LLM_PROVIDER = os.getenv("CYPHER_LLM_PROVIDER", "ollama").lower()

if LLM_PROVIDER == "anthropic":
    llm = ChatAnthropic(
        model=os.getenv("CYPHER_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.1,
        max_tokens=8192,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    print(f"Using Anthropic model: {os.getenv('CYPHER_ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')}")
else:
    llm = ChatOllama(
        model=os.getenv("CYPHER_OLLAMA_MODEL", "gpt-oss:20b"),
        temperature=0.1,
    )
    print(f"Using Ollama model: {os.getenv('CYPHER_OLLAMA_MODEL', 'gpt-oss:20b')}")

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

    # Include question and answer in the prompt
    qa_context = f"""
    Original Question: {analysis['question']}

    Original Answer: {analysis['answer']}

    """

    # Create the prompt
    prompt_text = f"""
    Please convert the following psychological analysis to a Cypher query for a single QA_Pair:

    Analysis Entry for {qa_id}:
    {qa_context}{analysis['content']}

    IMPORTANT: Use this exact QA_Pair ID: {qa_id}

    Remember to call the submit_cypher tool with your generated Cypher query.
    """

    # Build the graph
    from langchain_core.prompts import ChatPromptTemplate

    qa_pair_prompt = ChatPromptTemplate.from_messages([
        ("system", CYPHER_QA_PAIR_PROMPT),
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

    result = qa_pair_graph.invoke(initial_state, config=config)

    print(f"✅ Cypher generated successfully!")

    # Generate text chunks and embeddings
    print(f"\n📝 Generating text chunks and embeddings...")

    try:
        from src.graphs.create_kg import create_text_chunks_and_embeddings, generate_text_chunk_cypher
        from src.tools.text_graph_tools import append_cypher_to_file

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

            # Append to the same file
            append_cypher_to_file(
                f"\n// ============================================================================\n"
                f"// TEXT CHUNKS AND EMBEDDINGS FOR {qa_id.upper()}\n"
                f"// ============================================================================\n\n"
                f"{chunk_cypher}\n"
            )

            print(f"✅ Generated {len(chunks)} text chunks with embeddings")
        else:
            print(f"⚠️  Warning: Could not generate embeddings: {chunks_result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"⚠️  Warning: Error generating embeddings: {e}")

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
