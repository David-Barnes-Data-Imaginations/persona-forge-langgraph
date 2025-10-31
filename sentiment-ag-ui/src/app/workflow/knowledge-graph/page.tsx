"use client";

import { useState } from 'react';
import { Network, AlertCircle, CheckCircle, ArrowLeft, Download, Copy } from 'lucide-react';
import Link from 'next/link';
import { getBackendUrl } from '@/lib/config';
import Header from '@/components/Header';

export default function KnowledgeGraphPage() {
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [cypherScript, setCypherScript] = useState<string>('');
  const [copied, setCopied] = useState(false);

  const handleCreateGraph = async () => {
    setProcessing(true);
    setError(null);

    try {
      const response = await fetch(getBackendUrl('/workflow/knowledge-graph'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Knowledge graph creation failed');
      }

      const data = await response.json();
      setResults(data);

      // Fetch the cypher script
      const cypherResponse = await fetch(getBackendUrl('/workflow/cypher-output'));
      if (cypherResponse.ok) {
        const cypherData = await cypherResponse.json();
        setCypherScript(cypherData.content || '');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during graph creation');
      console.error('Graph creation error:', err);
    } finally {
      setProcessing(false);
    }
  };

  const copyCypher = () => {
    navigator.clipboard.writeText(cypherScript);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadCypher = () => {
    const blob = new Blob([cypherScript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `knowledge-graph-${new Date().toISOString()}.cypher`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center space-x-4 mb-6">
          <Link
            href="/landing"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </Link>
          <div className="flex items-center space-x-3">
            <Network className="w-8 h-8 text-green-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Knowledge Graph Creation</h1>
              <p className="text-sm text-gray-600">
                Generate Neo4j graph with embeddings
              </p>
            </div>
          </div>
        </div>
      </div>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <h2 className="text-lg font-semibold text-blue-900 mb-2">How it works</h2>
          <ol className="list-decimal list-inside space-y-2 text-blue-800">
            <li>Reads your Framework Analysis results</li>
            <li>Generates Neo4j Cypher script for graph creation</li>
            <li>Creates vector embeddings for hybrid RAG</li>
            <li>Copy the Cypher script and paste into Neo4j Browser</li>
          </ol>
        </div>

        {/* Prerequisites Check */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
          <h3 className="font-semibold text-yellow-900 mb-2">Prerequisites</h3>
          <p className="text-yellow-800 text-sm">
            ⚠️ Make sure you've completed the Framework Analysis workflow first. The system will
            read from <code className="bg-yellow-100 px-1 py-0.5 rounded">output/psychological_analysis/psychological_analysis_master.txt</code>
          </p>
        </div>

        {/* Start Button */}
        {!results && !processing && (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center">
            <Network className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Ready to Create Knowledge Graph
            </h2>
            <p className="text-gray-600 mb-6">
              This will process your analysis results and generate a Neo4j graph structure
            </p>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-800 text-left">{error}</p>
              </div>
            )}

            <button
              onClick={handleCreateGraph}
              className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              Create Knowledge Graph
            </button>
          </div>
        )}

        {/* Processing */}
        {processing && (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center">
            <div className="flex flex-col items-center">
              <svg
                className="animate-spin h-16 w-16 text-green-600 mb-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Creating Knowledge Graph...
              </h3>
              <p className="text-gray-600">
                This may take a few minutes. Generating Cypher and embeddings.
              </p>
            </div>
          </div>
        )}

        {/* Results */}
        {results && cypherScript && (
          <div className="space-y-6">
            {/* Success Banner */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 flex items-start space-x-3">
              <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-green-900">
                  Knowledge Graph Created!
                </h3>
                <p className="text-green-800 mt-1">
                  Your Cypher script is ready. Copy and paste it into Neo4j Browser.
                </p>
              </div>
            </div>

            {/* Cypher Script */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Cypher Script</h3>
                <div className="flex space-x-2">
                  <button
                    onClick={copyCypher}
                    className="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                  >
                    <Copy className="w-4 h-4" />
                    <span>{copied ? 'Copied!' : 'Copy'}</span>
                  </button>
                  <button
                    onClick={downloadCypher}
                    className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download</span>
                  </button>
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 overflow-x-auto max-h-96">
                <pre className="text-xs text-gray-800 font-mono">{cypherScript}</pre>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                How to Import into Neo4j
              </h3>
              <ol className="list-decimal list-inside space-y-3 text-gray-700">
                <li>Open Neo4j Browser (usually at <code className="bg-gray-100 px-1 py-0.5 rounded">http://localhost:7474</code>)</li>
                <li>Copy the Cypher script above</li>
                <li>Paste it into the Neo4j Browser query window</li>
                <li>Click the "Run" button or press Ctrl+Enter</li>
                <li>Wait for the import to complete</li>
                <li>Query your new knowledge graph using the chat interface!</li>
              </ol>
            </div>

            {/* Next Steps */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Next Steps</h3>
              <div className="flex flex-wrap gap-4">
                <Link
                  href="/chat"
                  className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  <span>Query Graph in Chat →</span>
                </Link>
                <button
                  onClick={() => {
                    setResults(null);
                    setCypherScript('');
                    setError(null);
                  }}
                  className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Network className="w-4 h-4" />
                  <span>Create Another Graph</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
