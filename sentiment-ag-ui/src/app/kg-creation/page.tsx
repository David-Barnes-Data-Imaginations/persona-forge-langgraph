"use client";

import { useState, useRef, useEffect } from "react";
import Header from "@/components/Header";
import { getBackendUrl } from "@/lib/config";

type WorkflowEvent = 
  | { type: "status"; message: string; step: string }
  | { type: "progress"; current: number; total: number; qa_id: string }
  | { type: "processing"; qa_id: string; entry: number }
  | { type: "cypher_result"; qa_id: string; content: string; chunks_created: number }
  | { type: "complete"; message: string }
  | { type: "error"; message?: string; qa_id?: string };

type CypherEntry = {
  id: string;
  qa_id: string;
  content: string;
  chunks_created: number;
  timestamp: Date;
};

export default function KGCreationPage() {
  const [isRunning, setIsRunning] = useState(false);
  const [status, setStatus] = useState<string>("Ready to start");
  const [progress, setProgress] = useState({ current: 0, total: 0 });
  const [cypherEntries, setCypherEntries] = useState<CypherEntry[]>([]);
  const [accumulatedOutput, setAccumulatedOutput] = useState<string>("");
  const outputEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Auto-scroll to bottom when new entries arrive
  useEffect(() => {
    outputEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [cypherEntries]);

  const startWorkflow = async () => {
    setIsRunning(true);
    setStatus("Starting workflow...");
    setProgress({ current: 0, total: 0 });
    setCypherEntries([]);
    setAccumulatedOutput("");

    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(getBackendUrl("/api/kg-creation/run"), {
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
                  setStatus(jsonData.message);
                  break;

                case "progress":
                  setProgress({ current: jsonData.current, total: jsonData.total });
                  setStatus(`Generating Cypher ${jsonData.current} of ${jsonData.total} (${jsonData.qa_id})`);
                  break;

                case "processing":
                  setStatus(`Processing analysis entry ${jsonData.entry}...`);
                  break;

                case "cypher_result":
                  const newEntry: CypherEntry = {
                    id: `${jsonData.qa_id}-${Date.now()}`,
                    qa_id: jsonData.qa_id,
                    content: jsonData.content,
                    chunks_created: jsonData.chunks_created,
                    timestamp: new Date(),
                  };
                  setCypherEntries((prev) => [...prev, newEntry]);
                  setAccumulatedOutput((prev) => prev + "\n\n" + jsonData.content);
                  break;

                case "complete":
                  setStatus(jsonData.message);
                  break;

                case "error":
                  const errorMsg = jsonData.qa_id 
                    ? `Error in ${jsonData.qa_id}: ${jsonData.message}` 
                    : `Error: ${jsonData.message}`;
                  setStatus(errorMsg);
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
          setStatus(`❌ ${error.message}`);
        }
      } else {
        setStatus("❌ Unknown error occurred");
      }
    } finally {
      setIsRunning(false);
      abortControllerRef.current = null;
    }
  };

  const stopWorkflow = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setStatus("⏹️ Workflow stopped by user");
    }
  };

  const copyOutput = () => {
    navigator.clipboard.writeText(accumulatedOutput);
    alert("Cypher output copied to clipboard!");
  };

  const progressPercentage = progress.total > 0 
    ? Math.round((progress.current / progress.total) * 100) 
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header Section */}
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-white mb-4">
              🔗 Knowledge Graph Creation
            </h1>
            <p className="text-gray-300 text-lg">
              Generate Cypher queries and embeddings from psychological analyses
            </p>
          </div>

          {/* Control Panel */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-6 mb-6 border border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex-1">
                <h2 className="text-xl font-semibold text-white mb-2">Workflow Control</h2>
                <p className="text-gray-400 text-sm">{status}</p>
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
                    "▶️ Start Generation"
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

            {/* Progress Bar */}
            {progress.total > 0 && (
              <div className="mt-4">
                <div className="flex justify-between text-sm text-gray-400 mb-2">
                  <span>Progress: {progress.current} / {progress.total} analyses</span>
                  <span>{progressPercentage}%</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Output Section */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg border border-slate-700 overflow-hidden">
            <div className="bg-slate-700/50 px-6 py-3 border-b border-slate-600 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-white">📄 Cypher Output</h3>
              {cypherEntries.length > 0 && (
                <button
                  onClick={copyOutput}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm rounded-lg transition-all"
                >
                  📋 Copy All Cypher
                </button>
              )}
            </div>
            
            <div className="h-[600px] overflow-y-auto p-6">
              {cypherEntries.length === 0 ? (
                <div className="text-gray-500 text-center py-20">
                  No Cypher generated yet. Click &quot;Start Generation&quot; to begin.
                </div>
              ) : (
                <div className="space-y-6">
                  {cypherEntries.map((entry) => (
                    <div
                      key={entry.id}
                      className="bg-slate-700/30 rounded-lg p-4 border border-slate-600"
                    >
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <span className="text-indigo-400 font-semibold">
                            {entry.qa_id}
                          </span>
                          <span className="text-gray-500 text-sm">
                            {entry.timestamp.toLocaleTimeString()}
                          </span>
                          {entry.chunks_created > 0 && (
                            <span className="text-green-400 text-sm bg-green-900/30 px-2 py-1 rounded">
                              {entry.chunks_created} chunks
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <pre className="text-gray-300 whitespace-pre-wrap text-sm leading-relaxed font-mono bg-slate-900/50 p-4 rounded overflow-x-auto">
                        {entry.content}
                      </pre>
                    </div>
                  ))}
                  <div ref={outputEndRef} />
                </div>
              )}
            </div>
          </div>

          {/* Info Box */}
          <div className="mt-6 bg-blue-900/30 backdrop-blur-sm rounded-lg p-6 border border-blue-700/50">
            <h4 className="text-blue-300 font-semibold mb-2">ℹ️ How This Works</h4>
            <ul className="text-gray-300 text-sm space-y-1">
              <li>• Reads psychological analyses from master file</li>
              <li>• Generates Cypher queries for Neo4j knowledge graph</li>
              <li>• Creates text chunks with embeddings for hybrid RAG</li>
              <li>• Saves to: <code className="text-blue-400 bg-slate-800 px-2 py-1 rounded">output/psychological_analysis/graph_output/psychological_graph_[date].cypher</code></li>
              <li>• Use &quot;Copy All Cypher&quot; to get the complete graph schema</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
