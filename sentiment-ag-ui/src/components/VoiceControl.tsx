"use client";
import { useState, useRef, useEffect } from "react";
import { Mic, Square, Volume2 } from "lucide-react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";

interface VoiceControlProps {
  handleTranscript: (transcript: string) => void;
  isSpeaking?: boolean;
}

export default function VoiceControl({ handleTranscript, isSpeaking = false }: VoiceControlProps) {
  const [status, setStatus] = useState<string>("Ready");
  const [isRecording, setIsRecording] = useState(false);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

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
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(audioBlob);
          setStatus("Processing...");
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
      setStatus("Recording...");
    } catch (error) {
      console.error("Error starting recording:", error);
      setStatus("Mic access denied");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      if (!socket || socket.readyState !== WebSocket.OPEN) {
        initWebSocket();
      }
      startRecording();
    }
  };

  useEffect(() => {
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [socket]);

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="flex flex-col items-end space-y-2">
        {isRecording && (
          <div className="bg-white/90 backdrop-blur-sm rounded-full px-4 py-2 shadow-lg border border-green-400 animate-pulse">
            <p className="text-sm text-gray-700 font-medium">{status}</p>
          </div>
        )}
        <button
          onClick={toggleRecording}
          disabled={isSpeaking}
          className={`group relative w-16 h-16 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${
            isRecording
              ? "bg-red-500 hover:bg-red-600 scale-110"
              : isSpeaking
              ? "bg-purple-400 cursor-not-allowed"
              : "bg-gradient-to-br from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-110"
          }`}
          title={isRecording ? "Stop recording" : "Start recording"}
        >
          {isRecording ? (
            <Square className="w-6 h-6 text-white" />
          ) : isSpeaking ? (
            <Volume2 className="w-7 h-7 text-white animate-bounce" />
          ) : (
            <Mic className="w-7 h-7 text-white" />
          )}
          {isRecording && (
            <span className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-75"></span>
          )}
        </button>
      </div>
    </div>
  );
}