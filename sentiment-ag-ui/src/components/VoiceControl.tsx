"use client";
import { useState, useRef, useEffect } from "react";
import { Mic, Square, Volume2 } from "lucide-react";
import VAD from "webrtc-vad";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";

interface VoiceControlProps {
  handleTranscript: (transcript: string) => void;
  isSpeaking?: boolean;
}

export default function VoiceControl({ handleTranscript, isSpeaking = false }: VoiceControlProps) {
  const [status, setStatus] = useState<string>("Ready");
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [listening, setListening] = useState(false);
  const [userSpeaking, setUserSpeaking] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioContextRef = useRef<AudioContext | null>(null);
  const vadRef = useRef<any>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const initWebSocket = () => {
    const wsUrl = BACKEND_URL.replace(/^http/, "ws");
    const ws = new WebSocket(`${wsUrl}/ws`);

    ws.onopen = () => {
      console.log("✅ WebSocket connected");
      setStatus("Connected");
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === "TRANSCRIPT" && message.text) {
          handleTranscript(message.text);
          setStatus("Transcribed!");
          setTimeout(() => setStatus("Ready"), 2000);
        } else {
          setStatus("Ready");
        }
      } catch (error) {
        console.error("Error parsing message:", error);
        setStatus("Error");
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setStatus("Connection error");
    };

    ws.onclose = () => {
      console.log("🔌 WebSocket disconnected");
      setSocket(null);
    };

    setSocket(ws);
    return ws;
  };

  const startRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "inactive") {
      audioChunksRef.current = [];
      mediaRecorderRef.current.start();
      setUserSpeaking(true);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
      setUserSpeaking(false);
    }
  };

  const processAudio = (audioData: Float32Array) => {
    if (vadRef.current) {
      const isSpeech = vadRef.current.process(audioData);
      if (isSpeech) {
        if (!userSpeaking) {
          startRecording();
        }
      } else {
        if (userSpeaking) {
          stopRecording();
        }
      }
    }
  };

  const toggleListening = async () => {
    if (listening) {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      audioContextRef.current?.close();
      setListening(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        streamRef.current = stream;
        const audioContext = new AudioContext();
        audioContextRef.current = audioContext;
        const source = audioContext.createMediaStreamSource(stream);
        const processor = audioContext.createScriptProcessor(1024, 1, 1);

        processor.onaudioprocess = (e) => {
          const inputData = e.inputBuffer.getChannelData(0);
          processAudio(inputData);
        };

        source.connect(processor);
        processor.connect(audioContext.destination);

        const mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus" });
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
          audioChunksRef.current.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm;codecs=opus" });
          if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(audioBlob);
            setStatus("Processing...");
          }
        };

        vadRef.current = new VAD(VAD.Mode.NORMAL);

        let ws = socket;
        if (!ws || ws.readyState !== WebSocket.OPEN) {
          ws = initWebSocket();
        }

        setListening(true);
      } catch (error) {
        console.error("Error starting recording:", error);
        setStatus("Mic access denied");
      }
    }
  };

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      audioContextRef.current?.close();
      if (socket) {
        socket.close();
      }
    };
  }, [socket]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="flex flex-col items-end space-y-2">
        {(listening || userSpeaking) && (
          <div className={`bg-white/90 backdrop-blur-sm rounded-full px-4 py-2 shadow-lg border ${
            userSpeaking ? "border-green-400 animate-pulse" : "border-blue-200"
          }`}>
            <p className="text-sm text-gray-700 font-medium">
              {userSpeaking ? "🎤 Speaking..." : status}
            </p>
          </div>
        )}
        <button
          onClick={toggleListening}
          disabled={isSpeaking}
          className={`group relative w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${
            userSpeaking
              ? "bg-green-500 hover:bg-green-600 scale-110 animate-pulse"
              : listening
              ? "bg-blue-500 hover:bg-blue-600 scale-105"
              : isSpeaking
              ? "bg-purple-400 cursor-not-allowed"
              : "bg-gradient-to-br from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-110"
          }`}
          title={
            listening
              ? "Stop listening"
              : isSpeaking
              ? "AI is speaking"
              : "Start listening"
          }
        >
          {isSpeaking ? (
            <Volume2 className="w-7 h-7 text-white animate-bounce" />
          ) : userSpeaking ? (
            <Mic className="w-7 h-7 text-white animate-pulse" />
          ) : listening ? (
            <Mic className="w-7 h-7 text-white" />
          ) : (
            <Mic className="w-7 h-7 text-white" />
          )}
          {userSpeaking && (
            <span className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-75"></span>
          )}
        </button>
      </div>
    </div>
  );
}
