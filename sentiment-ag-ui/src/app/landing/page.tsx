import Link from 'next/link';
import { FileText, Network, MessageSquare, Mic, TrendingUp } from 'lucide-react';
import Header from '@/components/Header';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <Header />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Transform Therapy Analysis
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Leverage cutting-edge AI to analyze therapy sessions with multiple psychological
            frameworks, knowledge graphs, and hybrid RAG technology.
          </p>
        </div>

        {/* Status Banner */}
        <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6 mb-12">
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div className="flex items-center justify-center space-x-3">
              <Mic className="w-6 h-6 text-purple-600" />
              <div className="text-left">
                <p className="font-semibold text-gray-900">Voice Features</p>
                <p className="text-sm text-gray-600">Faster-Whisper + Piper TTS</p>
              </div>
            </div>
            <div className="flex items-center justify-center space-x-3">
              <Network className="w-6 h-6 text-indigo-600" />
              <div className="text-left">
                <p className="font-semibold text-gray-900">Analysis Engine</p>
                <p className="text-sm text-gray-600">Hybrid Graph-RAG with LangGraph</p>
              </div>
            </div>
            <div className="flex items-center justify-center space-x-3">
              <TrendingUp className="w-6 h-6 text-green-600" />
              <div className="text-left">
                <p className="font-semibold text-gray-900">Frameworks</p>
                <p className="text-sm text-gray-600">7 Psychological Models</p>
              </div>
            </div>
          </div>
        </div>

        {/* Workflow Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Voice Chat Card */}
          <div className="bg-white rounded-xl shadow-lg border-l-4 border-purple-500 hover:shadow-xl transition-shadow">
            <div className="p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <MessageSquare className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Voice-Enabled Chat</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Interactive chat interface with speech-to-text and text-to-speech capabilities.
                Query your therapy data using voice commands.
              </p>
              <div className="space-y-2 mb-6">
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                  <span>Voice input with Faster-Whisper</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                  <span>Text-to-speech responses with Piper</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-purple-500 rounded-full"></span>
                  <span>Hybrid Graph-RAG integration</span>
                </div>
              </div>
              <Link
                href="/chat"
                className="block w-full px-4 py-2 bg-purple-600 text-white text-center rounded-lg hover:bg-purple-700 transition-colors"
              >
                Launch Chat Interface
              </Link>
            </div>
          </div>

          {/* Workflow 1: Framework Analysis */}
          <div className="bg-white rounded-xl shadow-lg border-l-4 border-orange-500 hover:shadow-xl transition-shadow">
            <div className="p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-3 bg-orange-100 rounded-lg">
                  <FileText className="w-6 h-6 text-orange-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Framework Analysis</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Upload therapy session transcripts for comprehensive psychological analysis using
                multiple frameworks.
              </p>
              <div className="space-y-2 mb-6">
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
                  <span>7 Psychological frameworks</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
                  <span>Big Five & attachment styles</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
                  <span>Cognitive distortions detection</span>
                </div>
              </div>
              <Link
                href="/framework-analysis"
                className="block w-full px-4 py-2 bg-orange-600 text-white text-center rounded-lg hover:bg-orange-700 transition-colors"
              >
                Upload Therapy Data
              </Link>
            </div>
          </div>

          {/* Workflow 2: Knowledge Graph */}
          <div className="bg-white rounded-xl shadow-lg border-l-4 border-green-500 hover:shadow-xl transition-shadow">
            <div className="p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <Network className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Knowledge Graph</h3>
              </div>
              <p className="text-gray-600 mb-4">
                Create knowledge graphs from analysis results with embeddings for hybrid graph-RAG
                queries.
              </p>
              <div className="space-y-2 mb-6">
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                  <span>Neo4j graph generation</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                  <span>Vector embeddings for RAG</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-700">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                  <span>Hybrid search capabilities</span>
                </div>
              </div>
              <Link
                href="/kg-creation"
                className="block w-full px-4 py-2 bg-green-600 text-white text-center rounded-lg hover:bg-green-700 transition-colors"
              >
                Create Knowledge Graph
              </Link>
            </div>
          </div>
        </div>

        {/* Footer Quick Links */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center space-x-8 px-8 py-4 bg-white rounded-full shadow-md border border-gray-200">
            <span className="text-sm font-semibold text-gray-700">Quick Start:</span>
            <Link href="/chat" className="text-sm text-purple-600 hover:text-purple-700 font-medium">
              Try Voice Chat
            </Link>
            <span className="text-gray-300">|</span>
            <Link
              href="/framework-analysis"
              className="text-sm text-orange-600 hover:text-orange-700 font-medium"
            >
              Upload Therapy Data
            </Link>
            <span className="text-gray-300">|</span>
            <Link
              href="/kg-creation"
              className="text-sm text-green-600 hover:text-green-700 font-medium"
            >
              Create Graph
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
