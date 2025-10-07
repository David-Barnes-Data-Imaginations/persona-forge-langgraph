"use client";

import React from 'react';
import dynamic from 'next/dynamic';
import { Loader2 } from 'lucide-react';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-64">
      <Loader2 className="h-8 w-8 animate-spin text-purple-400" />
    </div>
  ),
});

interface EmotionPoint {
  name: string;
  valence: number;
  arousal: number;
  confidence?: number;
}

interface CircumplexVisualizationProps {
  emotions: EmotionPoint[];
  title?: string;
}

export function CircumplexVisualization({ emotions, title = "Russell's Circumplex Model" }: CircumplexVisualizationProps) {
  // Create the base circumplex circle
  const createCircumplexBase = () => {
    const theta = Array.from({ length: 100 }, (_, i) => (i * 2 * Math.PI) / 100);
    const x = theta.map(t => Math.cos(t));
    const y = theta.map(t => Math.sin(t));
    
    return {
      x: x,
      y: y,
      mode: 'lines',
      type: 'scatter',
      line: { color: 'rgba(255,255,255,0.3)', width: 2 },
      showlegend: false,
      hoverinfo: 'skip'
    };
  };

  // Create quadrant lines
  const createQuadrantLines = () => {
    return [
      // Vertical line (valence axis)
      {
        x: [0, 0],
        y: [-1.2, 1.2],
        mode: 'lines',
        type: 'scatter',
        line: { color: 'rgba(255,255,255,0.2)', width: 1, dash: 'dash' },
        showlegend: false,
        hoverinfo: 'skip'
      },
      // Horizontal line (arousal axis)
      {
        x: [-1.2, 1.2],
        y: [0, 0],
        mode: 'lines',
        type: 'scatter',
        line: { color: 'rgba(255,255,255,0.2)', width: 1, dash: 'dash' },
        showlegend: false,
        hoverinfo: 'skip'
      }
    ];
  };

  // Create emotion points
  const createEmotionPoints = () => {
    if (!emotions || emotions.length === 0) {
      return [];
    }

    return [{
      x: emotions.map(e => e.valence),
      y: emotions.map(e => e.arousal),
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        size: emotions.map(e => (e.confidence || 0.5) * 20 + 10),
        color: emotions.map(e => {
          // Color based on quadrant
          if (e.valence > 0 && e.arousal > 0) return 'rgba(34, 197, 94, 0.8)'; // High arousal, positive valence (excited)
          if (e.valence < 0 && e.arousal > 0) return 'rgba(239, 68, 68, 0.8)'; // High arousal, negative valence (distressed)
          if (e.valence < 0 && e.arousal < 0) return 'rgba(59, 130, 246, 0.8)'; // Low arousal, negative valence (depressed)
          return 'rgba(168, 85, 247, 0.8)'; // Low arousal, positive valence (relaxed)
        }),
        line: { color: 'white', width: 2 },
        opacity: 0.8
      },
      text: emotions.map(e => e.name),
      textposition: 'top center',
      textfont: { color: 'white', size: 10 },
      hovertemplate: 
        '<b>%{text}</b><br>' +
        'Valence: %{x:.2f}<br>' +
        'Arousal: %{y:.2f}<br>' +
        '<extra></extra>',
      name: 'Emotions'
    }];
  };

  // Create quadrant labels
  const createQuadrantLabels = () => {
    return [
      {
        x: [0.7],
        y: [0.7],
        mode: 'text',
        type: 'scatter',
        text: ['High Arousal<br>Positive Valence<br>(Excited, Happy)'],
        textfont: { color: 'rgba(34, 197, 94, 0.8)', size: 10 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [-0.7],
        y: [0.7],
        mode: 'text',
        type: 'scatter',
        text: ['High Arousal<br>Negative Valence<br>(Angry, Stressed)'],
        textfont: { color: 'rgba(239, 68, 68, 0.8)', size: 10 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [-0.7],
        y: [-0.7],
        mode: 'text',
        type: 'scatter',
        text: ['Low Arousal<br>Negative Valence<br>(Sad, Depressed)'],
        textfont: { color: 'rgba(59, 130, 246, 0.8)', size: 10 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [0.7],
        y: [-0.7],
        mode: 'text',
        type: 'scatter',
        text: ['Low Arousal<br>Positive Valence<br>(Calm, Relaxed)'],
        textfont: { color: 'rgba(168, 85, 247, 0.8)', size: 10 },
        showlegend: false,
        hoverinfo: 'skip'
      }
    ];
  };

  // Create axis labels
  const createAxisLabels = () => {
    return [
      {
        x: [1.1],
        y: [0],
        mode: 'text',
        type: 'scatter',
        text: ['Positive'],
        textfont: { color: 'white', size: 12 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [-1.1],
        y: [0],
        mode: 'text',
        type: 'scatter',
        text: ['Negative'],
        textfont: { color: 'white', size: 12 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [0],
        y: [1.1],
        mode: 'text',
        type: 'scatter',
        text: ['High Arousal'],
        textfont: { color: 'white', size: 12 },
        showlegend: false,
        hoverinfo: 'skip'
      },
      {
        x: [0],
        y: [-1.1],
        mode: 'text',
        type: 'scatter',
        text: ['Low Arousal'],
        textfont: { color: 'white', size: 12 },
        showlegend: false,
        hoverinfo: 'skip'
      }
    ];
  };

  const plotData = [
    createCircumplexBase(),
    ...createQuadrantLines(),
    ...createEmotionPoints(),
    ...createQuadrantLabels(),
    ...createAxisLabels()
  ];

  const layout = {
    title: {
      text: title,
      font: { color: 'white', size: 18 }
    },
    xaxis: {
      title: 'Valence',
      range: [-1.3, 1.3],
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      color: 'white'
    },
    yaxis: {
      title: 'Arousal',
      range: [-1.3, 1.3],
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      color: 'white'
    },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
    font: { color: 'white' },
    height: 500,
    width: 500,
    showlegend: false
  };

  return (
    <div className="w-full flex justify-center">
      <Plot data={plotData} layout={layout} />
    </div>
  );
}
