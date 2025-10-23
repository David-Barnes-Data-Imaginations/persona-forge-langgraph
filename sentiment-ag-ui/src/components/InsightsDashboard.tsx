"use client";

import React from 'react';
import { Brain, Heart, TrendingUp, AlertTriangle, User, FileText } from 'lucide-react';

interface Insight {
  type: string;
  title: string;
  content: string;
  confidence?: number;
  severity?: 'low' | 'medium' | 'high';
  category?: string;
}

interface InsightsDashboardProps {
  insights: Insight[];
}

export function InsightsDashboard({ insights }: InsightsDashboardProps) {
  const getInsightIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'emotion':
      case 'emotional':
        return <Heart className="h-5 w-5" />;
      case 'cognitive':
      case 'distortion':
        return <Brain className="h-5 w-5" />;
      case 'personality':
      case 'trait':
        return <User className="h-5 w-5" />;
      case 'trend':
      case 'pattern':
        return <TrendingUp className="h-5 w-5" />;
      case 'risk':
      case 'warning':
        return <AlertTriangle className="h-5 w-5" />;
      case 'therapy_note':
      case 'clinical':
        return <FileText className="h-5 w-5" />;
      default:
        return <FileText className="h-5 w-5" />;
    }
  };

  const getInsightColor = (severity?: string, confidence?: number) => {
    if (severity) {
      switch (severity) {
        case 'high':
          return 'border-red-500 bg-red-500/10 text-red-300';
        case 'medium':
          return 'border-yellow-500 bg-yellow-500/10 text-yellow-300';
        case 'low':
          return 'border-green-500 bg-green-500/10 text-green-300';
      }
    }
    
    if (confidence !== undefined) {
      if (confidence > 0.8) return 'border-green-500 bg-green-500/10 text-green-300';
      if (confidence > 0.6) return 'border-yellow-500 bg-yellow-500/10 text-yellow-300';
      return 'border-red-500 bg-red-500/10 text-red-300';
    }
    
    return 'border-slate-500 bg-slate-500/10 text-slate-300';
  };

  const formatConfidence = (confidence?: number) => {
    if (confidence === undefined) return null;
    return `${Math.round(confidence * 100)}% confidence`;
  };

  if (!insights || insights.length === 0) {
    return (
      <div className="text-slate-400 text-center py-8">
        No insights available yet. Ask the AI to analyze psychological data.
      </div>
    );
  }

  return (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      {insights.map((insight, index) => (
        <div
          key={index}
          className={`p-4 rounded-lg border transition-all duration-200 hover:scale-[1.02] ${getInsightColor(
            insight.severity,
            insight.confidence
          )}`}
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 mt-1">
              {getInsightIcon(insight.type)}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-sm truncate">
                  {insight.title}
                </h3>
                {insight.confidence && (
                  <span className="text-xs opacity-75 ml-2">
                    {formatConfidence(insight.confidence)}
                  </span>
                )}
              </div>
              
              <p className="text-sm opacity-90 leading-relaxed">
                {insight.content}
              </p>
              
              <div className="flex items-center gap-2 mt-2">
                {insight.category && (
                  <span className="text-xs px-2 py-1 rounded-full bg-slate-700 text-slate-300">
                    {insight.category}
                  </span>
                )}
                {insight.severity && (
                  <span className="text-xs px-2 py-1 rounded-full bg-slate-700 text-slate-300">
                    {insight.severity} severity
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// Helper component for creating insights from raw data
export function createInsightsFromData(data: any, type: string): Insight[] {
  const insights: Insight[] = [];
  
  switch (type) {
    case 'personality_summary':
      if (data.big_five) {
        const traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'];
        traits.forEach(trait => {
          const value = data.big_five[trait];
          if (value !== undefined) {
            let severity: 'low' | 'medium' | 'high' = 'medium';
            let content = '';
            
            if (value > 0.7) {
              severity = 'high';
              content = `High ${trait} (${Math.round(value * 100)}%) - This suggests strong tendencies in this personality dimension.`;
            } else if (value < 0.3) {
              severity = 'low';
              content = `Low ${trait} (${Math.round(value * 100)}%) - This suggests weaker tendencies in this personality dimension.`;
            } else {
              content = `Moderate ${trait} (${Math.round(value * 100)}%) - This suggests balanced tendencies in this personality dimension.`;
            }
            
            insights.push({
              type: 'personality',
              title: `${trait.charAt(0).toUpperCase() + trait.slice(1)} Trait`,
              content,
              confidence: data.big_five.confidence || 0.7,
              severity,
              category: 'Big Five'
            });
          }
        });
      }
      break;
      
    case 'emotions':
      if (Array.isArray(data)) {
        data.forEach((emotion: any) => {
          if (emotion.valence !== undefined) {
            const valenceLevel = emotion.valence > 0.5 ? 'positive' : emotion.valence < -0.5 ? 'negative' : 'neutral';
            const arousalLevel = emotion.arousal > 0.7 ? 'high' : emotion.arousal < 0.3 ? 'low' : 'moderate';
            
            insights.push({
              type: 'emotion',
              title: `${emotion.name || 'Emotion'} Detected`,
              content: `${valenceLevel} emotion with ${arousalLevel} arousal (valence: ${emotion.valence?.toFixed(2)}, arousal: ${emotion.arousal?.toFixed(2)})`,
              confidence: emotion.confidence,
              category: 'Emotional State'
            });
          }
        });
      }
      break;
      
    case 'extreme_values':
      if (Array.isArray(data)) {
        data.forEach((item: any, index: number) => {
          insights.push({
            type: 'pattern',
            title: `Extreme Value #${index + 1}`,
            content: `${item.emotion || item.property || 'Value'}: ${item.value?.toFixed(2) || 'N/A'} - This represents an outlier in the psychological profile.`,
            severity: Math.abs(item.value || 0) > 0.8 ? 'high' : 'medium',
            category: 'Outlier Analysis'
          });
        });
      }
      break;
      
    default:
      // Generic insight creation
      insights.push({
        type: 'general',
        title: `${type} Analysis`,
        content: `Analysis completed for ${type}. Review the data for detailed insights.`,
        category: 'General Analysis'
      });
  }
  
  return insights;
}
