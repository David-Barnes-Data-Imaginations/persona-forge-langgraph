import re
import subprocess
import sys
import os
from typing import List
from ..graphs.deep_agent import get_new_deep_agent
from typing import Generator, List, Tuple
from ..io_py.edge.config import LLMConfigArchitect
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver


class LangGraphChatInterface:
    """Simplified chat interface for LangGraph ReactAgent"""

    def __init__(self):
        self.agent = None
        self.memory = MemorySaver()
        self.config = {"configurable": {"thread_id": "chat_session_1"}}
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the LangGraph agent"""
        try:
            # Initialize with empty memory stores for now
            short_term_memory = MemorySaver()
            long_term_memory = None  # add a proper store later if required

            self.agent = get_new_deep_agent(
                config=LLMConfigArchitect,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory,
            )
            print("✅ LangGraph agent initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            self.agent = None

    def chat_response(
        self, message: str, history: List[List[str]]
    ) -> Generator[str, None, None]:
        """
        Generate streaming response from the LangGraph agent

        Args:
            message: User's input message
            history: Chat history as list of [user, assistant] pairs

        Yields:
            Streaming response chunks
        """
        if not self.agent:
            yield "❌ Agent not initialized. Please check the configuration."
            return

        try:
            # Convert history to LangChain messages if needed
            messages = []
            for user_msg, assistant_msg in history:
                messages.append(HumanMessage(content=user_msg))
                if assistant_msg:
                    messages.append(AIMessage(content=assistant_msg))

            # Add current message
            messages.append(HumanMessage(content=message))

            # Stream response from agent
            full_response = ""
            for chunk in self.agent.stream(
                {"messages": messages}, config=self.config, stream_mode="values"
            ):
                if "messages" in chunk:
                    latest_message = chunk["messages"][-1]
                    if hasattr(latest_message, "content") and latest_message.content:
                        content = latest_message.content
                        if (
                            content != full_response
                        ):  # Only yield if content has changed
                            full_response = content
                            yield content

            # If no streaming occurred, get the final response
            if not full_response:
                result = self.agent.invoke({"messages": messages}, config=self.config)
                if "messages" in result and result["messages"]:
                    final_content = result["messages"][-1].content
                    yield final_content

        except Exception as e:
            error_msg = f"❌ Error getting response: {str(e)}"
            print(error_msg)
            yield error_msg


"""
admin_assistant: An provides an interface for the deep agent workflow with command execution safety features.

This module provides a command-line interface for interacting with the deep agent
while safely executing shell commands. It includes command classification,
extraction, and execution with appropriate safety checks based on command risk level.
"""


class CommandClassifier:
    """
    Classifies shell commands into different safety categories.

    Commands are classified as:
    - safe: Commands that are read-only or have minimal system impact
    - sudo: Commands that require elevated privileges
    - dangerous: Commands that could potentially harm the system
    - unknown: Commands that don't match known patterns
    """

    SAFE_COMMANDS = [
        "ls",
        "cd",
        "cat",
        "pwd",
        "echo",
        "which",
        "whereis",
        "man",
        "help",
        "grep",
        "find",
        "head",
        "tail",
        "less",
        "more",
        "wc",
        "sort",
        "uniq",
        "date",
        "cal",
        "whoami",
        "id",
        "groups",
        "history",
        "alias",
        "type",
        "file",
        "stat",
        "du",
        "df",
        "free",
        "uptime",
        "ps",
        "top",
        "htop",
        "git status",
        "git log",
        "git diff",
        "git show",
        "git branch",
    ]

    SUDO_COMMANDS = [
        "sudo",
        "su",
        "passwd",
        "usermod",
        "groupmod",
        "chown",
        "chmod",
        "mount",
        "umount",
        "systemctl",
        "service",
        "apt",
        "yum",
        "dnf",
        "pacman",
        "snap",
        "pip install",
        "npm install",
        "gem install",
    ]

    DANGEROUS_COMMANDS = [
        "rm -rf",
        "dd",
        "mkfs",
        "fdisk",
        "parted",
        "shred",
        "wipefs",
        ":(){:|:&};:",
        ":(){ :|:& };:",
        "fork()",
        "while true",
        "> /dev/",
        "truncate",
        ">/dev/sda",
        ">/dev/sd",
    ]

    FILESYSTEM_DESTRUCTIVE = ["rm", "rmdir", "mv", "cp", "ln", "unlink"]

    @classmethod
    def classify_command(cls, cmd: str) -> str:
        """
        Classify a shell command into a safety category.

        Args:
            cmd (str): The shell command to classify

        Returns:
            str: Classification category - "safe", "sudo", "dangerous", or "unknown"
        """
        cmd_lower = cmd.lower().strip()

        # Check for dangerous patterns first
        if any(danger in cmd_lower for danger in cls.DANGEROUS_COMMANDS):
            return "dangerous"

        # Check for filesystem operations that could be destructive
        if any(cmd_lower.startswith(fs_cmd) for fs_cmd in cls.FILESYSTEM_DESTRUCTIVE):
            # Check if it's operating on important directories
            if any(
                path in cmd_lower
                for path in ["/", "/home", "/etc", "/usr", "/var", "/boot"]
            ):
                return "dangerous"
            return "sudo"

        # Check for sudo commands
        if any(cmd_lower.startswith(sudo_cmd) for sudo_cmd in cls.SUDO_COMMANDS):
            return "sudo"

        # Check for safe commands
        if any(cmd_lower.startswith(safe_cmd) for safe_cmd in cls.SAFE_COMMANDS):
            return "safe"

        return "unknown"


class CommandExtractor:
    """
    Extracts shell commands from AI-generated text responses.

    This class provides functionality to parse and extract executable shell commands
    from both code blocks and inline code in AI responses.
    """

    @staticmethod
    def extract_commands(text: str) -> List[str]:
        """
        Extract command blocks from AI response text.

        Args:
            text (str): The AI-generated text response to parse

        Returns:
            List[str]: A list of extracted shell commands
        """
        # Pattern for code blocks
        code_blocks = re.findall(r"```(?:bash|sh|shell)?\n(.*?)```", text, re.DOTALL)

        # Pattern for inline commands (backticks)
        inline_commands = re.findall(r"`([^`\n]+)`", text)

        commands = []

        # Process code blocks
        for block in code_blocks:
            lines = block.strip().split("\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):  # Skip comments
                    commands.append(line)

        # Process inline commands (filter out non-commands)
        for cmd in inline_commands:
            cmd = cmd.strip()
            # Simple heuristic: if it contains spaces and starts with a common command
            if " " in cmd and any(
                cmd.startswith(c)
                for c in [
                    "ls",
                    "cd",
                    "cat",
                    "grep",
                    "find",
                    "mkdir",
                    "rm",
                    "cp",
                    "mv",
                    "sudo",
                    "touch",
                ]
            ):
                commands.append(cmd)

        return commands


class GumCommandInterface:
    """
    Interface for handling command execution with safety checks using Gum for UI.

    This class provides a user-friendly interface for executing shell commands
    with appropriate safety checks based on command classification. It uses the
    Gum CLI tool for UI elements when available, with fallbacks to standard input.
    """

    def __init__(self, backend_module):
        """
        Initialize the GumCommandInterface.

        Args:
            backend_module: The AI backend module to use for queries
        """
        self.backend = backend_module
        self.classifier = CommandClassifier()
        self.extractor = CommandExtractor()

    def gum_confirm(self, message: str) -> bool:
        """
        Show a confirmation dialog using Gum or fallback to standard input.

        Args:
            message (str): The message to display in the confirmation dialog

        Returns:
            bool: True if confirmed, False otherwise
        """
        try:
            # Let gum draw its UI directly on the terminal.
            # The return code tells us if the user confirmed.
            result = subprocess.run(
                ["gum", "confirm", message],
                stdout=subprocess.DEVNULL,  # We don't need stdout from 'confirm'
                stderr=sys.stderr,
            )
            return result.returncode == 0
        except FileNotFoundError:
            # Fallback to simple input if gum is not available
            response = input(f"{message} (y/N): ").strip().lower()
            return response in ["y", "yes"]

    def gum_input(self, placeholder: str, password: bool = False) -> str:
        """
        Get user input using Gum or fallback to standard input.

        Args:
            placeholder (str): The placeholder text to display in the input field
            password (bool, optional): Whether to hide input (for passwords). Defaults to False.

        Returns:
            str: The user input text
        """
        try:
            cmd = ["gum", "input", "--placeholder", placeholder]
            if password:
                cmd.append("--password")
            # Let gum draw its UI on stderr, but capture stdout for the result.
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=sys.stderr, text=True, check=True
            )
            return result.stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(
                f"Warning: 'gum' command failed or not found ({e}), falling back to standard input.",
                file=sys.stderr,
            )
            # Fallback to simple input if gum is not available or fails
            if password:
                import getpass

                return getpass.getpass(f"{placeholder}: ")
            else:
                return input(f"{placeholder}: ")

    def gum_choose(self, options: List[str], header: str) -> str:
        """
        Let user choose from a list of options using Gum or fallback to standard input.
        An option to exit without running any command is automatically added.

        Args:
            options (List[str]): List of options to choose from
            header (str): Header text to display above the options

        Returns:
            str: The selected option, or a special value to indicate exit.
        """
        EXIT_OPTION = "Don't run a command"

        # For gum, put the commands first, then the exit option
        full_options = options + [EXIT_OPTION]

        try:
            cmd = ["gum", "choose", "--header", header] + full_options
            # Let gum draw its UI on stderr, but capture stdout for the result.
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=sys.stderr, text=True, check=True
            )
            selected = result.stdout.strip()

            # If the user cancels (e.g., with Esc or Ctrl+C), gum returns an empty string.
            if not selected:
                return EXIT_OPTION
            return selected

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(
                f"Warning: 'gum' command failed or not found ({e}), falling back to standard input.",
                file=sys.stderr,
            )
            # Fallback to simple menu if gum is not available
            print(f"\n{header}")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            # Use '0' for the exit option in the manual fallback.
            print(f"0. {EXIT_OPTION}")

            while True:
                try:
                    choice = int(input("Choose option: "))
                    if choice == 0:
                        return EXIT_OPTION  # Fixed: return EXIT_OPTION instead of None
                    elif 1 <= choice <= len(options):
                        return options[choice - 1]
                    else:
                        print("Invalid choice, try again.")
                except ValueError:
                    print("Please enter a number.")

    def explain_command_risks(
        self, command: str, history: List[str], system_info: str
    ) -> str:
        """
        Ask the AI to explain the risks of a dangerous command.

        Args:
            command (str): The command to analyze for risks
            history (List[str]): Terminal command history for context
            system_info (str): System information for context

        Returns:
            str: AI-generated explanation of the command's risks
        """
        risk_prompt = f"Explain the potential risks and dangers of running this command: '{command}'. What could go wrong? What precautions should be taken?"
        return self.backend.query(risk_prompt, history, system_info)

    def handle_command_execution(
        self, command: str, history: List[str], system_info: str
    ) -> bool:
        """
        Handle the execution of a command based on its safety classification.

        This method classifies the command, presents appropriate confirmation dialogs
        based on the risk level, and executes the command if confirmed by the user.

        Args:
            command (str): The command to execute
            history (List[str]): Terminal command history for context
            system_info (str): System information for context

        Returns:
            bool: True if command executed successfully, False otherwise
        """
        classification = self.classifier.classify_command(command)

        print(f"\n📋 Command: {command}")
        print(f"🔍 Classification: {classification}")

        if classification == "safe":
            if self.gum_confirm(f"Run safe command: {command}?"):
                return self.execute_command(command)

        elif classification == "sudo":
            if self.gum_confirm(
                f"⚠️  This command requires elevated privileges: {command}\nProceed?"
            ):
                # Don't ask for password here - let the system handle it
                return self.execute_command(command)

        elif classification == "dangerous":
            choice = self.gum_choose(
                [
                    "🚨 Explain risks first",
                    "🔒 I understand the risks, proceed anyway",
                    "❌ Cancel",
                ],
                f"⚠️  DANGEROUS COMMAND DETECTED: {command}",
            )

            if choice and choice.startswith("🚨"):
                # Show risk explanation
                risks = self.explain_command_risks(command, history, system_info)
                print(f"\n🚨 RISK ANALYSIS:\n{risks}\n")

                if self.gum_confirm(
                    "After reading the risks, do you still want to proceed?"
                ):
                    return self.execute_command(command)

            elif choice and choice.startswith("🔒"):
                if self.gum_confirm(
                    "Are you sure you want to proceed with this dangerous command?"
                ):
                    return self.execute_command(command)

        else:  # unknown
            if self.gum_confirm(
                f"⚠️  Unknown command classification: {command}\nProceed with caution?"
            ):
                return self.execute_command(command)

        return False

    def execute_command(self, command: str) -> bool:
        """
        Execute a shell command using bash and display its output.

        This method runs the command in a bash shell (not sh) to ensure compatibility
        with bash-specific commands like 'source' and 'cd'.

        Args:
            command (str): The shell command to execute

        Returns:
            bool: True if command executed successfully (return code 0), False otherwise
        """
        try:
            print(f"\n🚀 Executing: {command}")

            # Use bash explicitly instead of default /bin/sh
            # This fixes issues with 'source', 'cd', and other bash-specific commands
            result = subprocess.run(
                ["/bin/bash", "-c", command],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
            )

            if result.stdout:
                print("📤 Output:")
                print(result.stdout)

            if result.stderr:
                print("⚠️  Errors:")
                print(result.stderr)

            return result.returncode == 0

        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return False

    def process_ai_response(self, response: str, history: List[str], system_info: str):
        """
        Process AI response, extract commands, and let the user choose which to execute.

        This method extracts shell commands from the AI response, displays them to the user,
        and allows the user to select which command(s) to execute.

        Args:
            response (str): The AI-generated text response
            history (List[str]): Terminal command history for context
            system_info (str): System information for context

        Returns:
            None
        """
        # First, show the AI's response to the user
        print(response)

        # Extract commands from AI response
        commands = self.extractor.extract_commands(response)

        if not commands:
            print("\nNo executable commands found in the response.")
            return

        print(f"\n🔍 Found {len(commands)} command(s) in response:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd}")

        # Let user choose which command to run
        choice = self.gum_choose(commands, "Choose a command to execute:")

        # Handle the choice
        if choice == "Don't run a command":
            print("No command executed.")
            return

        # If we get here, choice should be one of the actual commands
        selected_command = choice

        # Now execute the selected command
        self.handle_command_execution(selected_command, history, system_info)


def main():
    """
    Main entry point for the admin_assistant part of the application.

    Processes command-line arguments, initializes the appropriate AI backend,
    queries the AI with the user's prompt, and handles the response including
    any shell commands that need to be executed.

    Usage: davidgnome <your query>

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: admin_assistant <your query>")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])

    chat_interface = LangGraphChatInterface()

    # Create the gum interface (no Flask dependency)
    gum_interface = GumCommandInterface(chat_interface)

    # Need to change this to handle the agents responses
    response = deep_agent.query(prompt)

    # Process the response and handle any commands
    gum_interface.process_ai_response(response)


if __name__ == "__main__":
    main()
