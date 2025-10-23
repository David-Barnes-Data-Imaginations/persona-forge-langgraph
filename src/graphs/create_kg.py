import os
import re
from typing import Annotated, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from datetime import datetime
from dotenv import load_dotenv

from ..prompts.text_prompts import (
    SYSTEM_PROMPT,
    CYPHER_SETUP_PROMPT,
    CYPHER_QA_PAIR_PROMPT,
)
from ..tools.text_graph_tools import submit_cypher
from ..utils.embeddings import embed_texts

# Load environment variables
load_dotenv()

# Add LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "cypher-generation"

# LLM configuration - supports both Ollama and Anthropic
LLM_PROVIDER = os.getenv("CYPHER_LLM_PROVIDER", "ollama").lower()

if LLM_PROVIDER == "anthropic":
    # Use Anthropic Claude for Cypher generation
    llm = ChatAnthropic(
        model=os.getenv("CYPHER_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.1,
        max_tokens=8192,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    print(
        f"Using Anthropic model: {os.getenv('CYPHER_ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')}"
    )
if LLM_PROVIDER == "gemini":
    # Use Anthropic Claude for Cypher generation
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("CYPHER_GEMINI_MODEL", "google_genai:gemini-2.5-flash"),
        temperature=0.0,
        max_tokens=8192,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    print(
        f"Using Gemini model: {os.getenv('CYPHER_GEMINI_MODEL', 'google_genai:gemini-2.5-flash')}"
    )
else:
    # Use Ollama (default)
    llm = ChatOllama(
        model=os.getenv("CYPHER_OLLAMA_MODEL", "gpt-oss:20b"),
        temperature=0.1,
    )
    print(f"Using Ollama model: {os.getenv('CYPHER_OLLAMA_MODEL', 'gpt-oss:20b')}")


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
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


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please retry, make sure not to include any erroneous characters as that can trip the error. Thanks!",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)


# Create two separate prompts for the two-step approach
setup_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CYPHER_SETUP_PROMPT),
        ("placeholder", "{messages}"),
    ]
)

qa_pair_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CYPHER_QA_PAIR_PROMPT),
        ("placeholder", "{messages}"),
    ]
)

# TWO-STEP WORKFLOW APPROACH
tools = [submit_cypher]

# Setup graph for Client/Session creation
setup_runnable = setup_prompt | llm.bind_tools(tools)
setup_builder = StateGraph(State)
setup_builder.add_node("assistant", Assistant(setup_runnable))
setup_builder.add_node("tools", create_tool_node_with_fallback(tools))
setup_builder.add_edge(START, "assistant")
setup_builder.add_conditional_edges("assistant", tools_condition)
setup_builder.add_edge("tools", "assistant")
setup_graph = setup_builder.compile()

# QA Pair generation - simplified without tool calling for reliability
# We'll generate the Cypher directly and save it manually
qa_pair_runnable = qa_pair_prompt | llm

# Set configuration for recursion limit
graph_config = {
    "recursion_limit": 50,  # Match your working CSV workflow
    "configurable": {},
}

"""
Functions for processing the psychological analysis master file
"""


def extract_analyses_from_master_file():
    """
    Extract individual analyses from the master file and return as chunks.
    Now also extracts original question/answer text for text chunking.
    """
    master_file = os.path.join(
        os.getcwd(),
        "output",
        "psychological_analysis",
        "psychological_analysis_master.txt",
    )

    print(f"Debug: Looking for master file at: {master_file}")

    if not os.path.exists(master_file):
        print(f"Master file {master_file} doesn't exist!")
        return []

    with open(master_file, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Debug: Master file size: {len(content)} characters")
    print(f"Debug: File starts with: {repr(content[:200])}")

    # Split by the entry separators - match the actual pattern:
    # Pattern 1: Single line of === followed by "ANALYSIS ENTRY"
    # Pattern 2: Double line of === with "ANALYSIS ENTRY" in between (old format)
    entries = re.split(r"={80,}\n(?:={80,}\n)?ANALYSIS ENTRY", content)
    print(f"Debug: Found {len(entries)} entries after split")

    analyses = []
    for i, entry in enumerate(entries):
        print(f"Debug: Processing entry {i}")
        print(f"Debug: Entry starts with: {repr(entry[:100])}")

        if "Analysis" in entry:  # Match both "Analysis:" and "Analysis"
            # Clean up the entry
            entry = entry.strip()
            lines = entry.split("\n")

            # Extract original question and answer
            original_question = ""
            original_answer = ""
            analysis_text = ""

            # Find the different sections
            qa_id_start = -1
            question_start = -1
            answer_start = -1
            analysis_start = -1

            for j, line in enumerate(lines):
                line_stripped = line.strip()
                if line_stripped.startswith("QA ID:"):
                    qa_id_start = j
                elif line_stripped.startswith("Original Question:"):
                    question_start = j
                elif line_stripped.startswith("Original Answer:"):
                    answer_start = j
                elif line_stripped == "Analysis:" or line_stripped == "Analysis":
                    analysis_start = j
                    break

            # Extract sections
            if question_start >= 0:
                original_question = (
                    lines[question_start].replace("Original Question:", "").strip()
                )

            if answer_start >= 0 and analysis_start >= 0:
                # Extract multi-line answer between "Original Answer:" and "Analysis:"
                answer_lines = []
                for line_idx in range(answer_start, analysis_start):
                    line = lines[line_idx]
                    if line_idx == answer_start:
                        # First line - remove "Original Answer:" prefix
                        line = line.replace("Original Answer:", "").strip()
                    else:
                        line = line.strip()

                    if line:  # Only add non-empty lines
                        answer_lines.append(line)

                original_answer = " ".join(answer_lines)

            if analysis_start >= 0:
                # Take everything from "Analysis:" onwards
                analysis_text = "\n".join(lines[analysis_start:]).strip()

                # Extract clinical sections for embedding
                subjective_analysis = ""
                objective_analysis = ""
                assessment = ""
                plan = ""

                # Parse the analysis text to extract sections
                current_section = None
                section_lines = []

                for line in lines[analysis_start + 1 :]:  # Skip "Analysis:" line
                    line_stripped = line.strip()

                    if line_stripped.startswith("Subjective Analysis:"):
                        if current_section:
                            # Save previous section
                            section_text = " ".join(section_lines)
                            if current_section == "subjective":
                                subjective_analysis = section_text
                            elif current_section == "objective":
                                objective_analysis = section_text
                            elif current_section == "assessment":
                                assessment = section_text
                            elif current_section == "plan":
                                plan = section_text
                        current_section = "subjective"
                        section_lines = [
                            line_stripped.replace("Subjective Analysis:", "").strip()
                        ]
                    elif line_stripped.startswith("Objective Analysis:"):
                        if current_section:
                            section_text = " ".join(section_lines)
                            if current_section == "subjective":
                                subjective_analysis = section_text
                        current_section = "objective"
                        section_lines = [
                            line_stripped.replace("Objective Analysis:", "").strip()
                        ]
                    elif line_stripped.startswith("Assessment:"):
                        if current_section:
                            section_text = " ".join(section_lines)
                            if current_section == "objective":
                                objective_analysis = section_text
                        current_section = "assessment"
                        section_lines = [
                            line_stripped.replace("Assessment:", "").strip()
                        ]
                    elif line_stripped.startswith("Plan:"):
                        if current_section:
                            section_text = " ".join(section_lines)
                            if current_section == "assessment":
                                assessment = section_text
                        current_section = "plan"
                        section_lines = [line_stripped.replace("Plan:", "").strip()]
                    elif line_stripped and current_section:
                        section_lines.append(line_stripped)

                # Save last section
                if current_section and section_lines:
                    section_text = " ".join(section_lines)
                    if current_section == "plan":
                        plan = section_text
                    elif current_section == "assessment":
                        assessment = section_text

                analyses.append(
                    {
                        "entry_number": len(analyses) + 1,
                        "content": analysis_text,
                        "original_question": original_question,
                        "original_answer": original_answer,
                        "subjective_analysis": subjective_analysis,
                        "objective_analysis": objective_analysis,
                        "assessment": assessment,
                        "plan": plan,
                    }
                )
                print(f"Debug: Successfully extracted analysis {len(analyses)}")
                print(f"Debug: Analysis preview: {analysis_text[:100]}...")
            else:
                print(f"Debug: Could not find 'Analysis:' line in entry {i}")
                print(
                    f"Debug: Available lines: {[line.strip() for line in lines[:10]]}"
                )

    print(f"Debug: Total analyses extracted: {len(analyses)}")
    return analyses


def create_client_session_setup() -> dict:
    """
    Create the initial Client and Session nodes for the therapy session.
    This runs once before processing any analysis chunks.

    Returns:
        Dictionary with setup results
    """
    try:
        # Create the prompt for Client/Session setup
        prompt_text = """
        Create the initial Cypher query to set up the Client and Session nodes for this therapy session.
        Use client_001 and session_001 as the IDs.

        Remember to call the submit_cypher tool with your generated Cypher query.
        """

        # Initial state with the prompt
        initial_state = {"messages": [HumanMessage(content=prompt_text)]}

        # Setup config
        setup_config = {
            "recursion_limit": 50,
            "configurable": {
                "thread_id": f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            },
        }

        # Run the setup graph
        print("Creating Client and Session setup...")
        result = setup_graph.invoke(initial_state, config=setup_config)

        return {
            "type": "setup",
            "messages_count": len(result.get("messages", [])),
            "status": "success",
        }

    except Exception as e:
        return {"type": "setup", "error": str(e), "status": "error"}


def create_text_chunks_and_embeddings(
    qa_pair_id: str,
    question: str,
    answer: str,
    subjective_analysis: str = "",
    objective_analysis: str = "",
    assessment: str = "",
    plan: str = "",
) -> dict:
    """
    Create semantic text chunks from question, answer, and clinical analysis, then generate embeddings.

    Args:
        qa_pair_id: The QA pair identifier
        question: The therapist's question
        answer: The client's answer
        subjective_analysis: Subjective analysis from SOAP note
        objective_analysis: Objective analysis from SOAP note
        assessment: Assessment from SOAP note
        plan: Plan from SOAP note

    Returns:
        Dictionary with chunks and their embeddings
    """
    try:
        # Create semantic chunks - typically 2-3 chunks per QA pair
        # Now includes clinical analysis sections for richer embeddings
        chunks = []

        # Build comprehensive text for embedding that includes clinical context
        clinical_context = ""
        if subjective_analysis:
            clinical_context += f" Clinical subjective: {subjective_analysis}."
        if objective_analysis:
            clinical_context += f" Clinical objective: {objective_analysis}."
        if assessment:
            clinical_context += f" Clinical assessment: {assessment}."
        if plan:
            clinical_context += f" Clinical plan: {plan}."

        # Split answer into sentences for semantic chunking
        import re

        sentences = re.split(r"[.!?]+", answer)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Group sentences into 2-3 chunks based on length
        if len(sentences) <= 2:
            # Short answer - one chunk with clinical context
            chunk_text = answer.strip() + clinical_context
            chunks.append(
                {
                    "chunk_id": f"s001.{qa_pair_id}.c1",
                    "session_id": "session_001",
                    "qa_id": qa_pair_id,
                    "timestamp": datetime.now().isoformat() + "Z",
                    "text": chunk_text,
                }
            )
        elif len(sentences) <= 4:
            # Medium answer - two chunks, add clinical context to both
            mid = len(sentences) // 2
            chunk1_text = ". ".join(sentences[:mid]).strip() + "." + clinical_context
            chunk2_text = ". ".join(sentences[mid:]).strip() + "." + clinical_context

            if chunk1_text:
                chunks.append(
                    {
                        "chunk_id": f"s001.{qa_pair_id}.c1",
                        "session_id": "session_001",
                        "qa_id": qa_pair_id,
                        "timestamp": datetime.now().isoformat() + "Z",
                        "text": chunk1_text,
                    }
                )

            if chunk2_text:
                chunks.append(
                    {
                        "chunk_id": f"s001.{qa_pair_id}.c2",
                        "session_id": "session_001",
                        "qa_id": qa_pair_id,
                        "timestamp": datetime.now().isoformat() + "Z",
                        "text": chunk2_text,
                    }
                )
        else:
            # Long answer - three chunks, add clinical context to all
            chunk_size = len(sentences) // 3

            for i in range(3):
                start_idx = i * chunk_size
                if i == 2:  # Last chunk gets remaining sentences
                    end_idx = len(sentences)
                else:
                    end_idx = (i + 1) * chunk_size

                chunk_text = (
                    ". ".join(sentences[start_idx:end_idx]).strip()
                    + "."
                    + clinical_context
                )
                if chunk_text:
                    chunks.append(
                        {
                            "chunk_id": f"s001.{qa_pair_id}.c{i+1}",
                            "session_id": "session_001",
                            "qa_id": qa_pair_id,
                            "timestamp": datetime.now().isoformat() + "Z",
                            "text": chunk_text,
                        }
                    )

        # Generate embeddings for chunks
        if chunks:
            texts_to_embed = [chunk["text"] for chunk in chunks]
            embeddings = embed_texts(texts_to_embed)

            # Add embeddings to chunks
            for chunk, embedding in zip(chunks, embeddings):
                chunk["embedding"] = embedding

        return {"chunks": chunks, "status": "success"}

    except Exception as e:
        return {"error": str(e), "status": "error"}


def generate_text_chunk_cypher(chunks: list) -> str:
    """
    Generate Cypher query for TextChunk nodes and their relationships.

    Args:
        chunks: List of chunk dictionaries with chunk_id, text, embedding, etc.

    Returns:
        Cypher query string
    """
    if not chunks:
        return "// No chunks to process"

    # Build the Cypher query
    cypher_lines = []

    # Add chunks data as literal list
    cypher_lines.append("MATCH (s:Session {session_id: 'session_001'})")
    cypher_lines.append("WITH s, [")

    # Add each chunk as a literal object
    for i, chunk in enumerate(chunks):
        embedding_str = "[" + ", ".join(map(str, chunk["embedding"])) + "]"

        # Escape double quotes in text for Cypher string literals
        escaped_text = chunk["text"].replace('"', '\\"')

        chunk_line = f"""  {{
    chunk_id: '{chunk['chunk_id']}',
    qa_id: '{chunk['qa_id']}',
    text: "{escaped_text}",
    embedding: {embedding_str}
  }}"""
        if i < len(chunks) - 1:
            chunk_line += ","
        cypher_lines.append(chunk_line)

    cypher_lines.append("] AS chunks")
    cypher_lines.append("UNWIND chunks AS c")

    # Create TextChunk nodes
    cypher_lines.append("MERGE (tc:TextChunk {id: c.chunk_id})")
    cypher_lines.append("SET tc.text = c.text,")
    cypher_lines.append("    tc.embedding = c.embedding")

    # Link to QA_Pair
    cypher_lines.append("WITH c, tc")
    cypher_lines.append("MATCH (qa:QA_Pair {id: c.qa_id})")
    cypher_lines.append("MERGE (qa)-[:HAS_CHUNK]->(tc);")

    return "\n".join(cypher_lines)


def process_analysis_to_cypher(analysis: dict) -> dict:
    """
    Process a single analysis through the LangGraph workflow to generate Cypher.
    Now also creates text chunks and embeddings, generating a combined Cypher file.

    Args:
        analysis: Dictionary with entry_number, content, original_question, original_answer

    Returns:
        Dictionary with processing results
    """
    try:
        # Create a unique thread_id for each analysis to ensure fresh state
        thread_id = f"analysis_{analysis['entry_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create the prompt for the LLM with the analysis data
        qa_pair_id = f"qa_pair_{str(analysis['entry_number']).zfill(3)}"

        # Include question and answer if available
        qa_context = ""
        if analysis.get("original_question") and analysis.get("original_answer"):
            qa_context = f"""
        Original Question: {analysis['original_question']}

        Original Answer: {analysis['original_answer']}

        """

        prompt_text = f"""Generate Cypher for QA_Pair ID: {qa_pair_id}

{qa_context}
{analysis['content']}

Extract from above:
- question, answer (from "Original Question/Answer")
- subjective_analysis, objective_analysis, assessment, plan (from "Analysis" section)
- emotions with valence/arousal/confidence (from "Instrument output" in Objective)
- distortions, stages, attachments, defenses, schemas, bigfive (from Assessment)

Output ONE UNWIND Cypher query with all data. Use double quotes for strings. Replace newlines with spaces.
"""

        # Generate Cypher directly from LLM (without tool calling)
        print(f"Processing analysis #{analysis['entry_number']}...")

        # Create a properly formatted message input for the prompt template
        result = qa_pair_runnable.invoke({"messages": [HumanMessage(content=prompt_text)]})

        # Extract Cypher from LLM response
        cypher_query = result.content if hasattr(result, 'content') else str(result)

        # Clean up the Cypher query (remove markdown code blocks if present)
        if "```" in cypher_query:
            # Extract content between ```cypher or ``` blocks
            import re
            match = re.search(r'```(?:cypher)?\s*\n(.*?)\n```', cypher_query, re.DOTALL)
            if match:
                cypher_query = match.group(1)

        # Save the Cypher query directly
        if cypher_query and cypher_query.strip() and "MATCH" in cypher_query:
            output_dir = os.path.join(
                os.getcwd(), "output", "psychological_analysis", "graph_output"
            )
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"psychological_graph_{timestamp[:8]}.cypher"
            filepath = os.path.join(output_dir, filename)

            entry_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append to the master Cypher file
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(
                    f"\n// ============================================================================\n"
                )
                f.write(f"// CYPHER ENTRY - {entry_timestamp}\n")
                f.write(f"// QA Pair: {qa_pair_id}\n")
                f.write(
                    f"// ============================================================================\n\n"
                )
                f.write(cypher_query.strip())
                f.write(
                    f"\n\n// ============================================================================\n"
                )

            print(f"Saved psychology framework Cypher for {qa_pair_id}")

        # Create text chunks and embeddings if we have original text
        chunks_result = None
        if analysis.get("original_question") and analysis.get("original_answer"):
            print(f"Creating text chunks for QA pair #{analysis['entry_number']}...")
            chunks_result = create_text_chunks_and_embeddings(
                qa_pair_id,
                analysis["original_question"],
                analysis["original_answer"],
                analysis.get("subjective_analysis", ""),
                analysis.get("objective_analysis", ""),
                analysis.get("assessment", ""),
                analysis.get("plan", ""),
            )

            # Generate additional Cypher for text chunks if successful
            if chunks_result.get("status") == "success" and chunks_result.get("chunks"):
                chunks = chunks_result["chunks"]
                text_chunk_cypher = generate_text_chunk_cypher(chunks)

                # Append text chunk Cypher to the same file
                output_dir = os.path.join(
                    os.getcwd(), "output", "psychological_analysis", "graph_output"
                )
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"psychological_graph_{timestamp[:8]}.cypher"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "a", encoding="utf-8") as f:
                    f.write(
                        f"\n// ============================================================================\n"
                    )
                    f.write(f"// TEXT CHUNKS AND EMBEDDINGS FOR {qa_pair_id.upper()}\n")
                    f.write(
                        f"// ============================================================================\n\n"
                    )
                    f.write(text_chunk_cypher)
                    f.write(
                        f"\n\n// ============================================================================\n"
                    )

                print(f"Added text chunks to Cypher file: {filepath}")

        return {
            "analysis_id": analysis["entry_number"],
            "thread_id": thread_id,
            "content": analysis["content"][:200] + "...",  # Truncated for brevity
            "cypher_generated": bool(cypher_query and "MATCH" in cypher_query),
            "chunks_created": (
                len(chunks_result.get("chunks", [])) if chunks_result else 0
            ),
            "status": "success",
        }

    except Exception as e:
        return {
            "analysis_id": analysis["entry_number"],
            "content": analysis["content"][:200] + "...",
            "error": str(e),
            "status": "error",
        }


def batch_process_master_file():
    """
    Process all analyses in the master file and generate Cypher queries.
    Uses a two-step approach: setup Client/Session first, then process each QA_Pair.
    """
    analyses = extract_analyses_from_master_file()

    if not analyses:
        return {"error": "No analyses found in master file!", "status": "failed"}

    results = {
        "total_analyses": len(analyses),
        "successful": 0,
        "errors": 0,
        "setup_result": None,
        "results": [],
        "status": "completed",
    }

    # Step 1: Create Client and Session setup
    print("\n=== STEP 1: Creating Client/Session Setup ===")
    setup_result = create_client_session_setup()
    results["setup_result"] = setup_result

    if setup_result["status"] != "success":
        return {
            "error": f"Setup failed: {setup_result.get('error', 'Unknown error')}",
            "status": "failed",
        }

    # Step 2: Process each analysis chunk
    print(f"\n=== STEP 2: Processing {len(analyses)} Analysis Chunks ===")
    for analysis in analyses:
        result = process_analysis_to_cypher(analysis)
        results["results"].append(result)

        if result["status"] == "success":
            results["successful"] += 1
        else:
            results["errors"] += 1

    return results


def process_kg_creation() -> dict:
    """
    Main function to process the master file and create knowledge graph.
    This is what will be called from SentimentSuite.py
    """
    try:
        return batch_process_master_file()
    except Exception as e:
        return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    result = process_kg_creation()
    print(result)
