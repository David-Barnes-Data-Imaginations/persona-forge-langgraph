"""
Simplified Gradio chat interface for LangGraph ReactAgent integration with FastAPI.
This interface is designed to work with your existing chat_agent.py setup.
Enhanced with voice functionality (STT/TTS).
"""

import gradio as gr
from typing import Generator, List, Tuple
import asyncio
import base64
import io
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from ..graphs.chat_agent import get_new_agent
from ..io_py.edge.config import LLMConfigVoice
from ..voice_service import voice_service


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

            # Voice status check
            voice_available = voice_service.is_available()
            voice_status_emoji = "🔊" if voice_available else "🔇"

            gr.Markdown(
                f"""
                # 🤖 LangGraph Chat Agent {voice_status_emoji}

                Chat with your LangGraph ReactAgent powered by **{LLMConfigVoice.model_name}**

                This interface connects to your existing psychological analysis workflows.

                **Voice Features Available:** {'✅ STT & TTS enabled' if voice_available else '❌ Voice disabled'}
                """
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

            # Input controls with voice
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type your message here...",
                    label="Message",
                    scale=3,
                    lines=1
                )

                # Voice input (only show if available)
                if voice_available:
                    with gr.Column(scale=1):
                        # Use numpy type for reliable audio capture
                        voice_input = gr.Audio(
                            sources=["microphone"],
                            type="numpy",
                            label="🎤 Voice Input",
                            show_download_button=False,
                            interactive=True
                        )
                        # Manual transcribe button for reliable control
                        transcribe_btn = gr.Button("📝 Transcribe", variant="primary", size="sm")
                else:
                    voice_input = None
                    transcribe_btn = None

                send_btn = gr.Button("Send", scale=1, variant="primary")

            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
                reset_btn = gr.Button("Reset Agent Memory", variant="stop")

                # Voice controls (only show if available)
                if voice_available:
                    tts_enabled = gr.Checkbox(
                        label="🔊 Enable Text-to-Speech",
                        value=False,
                        scale=1
                    )
                    # Test button to verify voice service
                    voice_test_btn = gr.Button("🔧 Test Voice", variant="secondary", size="sm")
                else:
                    tts_enabled = None
                    voice_test_btn = None

            # Audio output - TEMPORARILY DISABLED for debugging
            audio_output = None

            # Status indicator
            status = gr.Textbox(
                value="🟢 Agent Ready" if self.agent else "🔴 Agent Not Initialized",
                label="Status",
                interactive=False
            )

            # Event handlers
            def handle_voice_input(voice_file, current_text):
                """Handle voice input and update text field - simplified approach"""
                try:
                    print(f"🔥 VOICE EVENT TRIGGERED!")
                    print(f"   - File: {voice_file}")

                    # Quick validation
                    if not voice_file:
                        print("⚠️ No voice file provided")
                        return current_text if current_text else ""

                    # Convert current_text to string safely
                    if current_text is None:
                        current_text = ""

                    # For now, just return a test message to verify the event works
                    # This bypasses the heavy Whisper processing that's causing timeouts
                    test_message = " [Voice recorded - processing temporarily disabled for demo]"

                    print(f"📝 Returning test message")
                    return current_text + test_message

                    # TODO: Re-enable actual transcription once event handling is stable
                    # The commented code below would do the actual transcription:

                    # import os
                    # if not os.path.exists(voice_file):
                    #     return current_text + " [File not found]"

                    # from ..voice_service import voice_service as vs
                    # if hasattr(vs, 'whisper_model') and vs.whisper_model:
                    #     result = vs.whisper_model.transcribe(voice_file, language="en")
                    #     transcribed_text = result["text"].strip()
                    #     return current_text + " " + transcribed_text if current_text else transcribed_text

                except Exception as e:
                    print(f"❌ Voice handler error: {e}")
                    return (current_text if current_text else "") + f" [Error: {str(e)[:30]}]"

            def test_voice_service():
                """Test function to verify voice service is working"""
                print("🧪 Testing voice service...")
                try:
                    # Import voice service properly
                    from ..voice_service import voice_service as vs
                    if hasattr(vs, 'whisper_model') and vs.whisper_model:
                        print("✅ Voice service model found")
                        return "✅ Voice service is working! Model loaded successfully."
                    else:
                        print("❌ Voice service model not found")
                        return "❌ Voice service model not available"
                except Exception as e:
                    print(f"❌ Voice service test error: {e}")
                    return f"❌ Voice service error: {str(e)}"

            def transcribe_current_audio(voice_data, current_text):
                """Manually transcribe the current audio data (numpy format)"""
                print("🎙️ MANUAL TRANSCRIBE BUTTON PRESSED!")
                print(f"   Voice data type: {type(voice_data)}")
                print(f"   Current text: {current_text}")

                if voice_data is None:
                    print("⚠️ No audio data to transcribe")
                    return (current_text or "") + " [No audio data]"

                try:
                    # Import the working voice service
                    from ..voice_service import voice_service as vs

                    if not vs.is_available():
                        print("❌ Voice service not available")
                        return (current_text or "") + " [Voice service not ready]"

                    # Use the numpy-based transcription
                    transcribed_text = vs.transcribe_audio_numpy(voice_data)

                    if "error" in transcribed_text.lower():
                        return (current_text or "") + f" [Error: {transcribed_text[:50]}]"

                    print(f"✅ Manual transcription successful: '{transcribed_text}'")

                    # Combine with existing text
                    if current_text and current_text.strip():
                        final_text = f"{current_text} {transcribed_text}"
                    else:
                        final_text = transcribed_text

                    return final_text

                except Exception as e:
                    print(f"❌ Manual transcription error: {e}")
                    import traceback
                    traceback.print_exc()
                    return (current_text or "") + f" [Error: {str(e)[:30]}]"

            def respond(message, history):
                """Handle user message and generate response - SIMPLIFIED"""
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

            # Wire up events - SIMPLIFIED
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

            # Voice transcription - Manual button approach for reliability
            if voice_available and transcribe_btn:
                transcribe_btn.click(
                    transcribe_current_audio,
                    inputs=[voice_input, msg_input],
                    outputs=[msg_input]
                )

            clear_btn.click(
                clear_chat,
                outputs=[chatbot, status]
            )

            reset_btn.click(
                reset_memory,
                outputs=[chatbot, status]
            )

            # Voice button events - TEMPORARILY DISABLED for debugging
            # (All voice events disabled to test basic chat)

        return interface


def create_chat_app() -> gr.Blocks:
    """Factory function to create the chat interface"""
    chat_interface = LangGraphChatInterface()
    return chat_interface.create_interface()


# For standalone testing
if __name__ == "__main__":
    app = create_chat_app()
    app.launch(debug=True, share=False)