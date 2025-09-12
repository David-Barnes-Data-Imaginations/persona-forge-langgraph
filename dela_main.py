from RealtimeSTT import AudioToTextRecorder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.store.sqlite.aio import AsyncSqliteStore
from RealtimeSTT import AudioToTextRecorder
from src.graphs.agent import get_new_agent, get_response_stream
from src.io_py.tts.output import KokoroSpeech, OutputChunkBuilder, Speech
from settings import load_config

async def stream_speech(
    msg_stream: AsyncGenerator,
    output_chunk_builder: OutputChunkBuilder,
    speech: Speech
):
    """Stream messages from the agent to the voice output."""
    async for chunk, metadata in msg_stream:
        if metadata["langgraph_node"] == "agent":
            # build up message chunks until a full sentence is received.
            if chunk.content != "":
                output_chunk_builder.add_chunk(chunk.content)

            if output_chunk_builder.output_chunk_ready():
                speech.speak(output_chunk_builder.get_output_chunk())

    # if we have anything left in the buffer, speak it.
    if output_chunk_builder.current_message_length() > 0:
        speech.speak(output_chunk_builder.get_output_chunk())

async def main():
    conf = load_config()
    voice = KokoroSpeech(**conf.KokoroSpeech)
    output_chunk_builder = OutputChunkBuilder()
    thread_config = {"configurable": {"thread_id": "abc123"}}

    agent_executor=get_new_agent()

    response_stream = agent_executor.invoke(
        {"messages": [system_prompt_formatted, user_query_formatted]},
    )

    output_stream = agent_executor.stream(
        {"messages": [system_prompt_formatted, user_query_formatted]},
        stream_mode="messages"
    )
# AsyncSqliteStore classes from the checkpoint and store modules in langgraph
    # short term memory
    async with AsyncSqliteSaver.from_conn_string(conf.Agent.memory.checkpointer) as saver:

        # long term memory
        async with AsyncSqliteStore.from_conn_string(conf.Agent.memory.store) as store:

            agent_executor = await get_new_agent(conf, saver, store)

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
                        response_stream = await get_response_stream(
                            query, agent_executor, thread_config
                        )

                        # output the response to device audio
                        await stream_speech(response_stream, output_chunk_builder, voice)



if __name__ == "__main__":
    asyncio.run(main()