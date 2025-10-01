"""
Synchronous version of chat response - no generators, no streaming
"""

def sync_chat_response(self, message: str, history):
    """NON-STREAMING synchronous response"""
    if not self.agent:
        return history + [[message, "❌ Agent not initialized"]], ""

    try:
        # Convert to LangChain messages
        messages = []
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})

        # Add current message
        messages.append({"role": "user", "content": message})

        # Get response (NO STREAMING)
        result = self.agent.invoke(
            {"messages": messages},
            config=self.config
        )

        if "messages" in result and result["messages"]:
            response = result["messages"][-1].content
        else:
            response = "No response from agent"

        # Return in old tuple format
        return history + [[message, response]], ""

    except Exception as e:
        error_response = f"❌ Error: {str(e)}"
        return history + [[message, error_response]], ""

print("Use this sync_chat_response function instead of the streaming version")