"use client";

import { useState, useRef, useEffect } from 'react';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8001";

const VoiceControl = ({ handleTranscript }: { handleTranscript: (transcript: string) => void }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  useEffect(() => {
    return () => {
      if (socket) {
        socket.close();
      }
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
    };
  }, [socket]);

  const startRecording = async () => {
    const wsUrl = BACKEND_URL.replace(/^http/, 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/vad-stream`);
    setSocket(ws);

    ws.onopen = async () => {
      console.log('WebSocket connected');
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          ws.send(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        ws.close();
      };

      mediaRecorder.start(1000); // Send data every second
      setIsRecording(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'TRANSCRIPT') {
        handleTranscript(message.text);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
      setIsRecording(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsRecording(false);
    };
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  return (
    <div className="fixed bottom-10 right-10">
      <button 
        onClick={isRecording ? stopRecording : startRecording}
        className={`w-16 h-16 rounded-full flex items-center justify-center text-white ${isRecording ? 'bg-red-500' : 'bg-purple-600'}`}>
        {isRecording ? 'Stop' : 'Record'}
      </button>
    </div>
  );
};

export default VoiceControl;
