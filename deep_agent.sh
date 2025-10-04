#!/bin/bash
# Deep Agent CLI Launcher
# This script allows you to run the deep agent from anywhere by typing 'deep_agent'

# Get the real path of this script (resolves symlinks)
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# Change to project directory
cd "$SCRIPT_DIR" || exit 1

# Run the deep agent with uv
uv run python run_deep_agent.py "$@"
