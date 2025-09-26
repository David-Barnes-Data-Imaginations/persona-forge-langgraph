// vad-worklet.js
class VADProcessor extends AudioWorkletProcessor {
  constructor(options) {
    super();
    this.frameSize = options.processorOptions.frameSize || 320; // 20 ms @ 16kHz
    this.buffer = new Float32Array(0);
  }

  // Downmix to mono, compute short-term energy, convert to Int16 PCM
  process(inputs) {
    const input = inputs[0];
    if (!input || input.length === 0) return true;

    const ch0 = input[0];
    // Append
    const newBuf = new Float32Array(this.buffer.length + ch0.length);
    newBuf.set(this.buffer, 0);
    newBuf.set(ch0, this.buffer.length);
    this.buffer = newBuf;

    while (this.buffer.length >= this.frameSize) {
      const frame = this.buffer.subarray(0, this.frameSize);
      this.buffer = this.buffer.subarray(this.frameSize);

      // simple energy (RMS) calculation
      let sum = 0;
      for (let i = 0; i < frame.length; i++) sum += frame[i] * frame[i];
      const rms = Math.sqrt(sum / frame.length);

      // float32 [-1..1] -> int16
      const pcm = new Int16Array(frame.length);
      for (let i = 0; i < frame.length; i++) {
        const s = Math.max(-1, Math.min(1, frame[i]));
        pcm[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
      }

      this.port.postMessage({ pcm, energy: rms });
    }
    return true;
  }
}

registerProcessor('vad-processor', VADProcessor);