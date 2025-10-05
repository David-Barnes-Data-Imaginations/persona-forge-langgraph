"""
E2B Sandbox Tools for Deep Agent

These tools replace the virtual filesystem with real E2B sandbox execution.
Agents can use bash commands and Python code directly.
"""

from typing import Annotated, Optional
from langchain_core.tools import tool
from langchain_core.tools import InjectedToolCallId

# Global sandbox reference (set by run_deep_agent_simple_e2b.py)
_GLOBAL_SANDBOX: Optional[object] = None


def set_global_sandbox(sandbox):
    """Set the global sandbox instance for E2B tools."""
    global _GLOBAL_SANDBOX
    _GLOBAL_SANDBOX = sandbox


def get_global_sandbox():
    """Get the global sandbox instance."""
    return _GLOBAL_SANDBOX


@tool
def execute_bash(
    command: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Execute a bash command in the E2B sandbox.

    Use this to run Linux commands like ls, cat, grep, mkdir, etc.
    The sandbox has a persistent ~/workspace/ directory for storing files.

    Args:
        command: Bash command to execute (e.g., "ls ~/workspace/", "cat file.txt")

    Returns:
        Command output (stdout and stderr)

    Examples:
        - List files: execute_bash("ls -la ~/workspace/")
        - Read file: execute_bash("cat ~/workspace/report.txt")
        - Save data: execute_bash("echo 'data' > ~/workspace/results.txt")
        - Search: execute_bash("grep 'keyword' ~/workspace/*.txt")
    """
    sandbox = get_global_sandbox()

    if not sandbox:
        return "Error: E2B sandbox not available"

    try:
        result = sandbox.commands.run(command, timeout=30)
        output = f"Exit code: {result.exit_code}\n"

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        return output.strip()

    except Exception as e:
        return f"Error executing command: {str(e)}"


@tool
def execute_python(
    code: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Execute Python code in the E2B sandbox.

    Use this for data processing, analysis, or complex operations.
    The code runs in a persistent Python environment with access to ~/workspace/.

    Args:
        code: Python code to execute

    Returns:
        Execution output and any printed results

    Examples:
        - Process data: execute_python("import pandas as pd\\ndf = pd.read_csv('~/workspace/data.csv')\\nprint(df.head())")
        - Write file: execute_python("with open('~/workspace/report.txt', 'w') as f:\\n    f.write('Report content')")
        - Analysis: execute_python("results = [x**2 for x in range(10)]\\nprint(results)")
    """
    sandbox = get_global_sandbox()

    if not sandbox:
        return "Error: E2B sandbox not available"

    try:
        # Use E2B's notebook.exec_cell for Python execution
        result = sandbox.notebook.exec_cell(code)

        output = ""
        if result.logs.stdout:
            output += f"STDOUT:\n{result.logs.stdout}\n"
        if result.logs.stderr:
            output += f"STDERR:\n{result.logs.stderr}\n"
        if result.error:
            output += f"ERROR:\n{result.error.name}: {result.error.value}\n"
        if result.results:
            output += f"RESULTS:\n{result.results}\n"

        return output.strip() if output else "Code executed successfully (no output)"

    except Exception as e:
        return f"Error executing Python code: {str(e)}"


@tool
def list_workspace_files(
    path: str = "~/workspace",
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
) -> str:
    """List files in the E2B sandbox workspace.

    Args:
        path: Directory path to list (default: ~/workspace)

    Returns:
        Directory listing with file details
    """
    sandbox = get_global_sandbox()

    if not sandbox:
        return "Error: E2B sandbox not available"

    try:
        result = sandbox.commands.run(f"ls -lah {path}", timeout=10)
        return result.stdout if result.stdout else "Directory is empty"
    except Exception as e:
        return f"Error listing files: {str(e)}"


@tool
def read_sandbox_file(
    file_path: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Read contents of a file from the E2B sandbox.

    Args:
        file_path: Path to file in sandbox (e.g., "~/workspace/report.txt")

    Returns:
        File contents
    """
    sandbox = get_global_sandbox()

    if not sandbox:
        return "Error: E2B sandbox not available"

    try:
        content = sandbox.files.read(file_path)
        return content if content else "File is empty"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_sandbox_file(
    file_path: str,
    content: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> str:
    """Write content to a file in the E2B sandbox.

    Args:
        file_path: Path to file in sandbox (e.g., "~/workspace/report.txt")
        content: Content to write to file

    Returns:
        Confirmation message
    """
    sandbox = get_global_sandbox()

    if not sandbox:
        return "Error: E2B sandbox not available"

    try:
        sandbox.files.write(file_path, content)
        return f"✅ File written successfully: {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


# E2B tool list (replaces virtual filesystem tools)
E2B_TOOLS = [
    execute_bash,
    execute_python,
    list_workspace_files,
    read_sandbox_file,
    write_sandbox_file,
]
