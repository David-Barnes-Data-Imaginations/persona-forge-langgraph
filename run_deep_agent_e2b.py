#!/usr/bin/env python3
"""
E2B Deep Agent with Fancy Terminal UI

This combines E2B sandbox execution with Rich terminal interface.
Orchestration happens on HOST, execution in E2B sandbox.
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from langgraph.checkpoint.memory import MemorySaver

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box

# Load environment
load_dotenv()

console = Console()


def setup_sandbox():
    """Create and configure E2B sandbox"""
    with console.status("[bold cyan]🚀 Creating E2B sandbox...", spinner="dots"):
        sandbox = Sandbox()

    with console.status("[bold cyan]📦 Installing dependencies...", spinner="dots"):
        result = sandbox.commands.run(
            "pip install neo4j langchain langchain-core langchain-openai", timeout=120
        )
        if result.exit_code != 0:
            console.print(f"[yellow]⚠️  Warning: {result.stderr}[/yellow]")

    # Set environment variables
    console.print("[bold green]🔑 Configuring environment...[/bold green]")
    env_vars = {
        "NEO4J_URI": os.getenv("NEO4J_URI", "bolt://host.docker.internal:7687"),
        "NEO4J_USER": os.getenv("NEO4J_USER", "neo4j"),
        "NEO4JP": os.getenv("NEO4JP"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    }

    for key, value in env_vars.items():
        if value:
            sandbox.commands.run(f"export {key}='{value}'")

    # Create workspace directories
    sandbox.commands.run("mkdir -p ~/workspace/data")
    sandbox.commands.run("mkdir -p ~/workspace/reports")
    sandbox.commands.run("mkdir -p ~/workspace/research")

    console.print("[bold green]✅ Sandbox ready![/bold green]\n")
    return sandbox


def create_e2b_agent(sandbox):
    """Create deep agent with E2B tools"""

    from src.graphs.deep_agent import (
        scribe_model,
        overseer_model,
        alt_model,
        LLMConfigArchitect,
        DeepAgentState,
    )
    from src.tools.e2b_tools import E2B_TOOLS, set_global_sandbox
    from src.tools.hybrid_rag_tools import (
        PERSONA_FORGE_TOOLS,
    )  # Use original tools, not deep_* wrappers
    from src.tools.research_tools import tavily_search, pubmed_search, think_tool
    from src.tools.todo_tools import write_todos, read_todos
    from src.tools.task_tool import _create_task_tool
    from src.prompts.e2b_prompts import (
        E2B_ARCHITECT_INSTRUCTIONS,
        E2B_ARCHITECT_INSTRUCTIONS,
        E2B_SUBAGENT_INSTRUCTIONS,
    )
    from langgraph.prebuilt import create_react_agent
    from langchain_openai import ChatOpenAI

    # Set global sandbox for E2B tools
    console.print("[bold cyan]🔧 Setting up global sandbox...[/bold cyan]")
    set_global_sandbox(sandbox)

    console.print("[bold cyan]🛠️  Creating agent tools...[/bold cyan]")

    # Core tools (E2B replaces virtual filesystem)
    core_tools = E2B_TOOLS + [write_todos, read_todos, think_tool]

    # Research tools
    research_tools = [tavily_search, pubmed_search]

    # Assistant tools (what sub-agents can use)
    # Use PERSONA_FORGE_TOOLS (original RAG tools that return data directly)
    # The agent will manually save results using execute_bash
    assistant_tools = PERSONA_FORGE_TOOLS + research_tools + core_tools

    # Create sub-agent definition
    assistant = {
        "name": "assistant",
        "description": "Delegate tasks to assistant for Neo4j queries and research",
        "prompt": E2B_SUBAGENT_INSTRUCTIONS,
        "tools": [t.name for t in assistant_tools],
    }

    # Create delegation tools
    console.print("[bold cyan]🔧 Creating delegation tools...[/bold cyan]")
    delegation_tools = [
        _create_task_tool(
            assistant_tools,
            [assistant],
            scribe_model,
            DeepAgentState,
            tool_name="delegate_to_scribe",
        ),
        _create_task_tool(
            assistant_tools,
            [assistant],
            overseer_model,
            DeepAgentState,
            tool_name="delegate_to_overseer",
        ),
        _create_task_tool(
            assistant_tools,
            [assistant],
            alt_model,
            DeepAgentState,
            tool_name="delegate_to_alt",
        ),
    ]

    # Architect has all tools for visibility
    architect_tools = (
        PERSONA_FORGE_TOOLS + research_tools + core_tools + delegation_tools
    )

    # Create architect model - LM Studio configuration
    console.print("[bold cyan]🧠 Creating architect model...[/bold cyan]")
    model = ChatOpenAI(
        model=LLMConfigArchitect.model_name,
        temperature=LLMConfigArchitect.temperature,
        max_tokens=32768,  # Doubled for gpt-oss:20b - it needs more tokens for tool calls
        base_url="http://localhost:1234/v1",  # LM Studio's OpenAI-compatible endpoint
        api_key="lm-studio",  # LM Studio doesn't require a real key
    ).with_config(
        {"recursion_limit": 75}  # Allow more steps since thinking counts as steps
    )
    # Create agent
    console.print("[bold cyan]🤖 Building deep agent...[/bold cyan]")
    agent = create_react_agent(
        model,
        architect_tools,
        prompt=E2B_ARCHITECT_INSTRUCTIONS,
        checkpointer=MemorySaver(),
        state_schema=DeepAgentState,
    )

    console.print(
        f"[bold green]✅ Agent created with {len(architect_tools)} tools![/bold green]\n"
    )
    return agent


def create_todo_table(todos):
    """Create a Rich table for TODOs"""
    if not todos:
        return Panel(
            "[dim]No TODOs yet[/dim]", title="📋 TODO List", border_style="cyan"
        )

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Status", width=12)
    table.add_column("Task", style="white")

    status_styles = {
        "pending": ("⏳", "yellow"),
        "in_progress": ("🔄", "cyan"),
        "completed": ("✅", "green"),
    }

    for i, todo in enumerate(todos, 1):
        status = todo.get("status", "pending")
        emoji, color = status_styles.get(status, ("❓", "white"))
        status_text = f"{emoji} {status}"
        content = todo.get("content", "Unknown task")

        table.add_row(str(i), Text(status_text, style=color), content)

    return Panel(table, title="📋 TODO List", border_style="cyan")


def run_workflow(agent, sandbox, task: str):
    """Run workflow with fancy terminal UI"""

    # Header
    console.print("\n" + "=" * 80)
    console.print(
        Panel.fit(
            f"[bold cyan]{task}[/bold cyan]", title="📋 TASK", border_style="cyan"
        )
    )
    console.print("=" * 80 + "\n")

    config = {
        "configurable": {"thread_id": "main_workflow"},
        "recursion_limit": 75,  # Increase from default 25 to allow more steps
    }

    # Initial state (no need to pass sandbox - it's global now)
    initial_state = {
        "messages": [{"role": "user", "content": task}],
    }

    console.print("[bold cyan]🔄 Running workflow...[/bold cyan]\n")

    current_todos = []
    step_count = 0

    for i, chunk in enumerate(
        agent.stream(initial_state, config, stream_mode="values")
    ):
        if "messages" in chunk:
            latest = chunk["messages"][-1]

            # Update TODOs if changed
            if "todos" in chunk and chunk["todos"] != current_todos:
                current_todos = chunk["todos"]
                console.print(create_todo_table(current_todos))
                console.print()

            # Show tool calls
            if hasattr(latest, "tool_calls") and latest.tool_calls:
                step_count += 1
                for tool_call in latest.tool_calls:
                    tool_name = tool_call.get("name")

                    # Special handling for think_tool
                    if tool_name == "think_tool":
                        reflection = tool_call.get("args", {}).get("reflection", "")
                        console.print(
                            Panel(
                                f"[dim]{reflection[:200]}...[/dim]",
                                title=f"💭 Step {step_count}: Thinking",
                                border_style="blue",
                            )
                        )
                    # Delegation tools
                    elif "delegate" in tool_name:
                        args = tool_call.get("args", {})
                        description = args.get("description", "No description")
                        console.print(
                            Panel(
                                f"[yellow]{description}[/yellow]",
                                title=f"🔧 Step {step_count}: {tool_name.replace('_', ' ').title()}",
                                border_style="yellow",
                            )
                        )
                    # Other tools
                    else:
                        console.print(
                            Panel(
                                f"[cyan]{tool_name}[/cyan]",
                                title=f"🔧 Step {step_count}: Tool Call",
                                border_style="cyan",
                            )
                        )

            # Show responses (limit length)
            if (
                hasattr(latest, "content")
                and latest.content
                and len(latest.content) > 10
            ):
                # Skip error messages about missing sandbox
                if "E2B sandbox not available" not in latest.content:
                    preview = latest.content[:300]
                    if len(latest.content) > 300:
                        preview += "..."

                    console.print(
                        Panel(
                            f"[white]{preview}[/white]",
                            title=f"💬 Response",
                            border_style="green",
                        )
                    )
                    console.print()

    # Final TODOs
    if current_todos:
        console.print("\n[bold green]📋 Final TODO Status:[/bold green]")
        console.print(create_todo_table(current_todos))

    console.print("\n[bold green]✅ Workflow complete![/bold green]")

    # Show workspace contents
    console.print("\n[bold cyan]📁 Workspace contents:[/bold cyan]")
    result = sandbox.commands.run("find ~/workspace -type f", timeout=10)
    if result.stdout:
        files = result.stdout.strip().split("\n")
        for f in files:
            console.print(f"  [dim]•[/dim] {f}")

    # Export the report
    console.print("\n[bold cyan]📥 Exporting report...[/bold cyan]")
    try:
        reports = sandbox.commands.run("ls ~/workspace/reports/*.txt", timeout=10)
        if reports.stdout:
            report_file = reports.stdout.strip().split("\n")[0]
            report_content = sandbox.files.read(report_file)

            # Save to local output directory
            import os

            os.makedirs("output/e2b_reports", exist_ok=True)
            output_path = "output/e2b_reports/therapy_note_latest.txt"

            with open(output_path, "w") as f:
                f.write(report_content)

            console.print(f"[bold green]✅ Report saved to: {output_path}[/bold green]")

            # Show preview
            console.print("\n" + "=" * 80)
            console.print(
                Panel.fit(
                    report_content[:800] + ("..." if len(report_content) > 800 else ""),
                    title="📄 Report Preview",
                    border_style="green",
                )
            )
            console.print("=" * 80)
        else:
            console.print(
                "[yellow]⚠️  No report file found in ~/workspace/reports/[/yellow]"
            )
    except Exception as e:
        console.print(f"[red]⚠️  Could not export report: {e}[/red]")


def main():
    """Main orchestration - runs on HOST"""

    console.print("\n[bold magenta]🌟 DEEP AGENT WITH E2B 🌟[/bold magenta]\n")

    # Setup
    sandbox = setup_sandbox()

    try:
        # Create agent
        agent = create_e2b_agent(sandbox)

        # Run workflow
        task = """Please start the workflow for client_001, session_001.

1. Retrieve diagnosis using retrieve_diagnosis and save to /home/user/workspace/data/diagnosis.txt
2. Retrieve subjective analysis using get_subjective_analysis and save to /home/user/workspace/data/subjective.txt
3. Retrieve objective statistics for analysis using get_objective_analysis and save to /home/user/workspace/data/objective.txt
4. Create a therapy note combining all three and save to /home/user/workspace/reports/therapy_note.txt

IMPORTANT: The RAG tools return data but don't save files. You must use execute_bash to save each result."""

        run_workflow(agent, sandbox, task)

        console.print("\n[bold green]🎉 All done![/bold green]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        import traceback

        traceback.print_exc()
    finally:
        console.print("\n[cyan]🧹 Cleaning up sandbox...[/cyan]")
        try:
            # Old e2b versions use kill() instead of close()
            if hasattr(sandbox, "close"):
                sandbox.close()
            elif hasattr(sandbox, "kill"):
                sandbox.kill()
        except Exception as e:
            console.print(f"[yellow]Warning: Error closing sandbox: {e}[/yellow]")
        console.print("[cyan]👋 Goodbye![/cyan]")


if __name__ == "__main__":
    main()
