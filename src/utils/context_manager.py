"""
Smart Context Window Manager for Deep Agents

Prevents context overflow by intelligently trimming old messages while preserving:
- Recent conversation history
- Important system messages
- Current task context
"""

from typing import List, Dict, Any
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)


class SmartContextManager:
    """
    Manages context window by removing oldest messages when approaching token limit.

    Unlike smolagents which uses string concatenation, this works with LangGraph's
    message-based architecture.
    """

    def __init__(self, max_tokens: int = 80000, preserve_last_n: int = 10):
        """
        Args:
            max_tokens: Maximum tokens to keep in context
            preserve_last_n: Always keep the last N messages (recent context)
        """
        self.max_tokens = max_tokens
        self.preserve_last_n = preserve_last_n

    def _estimate_tokens(self, messages: List[BaseMessage]) -> int:
        """
        Rough token estimation (1 token ≈ 0.75 words).
        For better accuracy, use tiktoken, but this is fast enough.
        """
        total_chars = sum(
            len(str(msg.content)) if hasattr(msg, "content") else 0 for msg in messages
        )
        # Rough approximation: 4 chars ≈ 1 token
        return int(total_chars / 4)

    def trim_messages(
        self, messages: List[BaseMessage], system_message: SystemMessage = None
    ) -> List[BaseMessage]:
        """
        Trim messages to fit within token limit while preserving important context.

        Strategy:
        1. Always keep system message
        2. Always keep last N messages (recent context)
        3. Remove oldest messages first until under limit

        Args:
            messages: List of messages to trim
            system_message: Optional system message to always preserve

        Returns:
            Trimmed list of messages
        """
        if not messages:
            return []

        # Estimate current token count
        current_tokens = self._estimate_tokens(messages)

        # If under limit, return as-is
        if current_tokens <= self.max_tokens:
            return messages

        print(
            f"⚠️  Context trimming: {current_tokens} tokens → target {self.max_tokens}"
        )

        # Separate system message if present
        has_system = isinstance(messages[0], SystemMessage)
        system_msg = messages[0] if has_system else system_message
        content_messages = messages[1:] if has_system else messages

        # Always preserve last N messages (recent context)
        preserved_messages = content_messages[-self.preserve_last_n :]
        older_messages = content_messages[: -self.preserve_last_n]

        # Remove oldest messages until we're under the limit
        trimmed_older = []
        for msg in reversed(older_messages):
            # Try adding this message
            candidate = [system_msg] if system_msg else []
            candidate.extend(trimmed_older + [msg] + preserved_messages)

            if self._estimate_tokens(candidate) <= self.max_tokens:
                trimmed_older.insert(0, msg)
            else:
                # Can't fit any more old messages
                break

        # Reconstruct final message list
        final_messages = []
        if system_msg:
            final_messages.append(system_msg)
        final_messages.extend(trimmed_older)
        final_messages.extend(preserved_messages)

        final_tokens = self._estimate_tokens(final_messages)
        removed_count = len(messages) - len(final_messages)
        print(
            f"✅ Trimmed {removed_count} messages: {current_tokens} → {final_tokens} tokens"
        )

        return final_messages

    def create_summary_message(self, removed_messages: List[BaseMessage]) -> AIMessage:
        """
        Create a summary of removed messages to preserve context.

        This is optional but helpful for maintaining awareness of what was removed.
        """
        if not removed_messages:
            return None

        summary_parts = []
        tool_calls = 0
        user_messages = 0

        for msg in removed_messages:
            if isinstance(msg, HumanMessage):
                user_messages += 1
            elif isinstance(msg, ToolMessage):
                tool_calls += 1

        summary = f"[Context Summary: Removed {len(removed_messages)} messages from history including {user_messages} user messages and {tool_calls} tool calls]"

        return AIMessage(content=summary)


class ConversationBuffer:
    """
    Simple buffer for managing conversation history with automatic trimming.

    This can be used as a drop-in replacement for ConversationBufferMemory
    but with automatic context window management.
    """

    def __init__(self, max_tokens: int = 40000, preserve_last_n: int = 10):
        self.manager = SmartContextManager(max_tokens, preserve_last_n)
        self.messages: List[BaseMessage] = []

    def add_message(self, message: BaseMessage):
        """Add a message and auto-trim if needed"""
        self.messages.append(message)
        self.messages = self.manager.trim_messages(self.messages)

    def add_messages(self, messages: List[BaseMessage]):
        """Add multiple messages and auto-trim"""
        self.messages.extend(messages)
        self.messages = self.manager.trim_messages(self.messages)

    def get_messages(self) -> List[BaseMessage]:
        """Get current messages"""
        return self.messages

    def clear(self):
        """Clear all messages"""
        self.messages = []
