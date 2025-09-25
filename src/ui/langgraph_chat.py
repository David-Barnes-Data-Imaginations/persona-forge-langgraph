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
                    # Try a different approach - use both Audio and File upload
                    with gr.Column(scale=1):
                        voice_input = gr.Audio(
                            sources=["microphone"],
                            type="filepath",
                            label="🎤 Voice Input",
                            show_download_button=False,
                            interactive=True
                        )
                        # Alternative: File upload for voice files
                        voice_file_input = gr.File(
                            file_types=[".wav", ".mp3", ".m4a"],
                            label="📁 Or upload audio file",
                            visible=True
                        )
                else:
                    voice_input = None
                    voice_file_input = None

                send_btn = gr.Button("Send", scale=1, variant="primary")

            # Control buttons
            with gr.Row():
                clear_btn = gr.Button("Clear Chat", variant="secondary")
                reset_btn = gr.Button("Reset Agent Memory", variant="stop")

                # TTS toggle and voice test (only show if available)
                if voice_available:
                    tts_enabled = gr.Checkbox(
                        label="🔊 Enable Text-to-Speech",
                        value=False,
                        scale=1
                    )
                    # Add a test button to verify voice processing works
                    voice_test_btn = gr.Button("🔧 Test Voice", variant="secondary", size="sm")
                    # Add manual transcription button
                    transcribe_btn = gr.Button("📝 Transcribe Audio", variant="primary", size="sm")
                else:
                    tts_enabled = None
                    voice_test_btn = None
                    transcribe_btn = None

            # Audio output for TTS (hidden by default)
            if voice_available:
                audio_output = gr.Audio(
                    label="🔊 Agent Speech",
                    visible=False,
                    autoplay=True
                )
            else:
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

            def transcribe_current_audio(voice_file, current_text):
                """Manually transcribe the current audio file"""
                print("🎙️ MANUAL TRANSCRIBE BUTTON PRESSED!")

                if not voice_file:
                    print("⚠️ No audio file to transcribe")
                    return current_text + " [No audio file]"

                try:
                    print(f"📁 Transcribing file: {voice_file}")

                    from ..voice_service import voice_service as vs

                    if hasattr(vs, 'whisper_model') and vs.whisper_model:
                        result = vs.whisper_model.transcribe(voice_file, language="en")
                        transcribed_text = result["text"].strip()
                        print(f"✅ Manual transcription successful: '{transcribed_text}'")

                        final_text = current_text + " " + transcribed_text if current_text else transcribed_text
                        return final_text
                    else:
                        return current_text + " [Voice service not ready]"

                except Exception as e:
                    print(f"❌ Manual transcription error: {e}")
                    return current_text + f" [Transcription error: {str(e)[:30]}]"

            def respond(message, history, tts_enabled_val=False):
                """Handle user message and generate response"""
                if not message.strip():
                    return history, "", None

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

                    # Generate TTS if enabled
                    audio_file = None
                    if tts_enabled_val and voice_available and response.strip():
                        try:
                            audio_data = voice_service.synthesize_speech(response)
                            if audio_data:
                                # Create temporary audio file
                                import tempfile
                                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                                temp_file.write(audio_data)
                                temp_file.close()
                                audio_file = temp_file.name
                        except Exception as e:
                            print(f"TTS error: {e}")

                    yield history, "", audio_file

                return history, "", None

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
            def get_response_inputs():
                """Get inputs for response function based on voice availability"""
                inputs = [msg_input, chatbot]
                if voice_available:
                    inputs.append(tts_enabled)
                return inputs

            def get_response_outputs():
                """Get outputs for response function based on voice availability"""
                outputs = [chatbot, msg_input]
                if voice_available:
                    outputs.append(audio_output)
                return outputs

            send_btn.click(
                respond,
                inputs=get_response_inputs(),
                outputs=get_response_outputs()
            )

            msg_input.submit(
                respond,
                inputs=get_response_inputs(),
                outputs=get_response_outputs()
            )

            # Voice input handling (only if voice available)
            if voice_available and voice_input:
                print("🔧 Setting up voice input event handler...")

                # Create a simple test function first
                def simple_voice_test(voice_file, current_text):
                    print(f"🚨 SIMPLE VOICE TEST TRIGGERED!")
                    print(f"   Voice file: {voice_file}")
                    print(f"   Current text: {current_text}")
                    return (current_text or "") + " [VOICE TEST WORKED!]"

                # Try multiple event types to catch voice input
                try:
                    # Method 1: stop_recording event (for when recording stops)
                    voice_input.stop_recording(
                        simple_voice_test,  # Use simple test first
                        inputs=[voice_input, msg_input],
                        outputs=[msg_input],
                        show_progress=False
                    )
                    print("✅ stop_recording event set up")
                except AttributeError:
                    print("⚠️ stop_recording event not available")
                except Exception as e:
                    print(f"⚠️ stop_recording setup failed: {e}")

                try:
                    # Method 2: change event
                    voice_input.change(
                        simple_voice_test,  # Use simple test first
                        inputs=[voice_input, msg_input],
                        outputs=[msg_input],
                        show_progress=False
                    )
                    print("✅ change event set up")
                except Exception as e:
                    print(f"⚠️ change event failed: {e}")

                try:
                    # Method 3: upload event
                    voice_input.upload(
                        simple_voice_test,  # Use simple test first
                        inputs=[voice_input, msg_input],
                        outputs=[msg_input],
                        show_progress=False
                    )
                    print("✅ upload event set up")
                except Exception as e:
                    print(f"⚠️ upload event failed: {e}")

                print("🎯 All voice events configured - try recording now!")

                # Also set up file upload event (alternative approach)
                if voice_file_input:
                    try:
                        voice_file_input.upload(
                            simple_voice_test,
                            inputs=[voice_file_input, msg_input],
                            outputs=[msg_input],
                            show_progress=False
                        )
                        print("✅ File upload voice event set up")
                    except Exception as e:
                        print(f"⚠️ File upload event failed: {e}")

            clear_btn.click(
                clear_chat,
                outputs=[chatbot, status]
            )

            reset_btn.click(
                reset_memory,
                outputs=[chatbot, status]
            )

            # Voice test button (only if voice available)
            if voice_available and voice_test_btn:
                voice_test_btn.click(
                    test_voice_service,
                    outputs=[status]
                )

            # Manual transcribe button
            if voice_available and transcribe_btn:
                transcribe_btn.click(
                    transcribe_current_audio,
                    inputs=[voice_input, msg_input],
                    outputs=[msg_input]
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