from RealtimeSTT import AudioToTextRecorder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.store.sqlite.aio import AsyncSqliteStore

from voice_assistant.agent import get_new_agent, get_response_stream
from voice_assistant.voice import KokoroVoice
from settings import load_config


async def main():
    conf = load_config()
    voice = KokoroVoice(**conf.KokoroVoice)
    output_chunk_builder = OutputChunkBuilder()
    thread_config = {"configurable": {"thread_id": "abc123"}}

# AsyncSqliteStore classes from the checkpoint and store modules in langgraph
    # short term memory
    async with AsyncSqliteSaver.from_conn_string(conf.Agent.memory.checkpointer) as saver:

        # long term memory
        async with AsyncSqliteStore.from_conn_string(conf.Agent.memory.store) as store:

            agent_executor = await get_new_agent(conf, saver, store)

            with AudioToTextRecorder(**conf.AudioToTextRecorder) as recorder:
                while True:
                    query = recorder.text()
                    if (query is not None) and (query != ""):
                        response_stream = await get_response_stream(
                            query, agent_executor, thread_config
                        )
                        await stream_voice(response_stream, output_chunk_builder, voice)


if __name__ == "__main__":
    asyncio.run(main()