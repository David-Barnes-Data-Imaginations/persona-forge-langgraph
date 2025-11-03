"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { Mic, Square } from "lucide-react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";
const VOICE_PROVIDER = (process.env.NEXT_PUBLIC_VOICE_PROVIDER || "local").toLowerCase();

const WORKLET_CODE = `
    class VADProcessor extends AudioWorkletProcessor {
        constructor(options) {
            super();
            this.frameSize = options.processorOptions.frameSize || 320;
            this.buffer = new Float32Array(0);
        }

        process(inputs) {
            const input = inputs[0];
            if (!input || input.length === 0) {
                return true;
            }

            const ch0 = input[0];
            const newBuf = new Float32Array(this.buffer.length + ch0.length);
            newBuf.set(this.buffer, 0);
            newBuf.set(ch0, this.buffer.length);
            this.buffer = newBuf;

            while (this.buffer.length >= this.frameSize) {
                const frame = this.buffer.subarray(0, this.frameSize);
                this.buffer = this.buffer.subarray(this.frameSize);

                let sum = 0;
                for (let i = 0; i < frame.length; i++) {
                    sum += frame[i] * frame[i];
                }
                const rms = Math.sqrt(sum / frame.length);

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
`;

const SAMPLE_RATE = 16000;
const FRAME_MS = 20;
const MIN_SPEECH_MS = 200;
const END_SILENCE_MS = 1200;
const ENERGY_ON = 0.008;
const ENERGY_OFF = 0.004;
const PRE_ROLL_MS = 300;
const MAX_PRE_ROLL_FRAMES = Math.ceil(PRE_ROLL_MS / FRAME_MS);

interface VoiceControlProps {
  handleTranscript: (transcript: string) => void;
  isSpeaking?: boolean;
}

export default function VoiceControl({ handleTranscript, isSpeaking = false }: VoiceControlProps) {
  const [status, setStatus] = useState<string>("Ready");
  const [listening, setListening] = useState<boolean>(false);

  const socketRef = useRef<WebSocket | null>(null);
  const socketReadyRef = useRef<boolean>(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceNodeRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const workletNodeRef = useRef<AudioWorkletNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const listeningRef = useRef<boolean>(false);
  const speakingRef = useRef<boolean>(false);
  const speechMsRef = useRef<number>(0);
  const silenceMsRef = useRef<number>(0);
  const preRollFramesRef = useRef<Int16Array[]>([]);
  const statusTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const clearStatusTimer = useCallback(() => {
    if (statusTimerRef.current) {
      clearTimeout(statusTimerRef.current);
      statusTimerRef.current = null;
    }
  }, []);

  const updateStatus = useCallback(
    (value: string) => {
      clearStatusTimer();
      setStatus(value);
    },
    [clearStatusTimer]
  );

  const setStatusWithTimeout = useCallback(
    (value: string, timeoutMs?: number) => {
      clearStatusTimer();
      setStatus(value);
      if (timeoutMs) {
        statusTimerRef.current = setTimeout(() => {
          setStatus("Ready");
          statusTimerRef.current = null;
        }, timeoutMs);
      }
    },
    [clearStatusTimer]
  );

  const sendFrame = useCallback((frame: Int16Array) => {
    const ws = socketRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      const buffer = frame.buffer.slice(frame.byteOffset, frame.byteOffset + frame.byteLength);
      ws.send(buffer);
    }
  }, []);

  const processFrame = useCallback(
    (frame: Int16Array, energy: number) => {
      const bufferedFrame = frame.slice();
      const preRoll = preRollFramesRef.current;
      preRoll.push(bufferedFrame);
      if (preRoll.length > MAX_PRE_ROLL_FRAMES) {
        preRoll.shift();
      }

      if (!socketReadyRef.current) {
        return;
      }

      if (!speakingRef.current) {
        if (energy > ENERGY_ON) {
          speechMsRef.current += FRAME_MS;
          if (speechMsRef.current >= MIN_SPEECH_MS) {
            speakingRef.current = true;
            silenceMsRef.current = 0;
            updateStatus("Listening...");

            const ws = socketRef.current;
            if (ws && ws.readyState === WebSocket.OPEN) {
              for (const storedFrame of preRoll) {
                sendFrame(storedFrame);
              }
            }
            preRoll.length = 0;
          }
        } else {
          speechMsRef.current = Math.max(0, speechMsRef.current - FRAME_MS);
        }
      }

      if (speakingRef.current) {
        sendFrame(frame);

        if (energy < ENERGY_OFF) {
          silenceMsRef.current += FRAME_MS;
          if (silenceMsRef.current >= END_SILENCE_MS) {
            speakingRef.current = false;
            speechMsRef.current = 0;
            silenceMsRef.current = 0;

            const ws = socketRef.current;
            if (ws && ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({ type: "UTTERANCE_END" }));
            }
            updateStatus("Processing...");
          }
        } else {
          silenceMsRef.current = 0;
        }
      }
    },
    [sendFrame, updateStatus]
  );

  const initWebSocket = useCallback((): Promise<WebSocket> => {
    const existing = socketRef.current;
    if (existing && existing.readyState === WebSocket.OPEN) {
      socketReadyRef.current = true;
      return Promise.resolve(existing);
    }

  const wsUrl = BACKEND_URL.replace(/^http/, "ws");
  const providerQuery = encodeURIComponent(VOICE_PROVIDER);
  const ws = new WebSocket(`${wsUrl}/ws/vad?provider=${providerQuery}`);
    socketRef.current = ws;
    socketReadyRef.current = false;
    updateStatus("Connecting...");

    return new Promise((resolve, reject) => {
      let settled = false;

      ws.onopen = () => {
        socketReadyRef.current = true;
        updateStatus("Voice mode ready");
        if (!settled) {
          settled = true;
          resolve(ws);
        }
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === "TRANSCRIPT" && message.text) {
            handleTranscript(message.text);
            setStatusWithTimeout("Transcribed!", 2500);
          } else if (message.type === "STATUS" && message.message) {
            updateStatus(message.message);
          } else if (message.type === "ERROR" && message.message) {
            updateStatus(`Error: ${message.message}`);
          }
        } catch (err) {
          console.error("Error parsing VAD message:", err);
          updateStatus("Error parsing message");
        }
      };

      ws.onerror = (event) => {
        console.error("WebSocket error:", event);
        socketReadyRef.current = false;
        updateStatus("Connection error");
        if (!settled) {
          settled = true;
          reject(new Error("WebSocket connection failed"));
        }
      };

      ws.onclose = () => {
        console.log("🔌 WebSocket disconnected");
        socketReadyRef.current = false;
        socketRef.current = null;
        if (listeningRef.current) {
          updateStatus("Connection lost");
        } else {
          updateStatus("Ready");
        }
      };
    });
  }, [handleTranscript, setStatusWithTimeout, updateStatus]);

  const stopListening = useCallback(
    (resetStatus: boolean = true) => {
      listeningRef.current = false;
      setListening(false);

      speakingRef.current = false;
      speechMsRef.current = 0;
      silenceMsRef.current = 0;
      preRollFramesRef.current = [];

      if (workletNodeRef.current) {
        workletNodeRef.current.port.onmessage = null;
        workletNodeRef.current.disconnect();
        workletNodeRef.current = null;
      }

      if (sourceNodeRef.current) {
        try {
          sourceNodeRef.current.disconnect();
        } catch (err) {
          console.warn("Error disconnecting source node", err);
        }
        sourceNodeRef.current = null;
      }

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }

      if (audioContextRef.current) {
        audioContextRef.current.close().catch((err) => {
          console.warn("Error closing audio context", err);
        });
        audioContextRef.current = null;
      }

      if (resetStatus) {
        updateStatus("Ready");
      }
    },
    [updateStatus]
  );

  const startListening = useCallback(async () => {
    if (listeningRef.current) {
      return;
    }

    listeningRef.current = true;
    speechMsRef.current = 0;
    silenceMsRef.current = 0;
    preRollFramesRef.current = [];
    speakingRef.current = false;

    try {
      await initWebSocket();

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
        video: false,
      });
      streamRef.current = stream;

      const audioContext = new AudioContext({ sampleRate: SAMPLE_RATE });
      audioContextRef.current = audioContext;

      const blob = new Blob([WORKLET_CODE], { type: "application/javascript" });
      const moduleUrl = URL.createObjectURL(blob);
      await audioContext.audioWorklet.addModule(moduleUrl);
      URL.revokeObjectURL(moduleUrl);

      const sourceNode = audioContext.createMediaStreamSource(stream);
      sourceNodeRef.current = sourceNode;

      const workletNode = new AudioWorkletNode(audioContext, "vad-processor", {
        processorOptions: { frameSize: Math.floor((SAMPLE_RATE * FRAME_MS) / 1000) },
      });
      workletNodeRef.current = workletNode;

      workletNode.port.onmessage = (event: MessageEvent) => {
        const { pcm, energy } = event.data as {
          pcm: Int16Array | number[] | ArrayBuffer;
          energy: number;
        };

        let frame: Int16Array;
        if (pcm instanceof Int16Array) {
          frame = pcm;
        } else if (pcm instanceof ArrayBuffer) {
          frame = new Int16Array(pcm);
        } else {
          frame = Int16Array.from(pcm);
        }

        processFrame(frame, energy);
      };

      sourceNode.connect(workletNode);

      setListening(true);
      updateStatus("Voice mode active");
    } catch (error) {
      console.error("Error starting VAD:", error);
      listeningRef.current = false;
      stopListening(false);
      updateStatus(
        error instanceof Error ? error.message : "Unable to start voice mode"
      );
    }
  }, [initWebSocket, processFrame, stopListening, updateStatus]);

  const toggleListening = () => {
    if (listeningRef.current) {
      stopListening();
    } else {
      startListening();
    }
  };

  useEffect(() => {
    return () => {
      clearStatusTimer();
      stopListening(false);
      if (socketRef.current) {
        socketRef.current.close();
        socketRef.current = null;
      }
    };
  }, [clearStatusTimer, stopListening]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="flex flex-col items-end space-y-2">
        {listening && (
          <div className="bg-white/90 backdrop-blur-sm rounded-full px-4 py-2 shadow-lg border border-blue-200">
            <p className="text-sm text-gray-700 font-medium">{status}</p>
          </div>
        )}
        <button
          onClick={toggleListening}
          disabled={isSpeaking}
          className={`group relative w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${
            listening
              ? "bg-blue-500 hover:bg-blue-600 scale-105"
              : isSpeaking
              ? "bg-purple-400 cursor-not-allowed"
              : "bg-gradient-to-br from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-110"
          }`}
          title={listening ? "Stop listening" : "Start listening"}
        >
          {listening ? (
            <Square className="w-6 h-6 text-white" />
          ) : (
            <Mic className="w-7 h-7 text-white" />
          )}
        </button>
      </div>
    </div>
  );
}