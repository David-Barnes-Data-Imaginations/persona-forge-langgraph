#!/usr/bin/env python3
"""
Launcher script for the Deep Agent Terminal UI

Run this script to start the Deep Agent psychological analysis workflow.

Usage:
    python run_deep_agent.py
    OR
    chmod +x run_deep_agent.py && ./run_deep_agent.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.terminal.admin_assistant import main

if __name__ == "__main__":
    main()