#!/usr/bin/env python3
"""
Admin Assistant Terminal UI for Deep Agent Workflow

A terminal-based interface for the Deep Agent psychological analysis workflow.
Provides a clean, interactive UI using Rich for formatting and Prompt Toolkit for input.
"""

import sys
import subprocess
from typing import Optional, Dict, Any
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from rich.layout import Layout
from rich.text import Text

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver

from ..graphs.deep_agent import get_new_deep_agent
from ..io_py.edge.config import LLMConfigArchitect


class DeepAgentTerminalUI:
    """Terminal UI for the Deep Agent workflow"""

    def __init__(self):
        self.console = Console()
        self.agent = None
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "deep_agent_session"}}
        self.conversation_history = []
        self.session_id = "session_001"  # Default session

        # Command execution safety lists
        self.safe_commands = ["ls", "cat", "pwd", "echo", "grep", "find", "head", "tail"]
        self.requires_confirmation = ["rm", "mv", "cp", "mkdir", "touch"]
        self.blacklisted = ["rm -rf /", "dd if=", "mkfs", ":(){:|:&};:"]

    def initialize_agent(self):
        """Initialize the Deep Agent"""
        with self.console.status("[bold cyan]Initializing Deep Agent...", spinner="dots"):
            try:
                short_term_memory = MemorySaver()
                long_term_memory = None  # Can be configured later if needed

                self.agent = get_new_deep_agent(
                    config=LLMConfigArchitect,
                    short_term_memory=short_term_memory,
                    long_term_memory=long_term_memory,
                )

                self.console.print(Panel(
                    "[bold green]✓[/bold green] Deep Agent initialized successfully",
                    border_style="green",
                    box=box.ROUNDED
                ))
                return True

            except Exception as e:
                self.console.print(Panel(
                    f"[bold red]✗[/bold red] Error initializing agent: {e}",
                    border_style="red",
                    box=box.ROUNDED
                ))
                return False

    def show_welcome_banner(self):
        """Display welcome banner with system info"""
        banner = Text()
        banner.append("╔═══════════════════════════════════════════════╗\n", style="cyan bold")
        banner.append("║  ", style="cyan bold")
        banner.append("SENTIMENT SUITE - DEEP AGENT TERMINAL", style="magenta bold")
        banner.append("  ║\n", style="cyan bold")
        banner.append("║  ", style="cyan bold")
        banner.append("Psychological Analysis & Report Generation", style="white")
        banner.append("   ║\n", style="cyan bold")
        banner.append("╚═══════════════════════════════════════════════╝", style="cyan bold")

        self.console.print(banner)
        self.console.print()

        # Show quick help
        help_table = Table(show_header=False, box=box.SIMPLE, border_style="dim")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")

        help_table.add_row("/help", "Show available commands")
        help_table.add_row("/stats", "Show graph statistics")
        help_table.add_row("/todos", "Show current task list")
        help_table.add_row("/session <id>", "Change session ID")
        help_table.add_row("/clear", "Clear conversation history")
        help_table.add_row("/exit", "Exit the application")

        self.console.print(Panel(
            help_table,
            title="[bold cyan]Quick Commands[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))
        self.console.print()

    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands starting with /

        Returns:
            True if command was handled, False to continue normal processing
        """
        if not user_input.startswith("/"):
            return False

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "/help":
            self.show_help()
        elif command == "/stats":
            self.show_statistics()
        elif command == "/todos":
            if hasattr(self, '_last_agent_state') and self._last_agent_state:
                self.display_todos(self._last_agent_state)
            else:
                self.console.print("[yellow]No tasks to display yet. Start a conversation with the agent first.[/yellow]")
        elif command == "/session":
            if args:
                self.session_id = args.strip()
                self.console.print(f"[green]✓[/green] Session changed to: {self.session_id}")
            else:
                self.console.print(f"[yellow]Current session:[/yellow] {self.session_id}")
        elif command == "/clear":
            self.conversation_history = []
            self.console.clear()
            self.console.print("[green]✓[/green] Conversation history cleared")
        elif command == "/exit":
            self.console.print("[cyan]Goodbye![/cyan]")
            sys.exit(0)
        else:
            self.console.print(f"[red]Unknown command:[/red] {command}")
            self.console.print("Type [cyan]/help[/cyan] for available commands")

        return True

    def show_help(self):
        """Display comprehensive help information"""
        help_md = """
# Deep Agent Commands

## Special Commands
- `/help` - Show this help message
- `/stats` - Display graph statistics for current session
- `/todos` - Show current agent task list and progress
- `/session <id>` - Change the active session ID
- `/clear` - Clear conversation history
- `/exit` - Exit the application

## Workflow Commands
You can ask the agent to:
- **Start Analysis** - "Start the psychological analysis workflow"
- **Generate Report** - "Generate the progress notes report"
- **Research Topics** - "Research recent studies on [topic]"
- **Query Statistics** - "What are the most common emotions?"
- **Find Extremes** - "Show me the highest neuroticism scores"

## File Operations
The agent can create files with human-in-the-loop confirmation for:
- Progress notes reports
- Analysis summaries
- Research compilations

Type your request naturally, and the agent will guide you through the workflow.
        """

        self.console.print(Panel(
            Markdown(help_md),
            title="[bold cyan]Help[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))

    def show_statistics(self):
        """Quick statistics display"""
        with self.console.status("[bold cyan]Fetching statistics...", spinner="dots"):
            try:
                from ..tools.hybrid_rag_tools import get_graph_statistics

                stats = get_graph_statistics(self.session_id)

                self.console.print(Panel(
                    stats,
                    title=f"[bold cyan]Statistics for {self.session_id}[/bold cyan]",
                    border_style="cyan",
                    box=box.ROUNDED
                ))
            except Exception as e:
                self.console.print(f"[red]Error fetching statistics:[/red] {e}")

    def check_file_operation_safety(self, operation: str, file_path: str) -> bool:
        """
        Human-in-the-loop check for file operations

        Args:
            operation: Type of operation (create, write, delete)
            file_path: Path to the file

        Returns:
            True if operation is approved, False otherwise
        """
        self.console.print()

        # Show operation details
        op_table = Table(show_header=False, box=box.SIMPLE)
        op_table.add_column("Property", style="cyan bold")
        op_table.add_column("Value", style="white")

        op_table.add_row("Operation", operation.upper())
        op_table.add_row("File Path", file_path)
        op_table.add_row("Absolute Path", str(Path(file_path).resolve()))

        self.console.print(Panel(
            op_table,
            title="[bold yellow]⚠ File Operation Request[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))

        # Ask for confirmation
        return Confirm.ask("Do you want to proceed with this file operation?", default=False)

    def process_agent_message(self, message: str) -> str:
        """
        Process message through the Deep Agent

        Args:
            message: User's message

        Returns:
            Agent's response
        """
        if not self.agent:
            return "❌ Agent not initialized. Please restart the application."

        try:
            # Build message history
            messages = []
            for user_msg, agent_msg in self.conversation_history:
                messages.append(HumanMessage(content=user_msg))
                if agent_msg:
                    messages.append(AIMessage(content=agent_msg))

            # Add current message
            messages.append(HumanMessage(content=message))

            # Invoke agent with streaming
            response = ""
            final_state = None
            displayed_tool_call_ids = set()  # Track displayed tool calls

            for chunk in self.agent.stream(
                {"messages": messages},
                config=self.config,
                stream_mode="values"
            ):
                final_state = chunk  # Keep track of final state
                if "messages" in chunk:
                    # Check all messages for tool calls, not just the latest
                    for message in chunk["messages"]:
                        # Display tool calls (especially think_tool)
                        if hasattr(message, "tool_calls") and message.tool_calls:
                            for tool_call in message.tool_calls:
                                # Create unique ID for this tool call
                                tool_call_id = tool_call.get("id", str(tool_call))

                                # Only display if we haven't shown this one yet
                                if tool_call_id not in displayed_tool_call_ids:
                                    if tool_call.get("name") == "think_tool":
                                        reflection = tool_call.get("args", {}).get("reflection", "")
                                        if reflection:
                                            self.console.print()
                                            self.console.print(Panel(
                                                f"[dim]{reflection}[/dim]",
                                                title="[bold magenta]💭 Agent Thinking[/bold magenta]",
                                                border_style="magenta",
                                                box=box.ROUNDED
                                            ))
                                    displayed_tool_call_ids.add(tool_call_id)

                    # Capture final response from latest message
                    latest_message = chunk["messages"][-1]
                    if hasattr(latest_message, "content") and latest_message.content:
                        response = latest_message.content

            # Store final state for TODO display
            self._last_agent_state = final_state

            # If no streaming response, get final result
            if not response:
                result = self.agent.invoke({"messages": messages}, config=self.config)
                if "messages" in result and result["messages"]:
                    response = result["messages"][-1].content
                # Update state for TODO display
                self._last_agent_state = result

            return response

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.console.print(f"\n[red]Full error traceback:[/red]\n{error_details}")
            return f"❌ Error processing message: {str(e)}"

    def display_todos(self, state: Dict[str, Any]):
        """Display TODO list from agent state"""
        if not state or "todos" not in state or not state["todos"]:
            return

        todos = state["todos"]

        # Create TODO table
        todo_table = Table(show_header=True, box=box.ROUNDED, border_style="blue")
        todo_table.add_column("Status", style="bold", width=12)
        todo_table.add_column("Task", style="white")

        # Status emoji mapping
        status_icons = {
            "pending": "⏳ Pending",
            "in_progress": "🔄 In Progress",
            "completed": "✅ Done"
        }

        # Color mapping
        status_colors = {
            "pending": "yellow",
            "in_progress": "cyan",
            "completed": "green"
        }

        for todo in todos:
            status = todo.get("status", "pending")
            content = todo.get("content", "")

            status_text = Text(status_icons.get(status, status))
            status_text.stylize(status_colors.get(status, "white"))

            todo_table.add_row(status_text, content)

        self.console.print()
        self.console.print(Panel(
            todo_table,
            title="[bold blue]📋 Task Progress[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        ))

    def display_agent_response(self, response: str):
        """Display agent response with rich formatting"""
        self.console.print()

        # Check if response contains markdown-like formatting
        if any(marker in response for marker in ["#", "**", "*", "-", "`"]):
            self.console.print(Panel(
                Markdown(response),
                title="[bold green]Agent Response[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2)
            ))
        else:
            self.console.print(Panel(
                response,
                title="[bold green]Agent Response[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2)
            ))

    def run(self):
        """Main application loop"""
        # Show welcome banner
        self.show_welcome_banner()

        # Initialize agent
        if not self.initialize_agent():
            return

        self.console.print("[dim]Type your message or use /help for commands[/dim]\n")

        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()

                if not user_input:
                    continue

                # Handle special commands
                if self.handle_command(user_input):
                    continue

                # Process through agent
                response = self.process_agent_message(user_input)

                # Display TODOs if available
                if hasattr(self, '_last_agent_state') and self._last_agent_state:
                    self.display_todos(self._last_agent_state)

                # Display response
                self.display_agent_response(response)

                # Store in conversation history
                self.conversation_history.append((user_input, response))

            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Interrupted by user[/yellow]")
                if Confirm.ask("Do you want to exit?", default=True):
                    self.console.print("[cyan]Goodbye![/cyan]")
                    break
                else:
                    continue

            except Exception as e:
                self.console.print(f"\n[red]Error:[/red] {e}")
                if Confirm.ask("Continue?", default=True):
                    continue
                else:
                    break


def main():
    """Entry point for the admin assistant terminal UI"""
    try:
        ui = DeepAgentTerminalUI()
        ui.run()
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Fatal error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()