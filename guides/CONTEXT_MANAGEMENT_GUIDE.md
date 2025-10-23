## Context Window Management for Deep Agents

### Problem

LLMs have token limits (e.g., 100k for granite4). Long workflows can exceed this:
- ❌ Context overflow crashes the agent
- ❌ Resetting memory loses all progress
- ❌ Manual trimming is tedious

### Solution: Smart Context Manager

**Automatic trimming** that preserves important context while removing old messages.

### How It Works

```python
from src.utils.context_manager import SmartContextManager

manager = SmartContextManager(
    max_tokens=80000,      # Stay under model limit
    preserve_last_n=10     # Always keep last 10 messages
)

# Trim messages when approaching limit
trimmed_messages = manager.trim_messages(messages)
```

**Strategy:**
1. ✅ Always keeps system message (instructions)
2. ✅ Always keeps last N messages (recent context)
3. ✅ Removes oldest messages first (ancient history)
4. ✅ Preserves conversation flow (no mid-conversation cuts)

### Integration with LangGraph

#### Option 1: Manual Trimming in Terminal UI

```python
# In admin_assistant.py

from src.utils.context_manager import SmartContextManager

class AdminAssistant:
    def __init__(self, ...):
        self.context_manager = SmartContextManager(
            max_tokens=80000,
            preserve_last_n=10
        )
        # ... rest of init

    def process_agent_message(self, message: str) -> str:
        # Build message history
        messages = []
        for user_msg, agent_msg in self.conversation_history:
            messages.append(HumanMessage(content=user_msg))
            if agent_msg:
                messages.append(AIMessage(content=agent_msg))

        messages.append(HumanMessage(content=message))

        # TRIM BEFORE SENDING TO AGENT
        trimmed_messages = self.context_manager.trim_messages(messages)

        # Stream with trimmed context
        for chunk in self.agent.stream(
            {"messages": trimmed_messages},  # Use trimmed!
            config=self.config,
            stream_mode="values"
        ):
            # ... process chunks
```

#### Option 2: Automatic Buffer (Drop-in Replacement)

```python
from src.utils.context_manager import ConversationBuffer

class AdminAssistant:
    def __init__(self, ...):
        # Instead of storing conversation_history as list
        self.conversation_buffer = ConversationBuffer(
            max_tokens=80000,
            preserve_last_n=10
        )

    def process_agent_message(self, message: str) -> str:
        # Add new message
        self.conversation_buffer.add_message(
            HumanMessage(content=message)
        )

        # Get auto-trimmed messages
        messages = self.conversation_buffer.get_messages()

        # Use trimmed messages
        for chunk in self.agent.stream(
            {"messages": messages},
            config=self.config,
            stream_mode="values"
        ):
            # ... process chunks

        # Buffer auto-trims after each message!
```

### Example: Before vs After

**Before (Context Overflow):**
```
Message 1-100: Normal workflow
Message 101: ❌ ERROR - Token limit exceeded
Agent resets, loses all progress
```

**After (Smart Trimming):**
```
Message 1-100: Normal workflow
[Automatic trim: Removes messages 1-50]
Message 101-200: ✅ Continues smoothly
[Automatic trim: Removes messages 51-100]
Message 201-300: ✅ Still working
```

### Token Estimation

The context manager uses a fast approximation:
- **4 characters ≈ 1 token**
- Good enough for real-time trimming
- For exact counting, use `tiktoken` (slower)

```python
# Current estimation
def _estimate_tokens(self, messages):
    total_chars = sum(len(str(msg.content)) for msg in messages)
    return int(total_chars / 4)

# For exact counting (optional upgrade):
import tiktoken

def _estimate_tokens_exact(self, messages, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    total_tokens = 0
    for msg in messages:
        total_tokens += len(enc.encode(str(msg.content)))
    return total_tokens
```

### Configuration Recommendations

| Model | Context Window | max_tokens Setting | preserve_last_n |
|-------|----------------|-------------------|-----------------|
| granite4:small-h | 100k | 80,000 | 10-15 |
| gpt-oss:20b | 128k | 100,000 | 15-20 |
| llama3:70b | 128k | 100,000 | 15-20 |

**Why 80% of limit?**
- Leave room for system prompt
- Leave room for tool schemas
- Buffer for token estimation variance

### Advanced: Preserving Important Messages

You can mark certain messages as "important" and preserve them:

```python
class SmartContextManager:
    def trim_messages(self, messages, important_indices=None):
        """
        important_indices: List of message indices to always keep
        """
        if important_indices:
            important_msgs = [messages[i] for i in important_indices]
            other_msgs = [m for i, m in enumerate(messages) if i not in important_indices]

            # Trim only the non-important messages
            trimmed_other = self._trim_list(other_msgs)

            # Merge back in chronological order
            # ... (implementation details)
```

### Debugging Context Issues

**Check token usage:**
```python
from src.utils.context_manager import SmartContextManager

manager = SmartContextManager()
messages = [...]  # Your messages

tokens = manager._estimate_tokens(messages)
print(f"Current context: {tokens} tokens")
print(f"Messages: {len(messages)}")
```

**Monitor trimming:**
```python
# Enable logging in context_manager.py
print(f"⚠️  Context trimming: {current_tokens} tokens → target {self.max_tokens}")
print(f"✅ Trimmed {removed_count} messages: {current_tokens} → {final_tokens} tokens")
```

### Comparison with Smolagents

| Feature | Smolagents | Our Implementation |
|---------|------------|-------------------|
| Data Structure | String concatenation | LangGraph messages |
| Trimming | Pop from list | Smart message pruning |
| Preservation | None | Last N messages |
| Token Counting | Word-based | Char-based (upgradable) |
| Integration | Built-in | Drop-in tool |

### Migration from Virtual Filesystem

The context manager works great with E2B because:
- ✅ Less prompt overhead (no virtual FS docs)
- ✅ More room for actual conversation
- ✅ Tool outputs can be longer (stored in /workspace/)
- ✅ Agents can reference files instead of keeping content in memory

### Next Steps

1. **Test the manager:**
```bash
python -c "from src.utils.context_manager import SmartContextManager; print('✅ Import successful')"
```

2. **Integrate with admin_assistant.py:**
- Add context manager initialization
- Wrap message building with trimming
- Monitor token usage

3. **Run a long workflow:**
- Start workflow
- Let it run >100 messages
- Verify no context overflow
- Check that agent maintains coherence

4. **Fine-tune settings:**
- Adjust `max_tokens` based on model
- Adjust `preserve_last_n` based on workflow
- Monitor for lost context issues

### Context Manager + E2B = Perfect Combo

```python
# Ultimate setup:
context_manager = SmartContextManager(max_tokens=80000)  # Prevent overflow
sandbox = Sandbox()  # Real filesystem for outputs

# Agent runs forever without hitting limits!
# - Old messages trimmed automatically
# - File outputs persisted in sandbox
# - Recent context always preserved
```
