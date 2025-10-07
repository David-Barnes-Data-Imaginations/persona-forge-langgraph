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

interface PsychologicalVisualizationProps {
  type: string;
  data: any;
}

export function PsychologicalVisualization({ type, data }: PsychologicalVisualizationProps) {
  const renderVisualization = () => {
    switch (type) {
      case 'emotions':
        return renderEmotionVisualization(data);
      case 'personality':
        return renderPersonalityVisualization(data);
      case 'statistics':
        return renderStatisticsVisualization(data);
      case 'extreme_values':
        return renderExtremeValuesVisualization(data);
      default:
        return renderGenericVisualization(data);
    }
  };

  const renderEmotionVisualization = (emotionData: any) => {
    if (!emotionData || !Array.isArray(emotionData)) {
      return <div className="text-slate-400">No emotion data available</div>;
    }

    // Create valence-arousal scatter plot
    const plotData = [{
      x: emotionData.map((e: any) => e.valence || 0),
      y: emotionData.map((e: any) => e.arousal || 0),
      text: emotionData.map((e: any) => e.name || 'Unknown'),
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        size: emotionData.map((e: any) => (e.confidence || 0.5) * 20 + 5),
        color: emotionData.map((e: any) => e.valence || 0),
        colorscale: 'RdYlBu',
        showscale: true,
        colorbar: {
          title: 'Valence',
          titlefont: { color: 'white' },
          tickfont: { color: 'white' }
        }
      },
      textposition: 'top center',
      textfont: { color: 'white', size: 10 }
    }];

    const layout = {
      title: {
        text: 'Emotional Valence-Arousal Space',
        font: { color: 'white', size: 18 }
      },
      xaxis: {
        title: 'Valence (Negative ← → Positive)',
        range: [-1, 1],
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      yaxis: {
        title: 'Arousal (Low ← → High)',
        range: [0, 1],
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      plot_bgcolor: 'rgba(0,0,0,0)',
      paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: 'white' },
      height: 400
    };

    return <Plot data={plotData} layout={layout} style={{ width: '100%' }} />;
  };

  const renderPersonalityVisualization = (personalityData: any) => {
    if (!personalityData || typeof personalityData !== 'object') {
      return <div className="text-slate-400">No personality data available</div>;
    }

    // Big Five radar chart
    const traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism'];
    const values = traits.map(trait => personalityData[trait] || 0);
    const labels = traits.map(trait => trait.charAt(0).toUpperCase() + trait.slice(1));

    const plotData = [{
      type: 'scatterpolar',
      r: [...values, values[0]], // Close the polygon
      theta: [...labels, labels[0]],
      fill: 'toself',
      fillcolor: 'rgba(147, 51, 234, 0.3)',
      line: { color: 'rgb(147, 51, 234)' },
      marker: { color: 'rgb(147, 51, 234)', size: 8 },
      name: 'Big Five Traits'
    }];

    const layout = {
      title: {
        text: 'Big Five Personality Profile',
        font: { color: 'white', size: 18 }
      },
      polar: {
        radialaxis: {
          visible: true,
          range: [0, 1],
          gridcolor: 'rgba(255,255,255,0.2)',
          color: 'white'
        },
        angularaxis: {
          gridcolor: 'rgba(255,255,255,0.2)',
          color: 'white'
        }
      },
      plot_bgcolor: 'rgba(0,0,0,0)',
      paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: 'white' },
      height: 400
    };

    return <Plot data={plotData} layout={layout} style={{ width: '100%' }} />;
  };

  const renderStatisticsVisualization = (statsData: any) => {
    if (!statsData || typeof statsData !== 'object') {
      return <div className="text-slate-400">No statistics data available</div>;
    }

    // Handle different types of statistics data
    if (statsData.raw_result && typeof statsData.raw_result === 'string') {
      // Parse text-based statistics from hybrid_rag_tools
      const lines = statsData.raw_result.split('\n');
      const categories: string[] = [];
      const values: number[] = [];

      lines.forEach((line: string) => {
        // Look for patterns like "Emotions: 15" or "Total QA pairs: 30"
        const match = line.match(/([^:]+):\s*(\d+)/);
        if (match) {
          categories.push(match[1].trim());
          values.push(parseInt(match[2]));
        }
      });

      if (categories.length === 0) {
        return (
          <div className="text-slate-400">
            <p>Statistics data (raw format):</p>
            <pre className="text-xs mt-2 bg-slate-900 p-4 rounded overflow-auto max-h-64">
              {statsData.raw_result}
            </pre>
          </div>
        );
      }

      const plotData = [{
        x: categories,
        y: values,
        type: 'bar',
        marker: {
          color: values.map((_, i) => `hsl(${(i * 360) / values.length}, 70%, 60%)`),
          line: { color: 'rgba(255,255,255,0.3)', width: 1 }
        }
      }];

      const layout = {
        title: {
          text: 'Psychological Statistics Overview',
          font: { color: 'white', size: 18 }
        },
        xaxis: {
          title: 'Categories',
          gridcolor: 'rgba(255,255,255,0.1)',
          color: 'white',
          tickangle: -45
        },
        yaxis: {
          title: 'Count',
          gridcolor: 'rgba(255,255,255,0.1)',
          color: 'white'
        },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: 'white' },
        height: 400,
        margin: { b: 100 }
      };

      return <Plot data={plotData} layout={layout} style={{ width: '100%' }} />;
    }

    // Handle structured data
    const categories = Object.keys(statsData);
    const values = Object.values(statsData).map((v: any) =>
      typeof v === 'number' ? v : (Array.isArray(v) ? v.length : 0)
    );

    const plotData = [{
      x: categories,
      y: values,
      type: 'bar',
      marker: {
        color: 'rgba(147, 51, 234, 0.8)',
        line: { color: 'rgb(147, 51, 234)', width: 2 }
      }
    }];

    const layout = {
      title: {
        text: 'Psychological Statistics Overview',
        font: { color: 'white', size: 18 }
      },
      xaxis: {
        title: 'Categories',
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      yaxis: {
        title: 'Count/Value',
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      plot_bgcolor: 'rgba(0,0,0,0)',
      paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: 'white' },
      height: 400
    };

    return <Plot data={plotData} layout={layout} style={{ width: '100%' }} />;
  };

  const renderExtremeValuesVisualization = (extremeData: any) => {
    if (!extremeData || !Array.isArray(extremeData)) {
      return <div className="text-slate-400">No extreme values data available</div>;
    }

    // Create horizontal bar chart for extreme values
    const plotData = [{
      y: extremeData.map((item: any, index: number) => `Item ${index + 1}`),
      x: extremeData.map((item: any) => item.value || 0),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: extremeData.map((item: any) => item.value > 0 ? 'rgba(34, 197, 94, 0.8)' : 'rgba(239, 68, 68, 0.8)'),
      },
      text: extremeData.map((item: any) => item.label || item.emotion || 'Unknown'),
      textposition: 'auto'
    }];

    const layout = {
      title: {
        text: 'Extreme Values Analysis',
        font: { color: 'white', size: 18 }
      },
      xaxis: {
        title: 'Value',
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      yaxis: {
        gridcolor: 'rgba(255,255,255,0.1)',
        color: 'white'
      },
      plot_bgcolor: 'rgba(0,0,0,0)',
      paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: 'white' },
      height: 400
    };

    return <Plot data={plotData} layout={layout} style={{ width: '100%' }} />;
  };

  const renderGenericVisualization = (genericData: any) => {
    return (
      <div className="text-slate-400 text-center py-8">
        <p>Visualization type "{type}" not yet implemented</p>
        <pre className="text-xs mt-4 text-left bg-slate-900 p-4 rounded overflow-auto max-h-32">
          {JSON.stringify(genericData, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className="w-full">
      {renderVisualization()}
    </div>
  );
}
