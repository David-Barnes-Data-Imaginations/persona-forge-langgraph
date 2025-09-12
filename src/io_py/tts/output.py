from __future__ import annotations
import numpy as np
from kokoro import KPipeline

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

class KokoroSpeech(Speech):
    def __init__(self, speech: str, sample_rate: int = 24000, chunk_size: int = 2048):
        """Initialise the model to use for TTS.

        Args:
            voice (str):
                The voice to use.
                See https://github.com/hexgrad/kokoro/blob/main/kokoro.js/voices/
                for all voices.
            sample_rate (int, optional):
                The sample rate to use. Defaults to 24000.
            chunk_size (int, optional):
                The chunk size to use. Defaults to 2048.
        """
        self.speech = speech
        super().__init__(sample_rate, chunk_size)

    def initialise_model(self):
        """Load the model to use for TTS."""
        self.pipeline = KPipeline(lang_code="b")

    def convert_text_to_speech(self, text: str) -> list[np.ndarray]:
        """Convert text to speech and return the waveform as frames."""
        generator = self.pipeline(text, voice=self.speech)
        frames = []
        for i, (_, _, audio) in enumerate(generator):
            for start in range(0, len(audio), self.chunk_size):
                chunk = audio[start: start + self.chunk_size]
                frames.append(chunk.numpy().astype(np.float32))
        return frames

