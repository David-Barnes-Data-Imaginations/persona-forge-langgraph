#!/usr/bin/env python3
"""
Minimal chat test to isolate the issue
"""

import gradio as gr
from typing import List

class MinimalChatTest:
    """Minimal chat interface for debugging"""

    def __init__(self):
        print("🔧 Initializing minimal chat test...")

    def simple_response(self, message: str, history: List) -> tuple:
        """Ultra-simple response function for testing"""
        print(f"📝 Processing message: '{message}'")

        if not message.strip():
            print("⚠️ Empty message")
            return history, ""

        try:
            # Add user message
            new_history = history + [{"role": "user", "content": message}]
            print(f"✅ Added user message to history")

            # Simple AI response (no LangGraph)
            ai_response = f"Echo: {message}"
            new_history = new_history + [{"role": "assistant", "content": ai_response}]
            print(f"✅ Added AI response: '{ai_response}'")

            return new_history, ""

        except Exception as e:
            print(f"❌ Error in simple_response: {e}")
            import traceback
            traceback.print_exc()
            return history, ""

    def create_interface(self):
        """Create minimal Gradio interface"""

        with gr.Blocks(title="Minimal Chat Test") as interface:

            gr.Markdown("# 🧪 Minimal Chat Test")

            # Chat interface
            chatbot = gr.Chatbot(
                label="Test Chat",
                height=400,
                type="messages"
            )

            # Input
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type test message...",
                    label="Message",
                    scale=4
                )
                send_btn = gr.Button("Send", scale=1, variant="primary")

            # Wire events
            send_btn.click(
                self.simple_response,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )

            msg_input.submit(
                self.simple_response,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )

        return interface

if __name__ == "__main__":
    print("🧪 Starting minimal chat test...")

    test_chat = MinimalChatTest()
    interface = test_chat.create_interface()

    print("🚀 Launching interface...")
    interface.launch(
        server_name="127.0.0.1",
        server_port=8001,  # Different port
        debug=True
    )