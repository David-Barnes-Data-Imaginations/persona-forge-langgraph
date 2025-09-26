"""
Simplified Gradio chat interface for LangGraph ReactAgent integration with FastAPI.
This interface is designed to work with your existing chat_agent.py setup.
"""

import gradio as gr
from typing import Generator, List, Tuple
import asyncio
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from ..graphs.chat_agent import get_new_agent
from ..io_py.edge.config import LLMConfigVoice


class LangGraphChatInterface:
    """Simplified chat interface for LangGraph ReactAgent"""

    def __init__(self):
        self.agent = None
        self.memory = MemorySaver()
        self.config = {
            "configurable": {"thread_id": "chat_session_1"}
        }
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the LangGraph agent"""
        try:
            # Initialize with empty memory stores for now
            short_term_memory = MemorySaver()
            long_term_memory = None  # You can add a proper store later

            self.agent = get_new_agent(
                config=LLMConfigVoice,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory
            )
            print("✅ LangGraph agent initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing agent: {e}")
            self.agent = None

    def chat_response(self, message: str, history: List[List[str]]) -> Generator[str, None, None]:
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
            response_chunks = []
            for chunk in self.agent.stream(
                {"messages": messages},
                config=self.config,
                stream_mode="values"
            ):
                if "messages" in chunk:
                    latest_message = chunk["messages"][-1]
                    if hasattr(latest_message, 'content'):
                        content = latest_message.content
                        if content and content not in response_chunks:
                            response_chunks.append(content)
                            yield content

            # If no streaming occurred, get the final response
            if not response_chunks:
                result = self.agent.invoke(
                    {"messages": messages},
                    config=self.config
                )
                if "messages" in result and result["messages"]:
                    final_content = result["messages"][-1].content
                    yield final_content

        except Exception as e:
            error_msg = f"❌ Error getting response: {str(e)}"
            print(error_msg)
            yield error_msg

    def create_interface(self) -> gr.Blocks:
        """Create the Gradio chat interface"""

        with gr.Blocks(
            title="LangGraph Chat Agent",
            theme=gr.themes.Soft(),
            css="""
            .gradio-container {
                max-width: 800px !important;
                margin: auto !important;
            }
            .chat-bubble {
                max-width: 70% !important;
            }
            """
        ) as interface:

            gr.Markdown(
                """
                # 🤖 LangGraph Chat Agent

                Chat with your LangGraph ReactAgent powered by **{}**

                This interface connects to your existing psychological analysis workflows.
                """.format(LLMConfigVoice.model_name)
            )

            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat with Agent",
                height=500,
                bubble_full_width=False,
                show_copy_button=True,
                layout="panel",
                type="messages"
            )

            # Input controls
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type your message here...",
                    label="Message",
                    scale=4,
                    lines=1
                )
                send_btn = gr.Button("Send", scale=1, variant="primary")

            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
                reset_btn = gr.Button("Reset Agent Memory", variant="stop")

            # Status indicator
            status = gr.Textbox(
                value="🟢 Agent Ready" if self.agent else "🔴 Agent Not Initialized",
                label="Status",
                interactive=False
            )

            # Event handlers
            def respond(message, history):
                """Handle user message and generate response"""
                if not message.strip():
                    return history, ""

                # Add user message to history
                history = history + [{"role": "user", "content": message}]

                # Get response from agent
                response = ""
                # Convert history to old format for chat_response
                history_tuples = []
                for i in range(0, len(history)-1, 2):
                    user_msg = history[i]["content"] if i < len(history) else ""
                    assistant_msg = history[i+1]["content"] if i+1 < len(history) else ""
                    history_tuples.append([user_msg, assistant_msg])

                for chunk in self.chat_response(message, history_tuples):
                    response = chunk
                    # Update or add assistant response
                    if len(history) > 0 and history[-1]["role"] == "user":
                        history = history + [{"role": "assistant", "content": response}]
                    else:
                        history[-1]["content"] = response
                    yield history, ""

                return history, ""

            def clear_chat():
                """Clear the chat history"""
                return [], "🟢 Chat cleared"

            def reset_memory():
                """Reset the agent's memory"""
                try:
                    # Reinitialize the agent to clear memory
                    self._initialize_agent()
                    return [], "🟢 Agent memory reset"
                except Exception as e:
                    return [], f"❌ Error resetting memory: {str(e)}"

            # Wire up events
            send_btn.click(
                respond,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )

            msg_input.submit(
                respond,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, msg_input]
            )

            clear_btn.click(
                clear_chat,
                outputs=[chatbot, status]
            )

            reset_btn.click(
                reset_memory,
                outputs=[chatbot, status]
            )

        return interface


def create_chat_app() -> gr.Blocks:
    """Factory function to create the chat interface"""
    chat_interface = LangGraphChatInterface()
    return chat_interface.create_interface()


# For standalone testing
if __name__ == "__main__":
    app = create_chat_app()
    app.launch(debug=True, share=False)