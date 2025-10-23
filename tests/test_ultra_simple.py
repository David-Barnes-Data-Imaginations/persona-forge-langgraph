#!/usr/bin/env python3
"""
Ultra-simple Gradio test - completely synchronous
"""

import gradio as gr

def ultra_simple_echo(message, history):
    """Ultra-simple synchronous function"""
    print(f"🔵 Function called with: '{message}'")

    if not message:
        print("⚠️ Empty message")
        return history, ""

    # Simple synchronous response - no async, no generators, no complexity
    response = f"Echo: {message}"
    new_history = history + [[message, response]]

    print(f"✅ Returning: {new_history}")
    return new_history, ""

# Create ultra-simple interface
with gr.Blocks() as demo:
    gr.Markdown("# Ultra Simple Test")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type here...")

    msg.submit(
        ultra_simple_echo,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

if __name__ == "__main__":
    print("🧪 Ultra-simple test starting...")
    demo.launch(
        server_name="127.0.0.1",
        server_port=8002,
        debug=True,
        share=False
    )