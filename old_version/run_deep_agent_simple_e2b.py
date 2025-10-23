#!/usr/bin/env python3
"""
Simple E2B Deep Agent Setup (No Terminal UI Imports)

This follows the smolagents pattern - orchestration on HOST, execution in E2B.
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from langgraph.checkpoint.memory import MemorySaver

# Load environment
load_dotenv()

def setup_sandbox():
    """Create and configure E2B sandbox"""
    print("🚀 Creating E2B sandbox...")
    sandbox = Sandbox()

    # Install dependencies
    print("📦 Installing dependencies...")
    sandbox.commands.run(
        "pip install neo4j langchain langchain-core langchain-ollama",
        timeout=120
    )

    # Set environment variables
    print("🔑 Configuring environment...")
    env_vars = {
        "NEO4J_URI": os.getenv("NEO4J_URI", "bolt://host.docker.internal:7687"),
        "NEO4J_USER": os.getenv("NEO4J_USER", "neo4j"),
        "NEO4JP": os.getenv("NEO4JP"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
    }

    for key, value in env_vars.items():
        if value:
            sandbox.commands.run(f"export {key}='{value}'")

    # Create workspace directories in home (where we have permissions)
    # Use ~/workspace instead of /workspace to avoid permission issues
    sandbox.commands.run("mkdir -p ~/workspace/data")
    sandbox.commands.run("mkdir -p ~/workspace/reports")
    sandbox.commands.run("mkdir -p ~/workspace/research")

    print("✅ Sandbox ready!")
    return sandbox


def create_e2b_agent(sandbox):
    """Create deep agent with E2B tools"""

    from src.graphs.deep_agent import (
        scribe_model, overseer_model, alt_model,
        LLMConfigArchitect, DeepAgentState
    )
    from src.tools.e2b_tools import E2B_TOOLS, set_global_sandbox
    from src.tools.deep_rag_tools import DEEP_PERSONA_FORGE_TOOLS
    from src.tools.research_tools import tavily_search, pubmed_search, think_tool
    from src.tools.todo_tools import write_todos, read_todos
    from src.tools.task_tool import _create_task_tool
    from src.prompts.e2b_prompts import E2B_ARCHITECT_INSTRUCTIONS, E2B_SUBAGENT_INSTRUCTIONS
    from langgraph.prebuilt import create_react_agent
    from langchain_ollama import ChatOllama

    # Set global sandbox for E2B tools
    print("🔧 Setting up global sandbox...")
    set_global_sandbox(sandbox)

    print("🛠️ Creating agent tools...")

    # Core tools (E2B replaces virtual filesystem)
    core_tools = E2B_TOOLS + [write_todos, read_todos, think_tool]

    # Research tools
    research_tools = [tavily_search, pubmed_search]

    # Assistant tools (what sub-agents can use)
    assistant_tools = DEEP_PERSONA_FORGE_TOOLS + research_tools + core_tools

    # Create sub-agent definition
    assistant = {
        "name": "assistant",
        "description": "Delegate tasks to assistant for Neo4j queries and research",
        "prompt": E2B_SUBAGENT_INSTRUCTIONS,
        "tools": [t.name for t in assistant_tools],
    }

    # Create delegation tools
    print("🔧 Creating delegation tools...")
    delegation_tools = [
        _create_task_tool(
            assistant_tools, [assistant], scribe_model, DeepAgentState,
            tool_name="delegate_to_scribe"
        ),
        _create_task_tool(
            assistant_tools, [assistant], overseer_model, DeepAgentState,
            tool_name="delegate_to_overseer"
        ),
        _create_task_tool(
            assistant_tools, [assistant], alt_model, DeepAgentState,
            tool_name="delegate_to_alt"
        ),
    ]

    # Architect has all tools for visibility
    architect_tools = DEEP_PERSONA_FORGE_TOOLS + research_tools + core_tools + delegation_tools

    # Create architect model
    print("🧠 Creating architect model...")
    model = ChatOllama(
        model=LLMConfigArchitect.model_name,
        temperature=LLMConfigArchitect.temperature,
        reasoning=LLMConfigArchitect.reasoning,
        num_predict=32768,  # Doubled for gpt-oss:20b - it needs more tokens for tool calls
        num_ctx=100000,     # Context window size
    )

    # Create agent
    print("🤖 Building deep agent...")
    agent = create_react_agent(
        model,
        architect_tools,
        prompt=E2B_ARCHITECT_INSTRUCTIONS,
        checkpointer=MemorySaver(),
        state_schema=DeepAgentState,
    )

    print(f"✅ Agent created with {len(architect_tools)} tools!")
    return agent


def run_workflow(agent, sandbox, task: str):
    """Run a single workflow task"""

    print("\n" + "="*80)
    print(f"📋 TASK: {task}")
    print("="*80 + "\n")

    config = {
        "configurable": {"thread_id": "main_workflow"},
        "recursion_limit": 75,  # Increase from default 25 to allow more steps
    }

    # Initial state (no need to pass sandbox - it's global now)
    initial_state = {
        "messages": [{"role": "user", "content": task}],
    }

    print("🔄 Running workflow...")

    for i, chunk in enumerate(agent.stream(initial_state, config, stream_mode="values")):
        if "messages" in chunk:
            latest = chunk["messages"][-1]

            # Show tool calls
            if hasattr(latest, "tool_calls") and latest.tool_calls:
                for tool_call in latest.tool_calls:
                    print(f"\n🔧 Tool: {tool_call.get('name')}")
                    if tool_call.get('name') == 'think_tool':
                        reflection = tool_call.get('args', {}).get('reflection', '')
                        print(f"💭 Thinking: {reflection[:100]}...")

            # Show responses
            if hasattr(latest, "content") and latest.content:
                print(f"\n💬 Response: {latest.content[:200]}...")

    print("\n✅ Workflow complete!")

    # Show workspace contents
    print("\n📁 Workspace contents:")
    result = sandbox.commands.run("find ~/workspace -type f", timeout=10)
    print(result.stdout)

    # Export the report
    print("\n📥 Exporting report...")
    try:
        # Find the therapy note file
        reports = sandbox.commands.run("ls ~/workspace/reports/*.txt", timeout=10)
        if reports.stdout:
            report_file = reports.stdout.strip().split('\n')[0]
            report_content = sandbox.files.read(report_file)

            # Save to local output directory
            import os
            os.makedirs("output/e2b_reports", exist_ok=True)
            output_path = "output/e2b_reports/therapy_note_latest.txt"

            with open(output_path, "w") as f:
                f.write(report_content)

            print(f"✅ Report saved to: {output_path}")
            print(f"\n📄 Report preview (first 500 chars):")
            print(report_content[:500])
        else:
            print("⚠️  No report file found in ~/workspace/reports/")
    except Exception as e:
        print(f"⚠️  Could not export report: {e}")


def main():
    """Main orchestration - runs on HOST"""

    print("\n🌟 DEEP AGENT WITH E2B 🌟\n")

    # Setup
    sandbox = setup_sandbox()

    try:
        # Create agent
        agent = create_e2b_agent(sandbox)

        # Run workflow
        task = "Please start the workflow for client_001, session_001. Retrieve diagnosis, subjective analysis, and objective analysis. Save results to ~/workspace/data/ and create a therapy note in ~/workspace/reports/."

        run_workflow(agent, sandbox, task)

        print("\n🎉 All done!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🧹 Cleaning up sandbox...")
        try:
            # Old e2b versions use kill() instead of close()
            if hasattr(sandbox, 'close'):
                sandbox.close()
            elif hasattr(sandbox, 'kill'):
                sandbox.kill()
        except Exception as e:
            print(f"Warning: Error closing sandbox: {e}")
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
