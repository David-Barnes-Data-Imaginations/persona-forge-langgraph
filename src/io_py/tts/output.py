from __future__ import annotations
import numpy as np

class Speech():
    def __init__(
        self,
        sample_rate: int = 24000,
        chunk_size: int = 2048
    ):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.initialise_model()

    def model_init(self):
        pass

    def tts(self, text:str) -> list[np.ndarray]:
        """Converts tts then returns the waveform as frames."""
        pass

    def speak(self, text:str):
        """Speak the provided text through device output."""
        frames = self.tts(self, text)
        for frame in frames:
            self.output_stream.write(frame.tobytes())

# chunker for collating the message output
class OutputChunkBuilder:
    def __init__(self):
        self._msg = ""
        self.end_of_sentence = (".", "?", ";", "!", "\n")

    def add_chunk(self, message_chunk: str):
        self._msg += message_chunk

    def output_chunk_ready(self) -> bool:
        return self._msg.endswith(self.end_of_sentence)

    def _reset_message(self):
        self._msg = ""

    def get_output_chunk(self):
        msg = self._msg  # Get the current message chunk
        self._reset_message()
        return msg

async def stream_speech(
    msg_stream: AsyncGenerator,
    output_chunk_builder: OutputChunkBuilder,
    voice: Speech
):
    """Stream messages from the agent to the voice output."""
    async for chunk, metadata in msg_stream:
        if metadata["langgraph_node"] == "agent":
            # build up message chunks until a full sentence is received.
            if chunk.content != "":
                output_chunk_builder.add_chunk(chunk.content)

            if output_chunk_builder.output_chunk_ready():
                voice.speak(output_chunk_builder.get_output_chunk())

    # if we have anything left in the buffer, speak it.
    if output_chunk_builder.current_message_length() > 0:
        voice.speak(output_chunk_builder.get_output_chunk())