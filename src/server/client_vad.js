// client-vad.js
// Assumes you have an "Open Mic" toggle that calls startOpenMic() / stopOpenMic().

let audioCtx, mic, workletNode;
let socket;
let speaking = false;
let silenceMs = 0;
let speechMs = 0;

const SAMPLE_RATE = 16000;     // downsample to 16k for ASR
const FRAME_MS = 20;           // 20 ms frames
const MIN_SPEECH_MS = 120;     // need at least this much to declare speech
const END_SILENCE_MS = 600;    // endpoint after this much silence
const ENERGY_ON = 0.006;       // energy threshold to flip ON (tune)
const ENERGY_OFF = 0.003;      // lower threshold to flip OFF (hysteresis)
const PRE_ROLL_MS = 300;       // keep this much audio before speech start

// small ring buffer for pre-roll
const preRollFrames = [];
const maxPreRollFrames = Math.ceil(PRE_ROLL_MS / FRAME_MS);

export async function startOpenMic() {
  audioCtx = new AudioContext({ sampleRate: SAMPLE_RATE });
  await audioCtx.audioWorklet.addModule('vad-worklet.js');

  mic = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }, video: false });

  const source = audioCtx.createMediaStreamSource(mic);
  workletNode = new AudioWorkletNode(audioCtx, 'vad-processor', {
    processorOptions: { frameSize: Math.floor(SAMPLE_RATE * FRAME_MS / 1000) }
  });

  source.connect(workletNode);
  workletNode.connect(audioCtx.destination); // or audioCtx.createGain() if you don't want playback

  // connect to your backend WebSocket that accepts raw PCM frames
  socket = new WebSocket('wss://your-server/stream');

  workletNode.port.onmessage = (event) => {
    const { pcm, energy } = event.data; // pcm: Int16Array mono 16kHz FRAME_MS length

    // Keep pre-roll
    preRollFrames.push(pcm);
    if (preRollFrames.length > maxPreRollFrames) preRollFrames.shift();

    // Basic hysteresis
    const onThresh = ENERGY_ON;
    const offThresh = ENERGY_OFF;

    if (!speaking) {
      if (energy > onThresh) {
        speechMs += FRAME_MS;
        if (speechMs >= MIN_SPEECH_MS) {
          speaking = true;
          silenceMs = 0;
          // Flush pre-roll first so we don't clip the start
          for (const fr of preRollFrames) socket.send(fr.buffer);
          preRollFrames.length = 0;
        }
      } else {
        speechMs = Math.max(0, speechMs - FRAME_MS);
      }
    }

    if (speaking) {
      socket.send(pcm.buffer);
      if (energy < offThresh) {
        silenceMs += FRAME_MS;
        if (silenceMs >= END_SILENCE_MS) {
          speaking = false;
          speechMs = 0;
          silenceMs = 0;
          // Signal utterance end to backend (custom message)
          socket.send(JSON.stringify({ type: 'UTTERANCE_END' }));
        }
      } else {
        silenceMs = 0;
      }
    }
  };
}

export function stopOpenMic() {
  if (workletNode) workletNode.port.postMessage({ type: 'STOP' });
  mic?.getTracks().forEach(t => t.stop());
  audioCtx?.close();
  socket?.close();
  speaking = false; silenceMs = 0; speechMs = 0; preRollFrames.length = 0;
}