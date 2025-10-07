"use client";

import React, { useState, useEffect } from 'react';
import { Brain, CheckCircle, Clock, AlertCircle, FileText, Search, Lightbulb } from 'lucide-react';

interface Todo {
  id: string;
  task: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at?: string;
}

interface AgentThought {
  id: string;
  content: string;
  type: 'reasoning' | 'observation' | 'plan' | 'reflection';
  timestamp: string;
  confidence?: number;
}

interface DeepAgentState {
  current_task?: string;
  todos: Todo[];
  thoughts: AgentThought[];
  status: 'idle' | 'thinking' | 'working' | 'completed' | 'error';
  progress?: number;
}

interface DeepAgentDashboardProps {
  agentState: DeepAgentState;
  onTaskUpdate?: (taskId: string, status: Todo['status']) => void;
}

export function DeepAgentDashboard({ agentState, onTaskUpdate }: DeepAgentDashboardProps) {
  const [selectedThought, setSelectedThought] = useState<AgentThought | null>(null);

  const getStatusIcon = (status: Todo['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'in_progress':
        return <Clock className="h-4 w-4 text-yellow-400 animate-spin" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-400" />;
      default:
        return <Clock className="h-4 w-4 text-slate-400" />;
    }
  };

  const getThoughtIcon = (type: AgentThought['type']) => {
    switch (type) {
      case 'reasoning':
        return <Brain className="h-4 w-4 text-purple-400" />;
      case 'observation':
        return <Search className="h-4 w-4 text-blue-400" />;
      case 'plan':
        return <FileText className="h-4 w-4 text-green-400" />;
      case 'reflection':
        return <Lightbulb className="h-4 w-4 text-yellow-400" />;
      default:
        return <Brain className="h-4 w-4 text-slate-400" />;
    }
  };

  const getPriorityColor = (priority: Todo['priority']) => {
    switch (priority) {
      case 'high':
        return 'border-red-500 bg-red-500/10';
      case 'medium':
        return 'border-yellow-500 bg-yellow-500/10';
      case 'low':
        return 'border-green-500 bg-green-500/10';
      default:
        return 'border-slate-500 bg-slate-500/10';
    }
  };

  const getStatusColor = (status: DeepAgentState['status']) => {
    switch (status) {
      case 'thinking':
        return 'text-purple-400';
      case 'working':
        return 'text-blue-400';
      case 'completed':
        return 'text-green-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-slate-400';
    }
  };

  const todos = agentState?.todos || [];
  const completedTodos = todos.filter(todo => todo.status === 'completed').length;
  const totalTodos = todos.length;
  const progressPercentage = totalTodos > 0 ? (completedTodos / totalTodos) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Agent Status Header */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white flex items-center gap-2">
            <Brain className="h-6 w-6 text-purple-400" />
            Deep Agent Status
          </h2>
          <span className={`text-sm font-medium ${getStatusColor(agentState?.status || 'idle')}`}>
            {(agentState?.status || 'idle').toUpperCase()}
          </span>
        </div>

        {agentState?.current_task && (
          <div className="mb-4">
            <p className="text-slate-300 text-sm mb-2">Current Task:</p>
            <p className="text-white font-medium">{agentState.current_task}</p>
          </div>
        )}

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-slate-400 mb-2">
            <span>Progress</span>
            <span>{completedTodos}/{totalTodos} tasks completed</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-purple-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* TODO List */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Task List</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {todos.length === 0 ? (
              <p className="text-slate-400 text-center py-8">No tasks available</p>
            ) : (
              todos.map((todo) => (
                <div
                  key={todo.id}
                  className={`p-3 rounded-lg border transition-all duration-200 hover:scale-[1.02] ${getPriorityColor(todo.priority)}`}
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {getStatusIcon(todo.status)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm font-medium mb-1">
                        {todo.task}
                      </p>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="text-slate-400">
                          {new Date(todo.created_at).toLocaleTimeString()}
                        </span>
                        <span className={`px-2 py-1 rounded-full bg-slate-700 text-slate-300`}>
                          {todo.priority}
                        </span>
                        <span className={`px-2 py-1 rounded-full bg-slate-700 text-slate-300`}>
                          {todo.status}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Agent Thoughts */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Agent Thoughts</h3>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {(agentState?.thoughts || []).length === 0 ? (
              <p className="text-slate-400 text-center py-8">No thoughts recorded</p>
            ) : (
              (agentState?.thoughts || []).map((thought) => (
                <div
                  key={thought.id}
                  className="p-3 rounded-lg border border-slate-600 bg-slate-700/30 hover:bg-slate-700/50 transition-all duration-200 cursor-pointer"
                  onClick={() => setSelectedThought(thought)}
                >
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 mt-1">
                      {getThoughtIcon(thought.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white text-sm mb-1 line-clamp-2">
                        {thought.content}
                      </p>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="text-slate-400">
                          {new Date(thought.timestamp).toLocaleTimeString()}
                        </span>
                        <span className="px-2 py-1 rounded-full bg-slate-600 text-slate-300">
                          {thought.type}
                        </span>
                        {thought.confidence && (
                          <span className="px-2 py-1 rounded-full bg-slate-600 text-slate-300">
                            {Math.round(thought.confidence * 100)}% confidence
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Thought Detail Modal */}
      {selectedThought && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-800 rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                {getThoughtIcon(selectedThought.type)}
                {selectedThought.type.charAt(0).toUpperCase() + selectedThought.type.slice(1)}
              </h3>
              <button
                onClick={() => setSelectedThought(null)}
                className="text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            <div className="text-slate-300 mb-4">
              {new Date(selectedThought.timestamp).toLocaleString()}
            </div>
            <p className="text-white leading-relaxed">
              {selectedThought.content}
            </p>
            {selectedThought.confidence && (
              <div className="mt-4 text-sm text-slate-400">
                Confidence: {Math.round(selectedThought.confidence * 100)}%
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
