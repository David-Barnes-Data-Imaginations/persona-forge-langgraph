from RealtimeSTT import AudioToTextRecorder

with AudioToTextRecorder(
    model='tiny',
    wakeword_backend='oww',
    wake_words='hey jarvis',
    device='cpu',
    wake_word_activation_delay=3.0,
    wake_word_buffer_duration=0.15,
    post_speech_silence_duration=1.0
) as recorder:
    while True:
        # get the transcribed text from recorder
        query = recorder.text()
        if (query is not None) and (query != ""):

            # get response from our langgraph agent
            response_stream = await get_response_stream(
                query, agent_executor, thread_config
            )

            # output the response to device audio
            await stream_voice(response_stream, output_chunk_builder, voice)