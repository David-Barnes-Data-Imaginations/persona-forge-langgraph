"use client";

import { useState, useRef, useEffect } from "react";
import Header from "@/components/Header";
import { getBackendUrl } from "@/lib/config";

type WorkflowEvent = 
  | { type: "status"; message: string; step: string }
  | { type: "todos"; data: Array<{ content: string; status: string }> }
  | { type: "thought"; content: string; step: number }
  | { type: "delegation"; tool: string; description: string; step: number }
  | { type: "tool_call"; tool: string; step: number }
  | { type: "response"; content: string; step: number }
  | { type: "files"; data: string[] }
  | { type: "report"; content: string }
  | { type: "complete"; message: string }
  | { type: "error"; message: string };

type LogEntry = {
  id: string;
  timestamp: Date;
  type: "status" | "thought" | "tool" | "response" | "error" | "complete";
  content: string;
  step?: number;
};

export default function DeepAgentPage() {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [todos, setTodos] = useState<Array<{ content: string; status: string }>>([]);
  const [report, setReport] = useState<string>("");
  const [files, setFiles] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const addLog = (type: LogEntry["type"], content: string, step?: number) => {
    setLogs((prev) => [
      ...prev,
      {
        id: `${Date.now()}-${Math.random()}`,
        timestamp: new Date(),
        type,
        content,
        step,
      },
    ]);
  };

  const startWorkflow = async () => {
    setIsRunning(true);
    setLogs([]);
    setTodos([]);
    setReport("");
    setFiles([]);

    abortControllerRef.current = new AbortController();

    try {
      addLog("status", "🚀 Connecting to backend...");

      const response = await fetch(getBackendUrl("/api/deep-agent/run"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No response body");
      }

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const jsonData = JSON.parse(line.slice(6)) as WorkflowEvent;

              switch (jsonData.type) {
                case "status":
                  addLog("status", `📋 ${jsonData.message}`, undefined);
                  break;

                case "todos":
                  setTodos(jsonData.data);
                  addLog("status", `✅ Updated TODO list (${jsonData.data.length} items)`, undefined);
                  break;

                case "thought":
                  addLog("thought", `💭 ${jsonData.content}`, jsonData.step);
                  break;

                case "delegation":
                  addLog("tool", `🔧 ${jsonData.tool}: ${jsonData.description}`, jsonData.step);
                  break;

                case "tool_call":
                  addLog("tool", `🔧 Tool: ${jsonData.tool}`, jsonData.step);
                  break;

                case "response":
                  addLog("response", jsonData.content, jsonData.step);
                  break;

                case "files":
                  setFiles(jsonData.data);
                  addLog("status", `📁 Created ${jsonData.data.length} files`, undefined);
                  break;

                case "report":
                  setReport(jsonData.content);
                  addLog("complete", "📄 Therapy report generated!", undefined);
                  break;

                case "complete":
                  addLog("complete", `✅ ${jsonData.message}`, undefined);
                  break;

                case "error":
                  addLog("error", `❌ Error: ${jsonData.message}`, undefined);
                  break;
              }
            } catch (e) {
              console.error("Failed to parse event:", e, line);
            }
          }
        }
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        if (error.name !== "AbortError") {
          addLog("error", `❌ ${error.message}`);
        }
      } else {
        addLog("error", "❌ Unknown error occurred");
      }
    } finally {
      setIsRunning(false);
      abortControllerRef.current = null;
    }
  };

  const stopWorkflow = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      addLog("status", "⏹️ Workflow stopped by user");
    }
  };

  const getStatusEmoji = (status: string) => {
    switch (status) {
      case "pending":
        return "⏳";
      case "in_progress":
        return "🔄";
      case "completed":
        return "✅";
      case "failed":
        return "❌";
      default:
        return "📋";
    }
  };

  const getLogColor = (type: LogEntry["type"]) => {
    switch (type) {
      case "status":
        return "text-blue-400";
      case "thought":
        return "text-purple-400";
      case "tool":
        return "text-yellow-400";
      case "response":
        return "text-green-400";
      case "error":
        return "text-red-400";
      case "complete":
        return "text-emerald-400";
      default:
        return "text-gray-400";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header Section */}
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-white mb-4">
              🧠 Deep Agent Workflow
            </h1>
            <p className="text-gray-300 text-lg">
              Automated therapy progress note generation using multi-agent AI system
            </p>
          </div>

          {/* Control Panel */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 mb-6 border border-slate-700">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-white mb-2">Workflow Control</h2>
                <p className="text-gray-400 text-sm">
                  {isRunning 
                    ? "Workflow is running... This may take several minutes." 
                    : "Click the button below to start the automated workflow"}
                </p>
              </div>
              
              <div className="flex gap-4">
                <button
                  onClick={startWorkflow}
                  disabled={isRunning}
                  className={`px-8 py-3 rounded-lg font-semibold transition-all ${
                    isRunning
                      ? "bg-gray-600 cursor-not-allowed"
                      : "bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg hover:shadow-xl"
                  } text-white`}
                >
                  {isRunning ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                          fill="none"
                        />
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        />
                      </svg>
                      Running...
                    </span>
                  ) : (
                    "▶️ Start Workflow"
                  )}
                </button>

                {isRunning && (
                  <button
                    onClick={stopWorkflow}
                    className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition-all"
                  >
                    ⏹️ Stop
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Logs */}
            <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 overflow-hidden">
              <div className="bg-slate-700/50 px-6 py-3 border-b border-slate-600">
                <h3 className="text-lg font-semibold text-white">📝 Workflow Log</h3>
              </div>
              
              <div className="h-[600px] overflow-y-auto p-6 font-mono text-sm">
                {logs.length === 0 ? (
                  <div className="text-gray-500 text-center py-20">
                    No logs yet. Start the workflow to see agent activity.
                  </div>
                ) : (
                  <div className="space-y-2">
                    {logs.map((log) => (
                      <div
                        key={log.id}
                        className={`${getLogColor(log.type)} leading-relaxed`}
                      >
                        <span className="text-gray-500">
                          [{log.timestamp.toLocaleTimeString()}]
                        </span>
                        {log.step && (
                          <span className="text-gray-400 ml-2">[Step {log.step}]</span>
                        )}
                        <span className="ml-2">{log.content}</span>
                      </div>
                    ))}
                    <div ref={logsEndRef} />
                  </div>
                )}
              </div>
            </div>

            {/* Right Column - TODOs and Status */}
            <div className="space-y-6">
              {/* TODOs */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 overflow-hidden">
                <div className="bg-slate-700/50 px-6 py-3 border-b border-slate-600">
                  <h3 className="text-lg font-semibold text-white">📋 Tasks</h3>
                </div>
                
                <div className="p-6">
                  {todos.length === 0 ? (
                    <div className="text-gray-500 text-sm">No tasks yet</div>
                  ) : (
                    <div className="space-y-3">
                      {todos.map((todo, idx) => (
                        <div
                          key={idx}
                          className="flex items-start gap-3 p-3 bg-slate-700/30 rounded-lg"
                        >
                          <span className="text-2xl">
                            {getStatusEmoji(todo.status)}
                          </span>
                          <div className="flex-1">
                            <div className="text-sm text-white">{todo.content}</div>
                            <div className="text-xs text-gray-400 mt-1 capitalize">
                              {todo.status.replace("_", " ")}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Files Created */}
              {files.length > 0 && (
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 overflow-hidden">
                  <div className="bg-slate-700/50 px-6 py-3 border-b border-slate-600">
                    <h3 className="text-lg font-semibold text-white">📁 Files</h3>
                  </div>
                  
                  <div className="p-6">
                    <div className="space-y-2">
                      {files.map((file, idx) => (
                        <div
                          key={idx}
                          className="text-sm text-gray-300 font-mono bg-slate-700/30 px-3 py-2 rounded"
                        >
                          {file}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Report Section */}
          {report && (
            <div className="mt-6 bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 overflow-hidden">
              <div className="bg-slate-700/50 px-6 py-3 border-b border-slate-600 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-white">📄 Generated Report</h3>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(report);
                    alert("Report copied to clipboard!");
                  }}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm rounded-lg transition-all"
                >
                  📋 Copy to Clipboard
                </button>
              </div>
              
              <div className="p-6">
                <pre className="text-gray-300 whitespace-pre-wrap text-sm leading-relaxed">
                  {report}
                </pre>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
