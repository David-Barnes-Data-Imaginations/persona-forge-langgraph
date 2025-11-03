import { useState, useEffect, useRef } from 'react';

const workletCode = `
class VADProcessor extends AudioWorkletProcessor {
    constructor(options) {
        super();
        this.frameSize = options.processorOptions.frameSize || 320;
        this.buffer = new Float32Array(0);
    }

    process(inputs) {
        const input = inputs[0];
        if (!input || input.length === 0) return true;

        const ch0 = input[0];
        const newBuf = new Float32Array(this.buffer.length + ch0.length);
        newBuf.set(this.buffer, 0);
        newBuf.set(ch0, this.buffer.length);
        this.buffer = newBuf;

        while (this.buffer.length >= this.frameSize) {
            const frame = this.buffer.subarray(0, this.frameSize);
            this.buffer = this.buffer.subarray(this.frameSize);

            let sum = 0;
            for (let i = 0; i < frame.length; i++) sum += frame[i] * frame[i];
            const rms = Math.sqrt(sum / frame.length);

            this.port.postMessage({ rms });
        }
        return true;
    }
}
registerProcessor('vad-processor', VADProcessor);
`;

interface CustomVADOptions {
  onSpeechStart: () => void;
  onSpeechEnd: () => void;
}

export function useCustomVAD({ onSpeechStart, onSpeechEnd }: CustomVADOptions) {
  const [listening, setListening] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const workletNodeRef = useRef<AudioWorkletNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const start = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const audioContext = new AudioContext({ sampleRate: 16000 });
      audioContextRef.current = audioContext;

      const blob = new Blob([workletCode], { type: 'application/javascript' });
      const workletUrl = URL.createObjectURL(blob);
      await audioContext.audioWorklet.addModule(workletUrl);

      const source = audioContext.createMediaStreamSource(stream);
      const workletNode = new AudioWorkletNode(audioContext, 'vad-processor', {
        processorOptions: { frameSize: Math.floor(16000 * 20 / 1000) }
      });
      workletNodeRef.current = workletNode;

      workletNode.port.onmessage = (event) => {
        const { rms } = event.data;
        if (rms > 0.008) {
          if (!speaking) {
            setSpeaking(true);
            onSpeechStart();
          }
        } else {
          if (speaking) {
            setSpeaking(false);
            onSpeechEnd();
          }
        }
      };

      source.connect(workletNode);
      setListening(true);
    } catch (error) {
      console.error('Error starting VAD:', error);
    }
  };

  const stop = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    setListening(false);
    setSpeaking(false);
  };

  useEffect(() => {
    return () => {
      stop();
    };
  }, []);

  return { listening, speaking, start, stop };
}
