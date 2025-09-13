from RealtimeSTT import AudioToTextRecorder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.store.sqlite.aio import AsyncSqliteStore
from RealtimeSTT import AudioToTextRecorder
from src.graphs.agent import get_new_agent
from src.io_py.tts.output import KokoroSpeech, OutputChunkBuilder, Speech
from langgraph.prebuilt import chat_agent_executor # add possibly later for STT
from settings import load_config

# Dependant on the python version used
try:
    from collections.abc import AsyncGenerator
except ImportError:
    from typing import AsyncGenerator


async def stream_speech(
    msg_stream: AsyncGenerator,
    output_chunk_builder: OutputChunkBuilder,
    speech: KokoroSpeech
):
    """Stream messages from the agent to the voice output."""
    async for chunk, metadata in msg_stream:
        if metadata["langgraph_node"] == "agent":
            # build up message chunks until a full sentence is received.
            if chunk.content != "":
                output_chunk_builder.add_chunk(chunk.content)

            if output_chunk_builder.output_chunk_ready():
                speech.convert_text_to_speech(output_chunk_builder.get_output_chunk())

    # if we have anything left in the buffer, speak it.
    if output_chunk_builder.current_message_length() > 0:
        speech.convert_text_to_speech(output_chunk_builder.get_output_chunk())

# Can handle other tasks while waiting for complete LLM response
# Placeholder until I add the local llm. Might not be an AsyncGenerator or AudioToTextRecorder
async def survey_mode(
        local_tts: AsyncGenerator,
        recorder: AudioToTextRecorder,
        speech: KokoroSpeech,
        agent_executor: chat_agent_executor
    ):

    messages = await agent_executor.ainvoke(...)  # async complete response
    await local_tts.speak(messages[-1].content)
    # add this later
 #   user_response = await stt.transcribe_until_silence()

async def main():
    conf = load_config()
    speech = KokoroSpeech(**conf.KokoroSpeech)
    output_chunk_builder = OutputChunkBuilder()

    user_query = "Hello world!"
    user_query_formatted = {
        "role": "user",
        "content": user_query
    }

    system_prompt_formatted = {
        "role": "system",
        "content": (
            "You are a voice assistant called Delamain."
            + " Keep your responses as short as possible."
            + "Do not format your responses using markdown, such as **bold** or _italics. ",
        )
    }


# AsyncSqliteStore classes from the checkpoint and store modules in langgraph
# SQL databases to store our short and long term memory
    # short term memory
    async with AsyncSqliteSaver.from_conn_string(conf.Agent.memory.checkpointer) as saver:

        # long term memory
        async with AsyncSqliteStore.from_conn_string(conf.Agent.memory.store) as store:

            agent_executor = get_new_agent(conf, saver, store)

            with AudioToTextRecorder(
                    model='tiny',
                    wakeword_backend='',
                    wake_words='delamain',
                    device='cpu',
                    wake_word_activation_delay=3.0,
                    wake_word_buffer_duration=0.15,
                    post_speech_silence_duration=1.0
            ) as recorder:
                while True:
                    # get the transcribed text from recorder
                    query = recorder.text()
                    if (query is not None) and (query != ""):
                        # get response from the langgraph agent
                        output_stream = agent_executor.stream(
                            {"messages": [system_prompt_formatted, user_query_formatted]},
                            stream_mode="messages"
                        )
                        # output the response to device audio
                        await stream_speech(output_stream, output_chunk_builder, speech)



if __name__ == "__main__":
    asyncio.run(main())