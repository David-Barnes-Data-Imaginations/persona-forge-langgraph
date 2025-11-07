import pandas as pd
import os
from typing import Annotated, Optional
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from ..prompts.text_prompts import SYSTEM_PROMPT
from ..tools.text_graph_tools import submit_analysis
from ..io_py.edge.config import LLMConfigGraphs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add LangSmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "cypher-generation"

# LLM configuration - supports both Ollama and Anthropic
LLM_PROVIDER = os.getenv("TAGGING_LLM_PROVIDER", "ollama").lower()

if LLM_PROVIDER == "anthropic":
    # Use Anthropic Claude for Cypher generation
    llm = ChatAnthropic(
        model=os.getenv("TAGGING_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
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
        model=os.getenv("TAGGING_GEMINI_MODEL", "google_genai:gemini-2.5-flash"),
        temperature=0.0,
        max_tokens=16000,
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    print(
        f"Using Gemini model: {os.getenv('TAGGING_GEMINI_MODEL', 'google_genai:gemini-2.5-flash')}"
    )
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


assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("placeholder", "{messages}"),
    ]
)


tools = [submit_analysis]
assistant_runnable = assistant_prompt | llm.bind_tools(tools)

builder = StateGraph(State)

# Define nodes: these do the work
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
framework_graph = builder.compile()

# Set configuration for recursion limit
graph_config = {"recursion_limit": 50, "configurable": {}}  # Increased from default 25


def parse_therapy_csv(csv_content: str) -> list:
    """
    Parse the therapy CSV and extract QA pairs for processing.

    Handles CSV format where:
    - Question/answer text can span multiple rows.
    - message_id only appears on the LAST row of each Q&A pair
    - Forward-fills message_id to group multi-row entries

    Expected CSV format:
    Therapist,Client,message_id
    "question text",,,
    ,"answer text",,
    ,"more answer",,1
    "next question",,,
    ,"next answer",,2

    Args:
        csv_content: Raw CSV content as string

    Returns:
        List of QA pair dictionaries with question, answer, and message_id
    """
    try:
        from io import StringIO

        print("🔍 Parsing CSV...")

        # Try to read CSV with more robust error handling
        try:
            # Use python engine which is more forgiving with quoting issues
            df = pd.read_csv(
                StringIO(csv_content),
                quotechar='"',
                escapechar="\\",
                skipinitialspace=True,
                encoding="utf-8",
                engine="python",  # More forgiving parser
                on_bad_lines="warn",  # Show warnings instead of crashing
            )
        except Exception as parse_error:
            # If that fails, try to give more helpful error message
            lines = csv_content.split("\n")
            print(f"\n❌ CSV Parsing Error: {str(parse_error)}")
            print(f"📄 Total lines in CSV: {len(lines)}")

            # Show problematic line if we can identify it
            error_str = str(parse_error)
            if "line" in error_str.lower():
                import re

                line_match = re.search(r"line (\d+)", error_str)
                if line_match:
                    line_num = int(line_match.group(1))
                    if line_num < len(lines):
                        print(f"\n⚠️  Problem near line {line_num}:")
                        # Show context: 2 lines before, problem line, 2 lines after
                        start = max(0, line_num - 3)
                        end = min(len(lines), line_num + 2)
                        for i in range(start, end):
                            marker = ">>> " if i == line_num - 1 else "    "
                            print(f"{marker}Line {i+1}: {lines[i][:100]}")

            print("\n💡 Common CSV issues:")
            print('  - Unescaped quotes within quoted text (use "" for literal quotes)')
            print("  - Commas in text that aren't inside quotes")
            print('  - Mismatched quotes (opening " without closing ")')
            print("  - Extra columns or missing commas")

            raise ValueError(f"CSV parsing failed. See error details above.")

        # Clean column names
        df.columns = [col.strip() for col in df.columns]

        print(f"📊 Columns found: {df.columns.tolist()}")
        print(f"📏 Total rows: {len(df)}")

        # Verify required columns
        required_cols = ["Therapist", "Client", "message_id"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(
                f"CSV must contain columns: {required_cols}\n"
                f"Found columns: {df.columns.tolist()}\n"
                f"💡 Check that your header row is: Therapist,Client,message_id"
            )

        # Show first few rows for debugging
        print("\n📋 First 3 rows preview:")
        for idx, row in df.head(3).iterrows():
            print(
                f"  Row {idx+1}: Therapist={str(row['Therapist'])[:50]}... | "
                f"Client={str(row['Client'])[:50]}... | "
                f"message_id={row['message_id']}"
            )

        # Fill NaN message_ids backwards (in case message_id appears at end of blocks)
        df["message_id"] = df["message_id"].bfill()

        # Remove rows where message_id is still NaN
        df = df[df["message_id"].notna()]

        print(f"✓ After filtering: {len(df)} rows with valid message_ids")

        # Group by message_id to combine multi-row entries (if any)
        qa_pairs = []
        grouped = df.groupby("message_id", sort=False)

        for message_id, group in grouped:
            # Combine all non-null values for each column
            therapist_parts = group["Therapist"].dropna().astype(str).str.strip()
            client_parts = group["Client"].dropna().astype(str).str.strip()

            # Filter out empty strings, 'nan', and combine with spaces
            therapist_text = " ".join(
                [part for part in therapist_parts if part and part.lower() != "nan"]
            ).strip()

            client_text = " ".join(
                [part for part in client_parts if part and part.lower() != "nan"]
            ).strip()

            # Only include if we have both question and answer
            if therapist_text and client_text:
                qa_pair = {
                    "question": therapist_text,
                    "answer": client_text,
                    "message_id": f"qa_pair_{int(message_id):03d}",
                }
                qa_pairs.append(qa_pair)
                print(
                    f"✓ Parsed {qa_pair['message_id']}: Q={len(therapist_text)} chars, A={len(client_text)} chars"
                )
            else:
                missing = "question" if not therapist_text else "answer"
                print(f"⚠ Skipping message_id {message_id}: Missing {missing}")

        if not qa_pairs:
            raise ValueError(
                "No valid QA pairs found in CSV.\n"
                "💡 Check that:\n"
                "  - Therapist column has question text\n"
                "  - Client column has answer text\n"
                "  - message_id column has numbers (1, 2, 3, ...)"
            )

        print(f"\n✅ Successfully parsed {len(qa_pairs)} QA pairs from CSV\n")
        return qa_pairs

    except ValueError:
        # Re-raise ValueError with our custom messages
        raise
    except Exception as e:
        raise ValueError(f"Unexpected error parsing CSV: {str(e)}")


def enhance_analysis_with_qa(question: str, answer: str, message_id: str) -> None:
    """
    Post-process the most recent analysis entry to include original question, answer, and QA ID.
    This ensures the Q&A text and ID are always included regardless of LLM memory issues.

    Args:
        question: The therapist's original question
        answer: The client's original answer
        message_id: The message/QA pair ID
    """
    try:
        import os

        master_file = os.path.join(
            os.getcwd(),
            "output",
            "psychological_analysis",
            "psychological_analysis_master.txt",
        )

        if not os.path.exists(master_file):
            print("Warning: Master analysis file doesn't exist yet")
            return

        # Read the entire file
        with open(master_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by entry separators to find the last entry
        separator = "=" * 80
        entries = content.split(f"\n{separator}\nANALYSIS ENTRY")

        if len(entries) < 2:
            print("Warning: No analysis entries found to enhance")
            return

        # Get the last entry (most recent)
        last_entry = entries[-1]

        # Split the last entry to separate the timestamp line from the analysis
        lines = last_entry.split("\n")
        if len(lines) < 3:
            print("Warning: Last entry format is unexpected")
            return

        # Find where the analysis content starts (after the timestamp and separator lines)
        analysis_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip() == separator:
                analysis_start_idx = i + 1
                break

        if analysis_start_idx == 0:
            print("Warning: Could not find analysis content in last entry")
            return

        # Extract the timestamp and separator lines
        header_lines = lines[:analysis_start_idx]

        # Extract the existing analysis content
        existing_analysis = "\n".join(lines[analysis_start_idx:]).strip()

        # Create the enhanced analysis with QA ID, Q&A prepended
        qa_id = f"qa_pair_{str(message_id).zfill(3)}"
        enhanced_analysis = f"QA ID: {qa_id}\n\nOriginal Question: {question}\n\nOriginal Answer: {answer}\n\n{existing_analysis}"

        # Reconstruct the last entry with enhanced content
        enhanced_entry = "\n".join(header_lines) + "\n" + enhanced_analysis

        # Reconstruct the full file with the enhanced last entry
        enhanced_content = (
            f"\n{separator}\nANALYSIS ENTRY".join(entries[:-1])
            + f"\n{separator}\nANALYSIS ENTRY"
            + enhanced_entry
        )

        # Write the enhanced content back to the file
        with open(master_file, "w", encoding="utf-8") as f:
            f.write(enhanced_content)

        print(f"Enhanced analysis with original Q&A text")

    except Exception as e:
        print(f"Warning: Failed to enhance analysis with Q&A: {str(e)}")


def process_qa_pair(qa_pair: dict) -> dict:
    """
    Process a single QA pair through the LangGraph workflow.

    Args:
        qa_pair: Dictionary with question, answer, message_id

    Returns:
        Dictionary with processing results
    """
    try:
        # Create the prompt for the LLM with the QA pair data
        prompt_text = f"""
        Please analyze the following QA pair from a therapy session:
        
        Question: {qa_pair['question']}
        Answer: {qa_pair['answer']}
        Message ID: {qa_pair['message_id']}
        
        Analyze ONLY the Client's answer and return the psychological analysis on its own without the Question and Answer.
        """

        # Initial state with the prompt
        initial_state = {"messages": [HumanMessage(content=prompt_text)]}

        # Run the graph with increased recursion limit
        result = framework_graph.invoke(initial_state, config=graph_config)

        # Post-process: Add original question, answer, and QA ID to the analysis file
        enhance_analysis_with_qa(qa_pair["question"], qa_pair["answer"], qa_pair["message_id"])

        return {
            "qa_id": qa_pair["message_id"],
            "question": qa_pair["question"],
            "answer": qa_pair["answer"],
            "result": result,
            "status": "success",
        }

    except Exception as e:
        return {
            "qa_id": qa_pair["message_id"],
            "question": qa_pair["question"],
            "answer": qa_pair["answer"],
            "error": str(e),
            "status": "error",
        }


def process_therapy_session(csv_content: str) -> dict:
    """
    Process entire therapy session CSV through the LangGraph workflow.

    Args:
        csv_content: Raw CSV content as string

    Returns:
        Dictionary with processing results and statistics
    """
    try:
        qa_pairs = parse_therapy_csv(csv_content)

        results = []
        successful_count = 0
        error_count = 0

        for qa_pair in qa_pairs:
            result = process_qa_pair(qa_pair)
            results.append(result)

            if result["status"] == "success":
                successful_count += 1
            else:
                error_count += 1

        return {
            "total_pairs": len(qa_pairs),
            "successful": successful_count,
            "errors": error_count,
            "results": results,
            "status": "completed",
        }

    except Exception as e:
        return {"error": str(e), "status": "failed"}
