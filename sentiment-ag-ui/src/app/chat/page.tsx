"use client";

import { useCopilotAction, useCopilotChat } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";
import { PsychologicalVisualization } from "@/components/PsychologicalVisualization";
import { InsightsDashboard } from "@/components/InsightsDashboard";
import { CircumplexVisualization } from "@/components/CircumplexVisualization";
import { DeepAgentDashboard } from "@/components/DeepAgentDashboard";
import VoiceControl from "@/components/VoiceControl";
import { getBackendUrl } from "@/lib/config";
import Header from "@/components/Header";

// Agent state type - this should match your LangGraph agent state
type SentimentAgentState = {
  visualizations: any[];
  insights: any[];
  circumplex_data: any;
  deep_agent_state: any;
  current_analysis: string;
}

export default function CopilotKitPage() {
  const [themeColor, setThemeColor] = useState("#6366f1");

  // State management for psychological analysis
  const [state, setState] = useState<SentimentAgentState>({
    visualizations: [],
    insights: [],
    circumplex_data: null,
    deep_agent_state: null,
    current_analysis: "Ready to analyze psychological data",
  });

  const [mainTheme, setMainTheme] = useState({
    primary: "purple",
    gradient: "from-slate-900 via-purple-900 to-slate-900"
  });

  // Get CopilotKit's chat functions
  const copilotChat = useCopilotChat();

  const handleTranscript = (transcript: string) => {
    console.log("🎤 Voice transcript received:", transcript);
    
    // Update state to show the transcript
    setState({
      ...state,
      current_analysis: `🎤 Voice: "${transcript}"`,
    });
    
    // IMPORTANT: Inject the transcript into the CopilotKit sidebar
    // We'll trigger the chat input by finding the textarea and simulating user input
    setTimeout(() => {
      console.log("🔍 Looking for chat input textarea...");
      
      // Try multiple selectors to find the chat input
      let chatInput = document.querySelector('textarea[placeholder*="Message"]') as HTMLTextAreaElement;
      
      if (!chatInput) {
        console.log("⚠️ Trying alternative selector...");
        chatInput = document.querySelector('textarea') as HTMLTextAreaElement;
      }
      
      if (chatInput) {
        console.log("✅ Found chat input, setting value:", transcript);
        
        // Get the form that contains the textarea
        const form = chatInput.closest('form');
        console.log("📝 Found form:", form ? "YES" : "NO");
        
        // Set the value
        chatInput.value = transcript;
        
        // Trigger multiple events to ensure React picks it up
        const inputEvent = new Event('input', { bubbles: true });
        const changeEvent = new Event('change', { bubbles: true });
        chatInput.dispatchEvent(inputEvent);
        chatInput.dispatchEvent(changeEvent);
        
        // Focus the input
        chatInput.focus();
        
        console.log("🔍 Looking for send button...");
        
        // Method 1: Try to find submit button
        let sendButton = document.querySelector('button[type="submit"]') as HTMLButtonElement;
        
        if (!sendButton && form) {
          // Look for button inside the form
          sendButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;
        }
        
        if (!sendButton) {
          console.log("⚠️ Trying alternative button selectors...");
          // Look for button with aria-label
          sendButton = document.querySelector('button[aria-label*="Send"]') as HTMLButtonElement;
        }
        
        if (!sendButton) {
          // Try finding button with SVG icon (send icon)
          const buttons = Array.from(document.querySelectorAll('button'));
          sendButton = buttons.find(btn => {
            const svg = btn.querySelector('svg');
            const hasIcon = svg && (
              svg.innerHTML.includes('path') || 
              svg.innerHTML.includes('polygon')
            );
            return hasIcon || 
              btn.textContent?.toLowerCase().includes('send') ||
              btn.getAttribute('aria-label')?.toLowerCase().includes('send');
          }) as HTMLButtonElement;
          
          if (sendButton) {
            console.log("✅ Found button with icon!");
          }
        }
        
        if (sendButton) {
          setTimeout(() => {
            console.log("✅ Clicking send button!");
            sendButton.click();
            console.log("✅ Voice input sent to chat!");
          }, 200);
        } else if (form) {
          // Try submitting the form directly
          console.log("📤 Trying to submit form directly...");
          setTimeout(() => {
            const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
            form.dispatchEvent(submitEvent);
            console.log("✅ Form submitted!");
          }, 200);
        } else {
          console.error("❌ Could not find send button or form. Trying Enter key...");
          // Fallback: trigger Enter key (without Shift for submission)
          const enterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            bubbles: true,
            cancelable: true
          });
          chatInput.dispatchEvent(enterEvent);
          
          // Also try keypress and keyup
          const keypressEvent = new KeyboardEvent('keypress', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            bubbles: true,
            cancelable: true
          });
          chatInput.dispatchEvent(keypressEvent);
        }
      } else {
        console.error("❌ Could not find chat input textarea!");
        console.log("Available textareas:", document.querySelectorAll('textarea'));
      }
    }, 100);
  };

  const playAudio = async (text: string) => {
    try {
      const response = await fetch(getBackendUrl(`/api/voice/synthesize?text=${encodeURIComponent(text)}`), {
        method: 'POST',
      });
      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
      }
    } catch (error) {
      console.error("Error synthesizing voice:", error);
    }
  };

  // Note: Auto-playing TTS for responses is commented out for now
  // You can enable this later by tracking when the assistant responds
  // useEffect(() => {
  //   // Play audio when assistant responds
  // }, []);

  // 🪁 Frontend Actions: https://docs.copilotkit.ai/coagents/frontend-actions
  useCopilotAction({
    name: "setThemeColor",
    parameters: [{
      name: "themeColor",
      description: "The theme color to set. Make sure to pick nice colors.",
      required: true, 
    }],
    handler({ themeColor }) {
      setThemeColor(themeColor);
    },
  });

  // Action to change main background theme
  useCopilotAction({
    name: "changeMainTheme",
    description: "Change the main background theme of the entire application. Use color names like 'blue', 'green', 'red', 'purple', 'teal', 'orange', etc.",
    parameters: [{
      name: "colorTheme",
      description: "Main color theme (e.g., 'blue', 'green', 'red', 'purple', 'teal', 'orange', 'pink', 'indigo')",
      required: true,
    }],
    handler: ({ colorTheme }) => {
      const themeMap: { [key: string]: { primary: string; gradient: string } } = {
        purple: { primary: "purple", gradient: "from-slate-900 via-purple-900 to-slate-900" },
        blue: { primary: "blue", gradient: "from-slate-900 via-blue-900 to-slate-900" },
        green: { primary: "green", gradient: "from-slate-900 via-green-900 to-slate-900" },
        red: { primary: "red", gradient: "from-slate-900 via-red-900 to-slate-900" },
        teal: { primary: "teal", gradient: "from-slate-900 via-teal-900 to-slate-900" },
        orange: { primary: "orange", gradient: "from-slate-900 via-orange-900 to-slate-900" },
        pink: { primary: "pink", gradient: "from-slate-900 via-pink-900 to-slate-900" },
        indigo: { primary: "indigo", gradient: "from-slate-900 via-indigo-900 to-slate-900" },
        emerald: { primary: "emerald", gradient: "from-slate-900 via-emerald-900 to-slate-900" },
        cyan: { primary: "cyan", gradient: "from-slate-900 via-cyan-900 to-slate-900" },
        amber: { primary: "amber", gradient: "from-slate-900 via-amber-900 to-slate-900" },
        violet: { primary: "violet", gradient: "from-slate-900 via-violet-900 to-slate-900" },
      };

      const selectedTheme = themeMap[colorTheme.toLowerCase()] || themeMap.purple;
      setMainTheme(selectedTheme);

      setState({
        ...state,
        current_analysis: `🎨 Main theme changed to ${colorTheme}! The entire background is now ${colorTheme}-themed.`,
      });

      return `✅ Main theme successfully changed to ${colorTheme}! The entire application background is now ${colorTheme}-themed.`;
    },
  });

  // Action to analyze emotions and create visualizations
  useCopilotAction({
    name: "analyzeEmotions",
    description: "IMMEDIATELY analyze emotional patterns from the existing therapy session data in the Neo4j database and create visualizations. Do not ask for session data - it already exists in the system.",
    parameters: [{
      name: "query",
      description: "Optional query to filter the emotional analysis",
      required: false,
    }],
    handler: async ({ query }) => {
      try {
        // Call your FastAPI backend for emotional analysis
        const response = await fetch(getBackendUrl("/visualize"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            data_type: "emotions",
            query: query || "emotional patterns feelings",
            session_id: "session_001",
          }),
        });

        if (response.ok) {
          const data = await response.json();

          // Parse emotional data from the insights text
          const insights = data.data.insights || "";
          const emotions = [];

          // Extract emotion data using regex patterns
          const emotionMatches = insights.matchAll(/(\w+) valence ([\d.]+) arousal ([\d.]+) conf ([\d.]+)/g);
          for (const match of emotionMatches) {
            emotions.push({
              name: match[1],
              valence: parseFloat(match[2]),
              arousal: parseFloat(match[3]),
              confidence: parseFloat(match[4])
            });
          }

          // If no emotions found, create some sample data from the text
          if (emotions.length === 0) {
            const emotionWords = ['Empathy', 'Detachment', 'Fulfillment', 'Calm'];
            emotionWords.forEach((emotion, index) => {
              if (insights.toLowerCase().includes(emotion.toLowerCase())) {
                emotions.push({
                  name: emotion,
                  valence: 0.3 + (index * 0.2),
                  arousal: 0.2 + (index * 0.15),
                  confidence: 0.7 + (index * 0.05)
                });
              }
            });
          }

          setState({
            ...state,
            visualizations: [...(state.visualizations || []), {
              type: "emotions",
              data: emotions,
              timestamp: new Date().toISOString(),
            }],
            current_analysis: "Emotional patterns analyzed successfully",
          });
          return "✅ Emotional analysis complete! Check the visualization panel.";
        } else {
          return "❌ Error analyzing emotions. Please try again.";
        }
      } catch (error) {
        return `❌ Error: ${error}`;
      }
    },
  });

  // Action to generate personality analysis
  useCopilotAction({
    name: "analyzePersonality",
    description: "IMMEDIATELY generate Big Five personality analysis from existing therapy session data and create visualization. The data is already in the Neo4j database.",
    parameters: [],
    handler: async () => {
      try {
        const response = await fetch(getBackendUrl("/visualize"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            data_type: "personality",
            session_id: "session_001",
          }),
        });

        if (response.ok) {
          const data = await response.json();

          // Parse Big Five scores from the text summary
          const summary = data.data.summary || "";
          const bigFiveMatch = summary.match(/Big Five Profile: Openness: \w+ \(([\d.]+)\) \| Conscientiousness: \w+ \(([\d.]+)\) \| Extraversion: \w+ \(([\d.]+)\) \| Agreeableness: \w+ \(([\d.]+)\) \| Neuroticism: \w+ \(([\d.]+)\)/);

          let personalityData = {};
          if (bigFiveMatch) {
            personalityData = {
              openness: parseFloat(bigFiveMatch[1]),
              conscientiousness: parseFloat(bigFiveMatch[2]),
              extraversion: parseFloat(bigFiveMatch[3]),
              agreeableness: parseFloat(bigFiveMatch[4]),
              neuroticism: parseFloat(bigFiveMatch[5]),
              summary: summary
            };
          } else {
            // Fallback with default values if parsing fails
            personalityData = {
              openness: 0.5,
              conscientiousness: 0.5,
              extraversion: 0.5,
              agreeableness: 0.5,
              neuroticism: 0.5,
              summary: summary
            };
          }

          setState({
            ...state,
            visualizations: [...(state.visualizations || []), {
              type: "personality",
              data: personalityData,
              timestamp: new Date().toISOString(),
            }],
            current_analysis: "Personality analysis complete",
          });
          return "✅ Personality analysis complete! Big Five traits visualized.";
        } else {
          return "❌ Error analyzing personality. Please try again.";
        }
      } catch (error) {
        return `❌ Error: ${error}`;
      }
    },
  });

  // Action to create circumplex visualization
  useCopilotAction({
    name: "createCircumplex",
    description: "IMMEDIATELY create Russell's Circumplex emotional mapping from existing therapy session data in Neo4j. Do not ask for data - use the existing session data.",
    parameters: [{
      name: "query",
      description: "Optional query to filter emotions for circumplex",
      required: false,
    }],
    handler: async ({ query }) => {
      try {
        const response = await fetch(getBackendUrl("/circumplex"), {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            data_type: "emotions",
            query: query || "emotions valence arousal",
            session_id: "session_001",
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setState({
            ...state,
            circumplex_data: {
              emotions: data.emotions,
              title: data.title || "Emotional Circumplex Analysis",
            },
            current_analysis: "Circumplex visualization created",
          });
          return "✅ Circumplex visualization created! Check the emotional mapping panel.";
        } else {
          return "❌ Error creating circumplex. Please try again.";
        }
      } catch (error) {
        return `❌ Error: ${error}`;
      }
    },
  });

  // Action to read therapy note
  useCopilotAction({
    name: "readTherapyNote",
    description: "IMMEDIATELY read and display the therapy note from the output file. This contains the psychological insights and treatment plan.",
    parameters: [],
    handler: async () => {
      try {
        // Call FastAPI backend to read the therapy note file
        const response = await fetch(getBackendUrl("/read-therapy-note"), {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
          const data = await response.json();

          // Format the therapy note as a proper insight
          const therapyInsight = {
            type: "therapy_note",
            title: "Complete Psychological Assessment & Treatment Plan",
            content: data.content,
            confidence: 0.95,
            severity: "medium" as const,
            category: "Clinical Assessment",
            timestamp: new Date().toISOString(),
          };

          setState({
            ...state,
            insights: [...(state.insights || []), therapyInsight],
            current_analysis: "Therapy note loaded successfully",
          });
          return "✅ Therapy note loaded! Check the Psychological Insights panel for the complete assessment.";
        } else {
          return "❌ Error reading therapy note. Please try again.";
        }
      } catch (error) {
        return `❌ Error: ${error}`;
      }
    },
  });

  return (
    <main style={{ "--copilot-kit-primary-color": themeColor } as CopilotKitCSSProperties}>
      <Header />
      <YourMainContent themeColor={themeColor} state={state} mainTheme={mainTheme} />
      <VoiceControl handleTranscript={handleTranscript} />
      <CopilotSidebar
        clickOutsideToClose={false}
        defaultOpen={true}
        labels={{
          title: "Persona Forge AI Assistant",
          initial: "👋 Hi! I'm your psychological analysis assistant.\n\n🎤 **Voice Mode**: Click the blue microphone button to speak!\n\nI can help you:\n\n- **Analyze Emotions**: \"Show me emotional patterns\"\n- **Personality Analysis**: \"Generate Big Five summary\"\n- **Statistical Overview**: \"Show psychological patterns\"\n- **Circumplex Visualization**: \"Create emotional circumplex\"\n- **Read Therapy Note**: \"Show the therapy assessment\"\n\nTry typing or speaking any command!"
        }}
        suggestions={[
          {
            title: "Analyze Emotions",
            message: "Use the analyzeEmotions tool to pull emotional patterns from the therapy session data and create visualizations now."
          },
          {
            title: "Personality Summary",
            message: "Use the analyzePersonality tool to generate Big Five personality analysis from the session data now."
          },
          {
            title: "Create Circumplex",
            message: "Use the createCircumplex tool to generate Russell's Circumplex emotional mapping from the session data now."
          },
          {
            title: "Statistical Overview",
            message: "Use the analyzeEmotions tool with query 'statistics' to show statistical analysis of psychological patterns."
          },
          {
            title: "Extreme Values",
            message: "Use the analyzeEmotions tool with query 'extreme values' to find the most extreme emotional responses."
          },
          {
            title: "Therapy Note",
            message: "Use the readTherapyNote tool to display the complete psychological assessment and treatment plan."
          },

        ]}
      />
    </main>
  );
}

function YourMainContent({ themeColor, state, mainTheme }: {
  themeColor: string,
  state: SentimentAgentState,
  mainTheme: { primary: string; gradient: string }
}) {
  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <main className="flex-1 p-6 overflow-auto">
        <div className="max-w-7xl mx-auto">
          <header className="mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Persona Forge AI Chat
            </h1>
            <h2 className="text-xl font-medium text-gray-600 mb-2">
              AI-powered psychological analysis and insights.
            </h2>
            {state.current_analysis && (
              <div className={`mt-3 p-3 rounded-lg ${
                state.current_analysis.includes("Voice") 
                  ? "bg-blue-100 border border-blue-300" 
                  : "bg-gray-100 border border-gray-300"
              }`}>
                <p className="text-gray-700 text-sm">
                  {state.current_analysis}
                </p>
              </div>
            )}
          </header>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Visualization Panel */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border border-blue-100 shadow-lg">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Data Visualizations
              </h2>
              {state.visualizations && state.visualizations.length > 0 ? (
                <div className="space-y-4">
                  {state.visualizations.map((viz, index) => (
                    <PsychologicalVisualization 
                      key={index}
                      type={viz.type} 
                      data={viz.data} 
                    />
                  ))}
                </div>
              ) : (
                <div className="text-gray-400 text-center py-12">
                  Ask the AI to visualize psychological data to see charts here
                </div>
              )}
            </div>

            {/* Insights Panel */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border border-blue-100 shadow-lg">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Psychological Insights
              </h2>
              {state.insights && state.insights.length > 0 ? (
                <InsightsDashboard insights={state.insights} />
              ) : (
                <div className="text-gray-400 text-center py-12">
                  Ask the AI for psychological insights to see analysis here
                </div>
              )}
            </div>

            {/* Circumplex Panel */}
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border border-blue-100 shadow-lg">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Emotional Circumplex
              </h2>
              {state.circumplex_data ? (
                <CircumplexVisualization 
                  emotions={state.circumplex_data.emotions} 
                  title={state.circumplex_data.title} 
                />
              ) : (
                <div className="text-gray-400 text-center py-12">
                  Ask the AI to create a circumplex plot to see emotional mapping here
                </div>
              )}
            </div>
          </div>

          {/* Deep Agent Dashboard - Full Width */}
          {state.deep_agent_state && (
            <div className="mt-6">
              <DeepAgentDashboard agentState={state.deep_agent_state} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
