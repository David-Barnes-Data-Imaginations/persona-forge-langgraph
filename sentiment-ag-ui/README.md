# SentimentSuite AG UI

A modern Next.js frontend for the SentimentSuite psychological analysis platform, powered by CopilotKit and AG UI for seamless AI agent interactions.

## 🚀 Features

### Core Capabilities
- **AI-Powered Chat Interface**: Natural language interaction with psychological analysis agents
- **Real-time Visualizations**: Dynamic charts and graphs for psychological data
- **Russell's Circumplex Model**: Interactive emotional mapping visualization
- **Deep Agent Dashboard**: Real-time monitoring of AI agent workflows
- **Hybrid Graph-RAG Integration**: Advanced retrieval and analysis of therapy session data

### Visualization Components
1. **Psychological Data Visualization**
   - Emotion valence-arousal scatter plots
   - Big Five personality radar charts
   - Statistical overview bar charts
   - Extreme values analysis

2. **Circumplex Visualization**
   - Russell's Circumplex emotional model
   - Interactive emotion mapping
   - Quadrant-based emotional categorization

3. **Deep Agent Dashboard**
   - Real-time task monitoring
   - Agent thought processes
   - Progress tracking
   - TODO list management

## 🛠 Technology Stack

- **Frontend**: Next.js 15 with TypeScript
- **UI Framework**: Tailwind CSS
- **AI Integration**: CopilotKit/AG UI
- **Visualizations**: Plotly.js with React
- **Backend**: FastAPI (Python)
- **Agent Framework**: LangGraph
- **Database**: Neo4j (for psychological knowledge graph)

## 📦 Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- Neo4j database (for psychological data)

### Frontend Setup
```bash
cd sentiment-ag-ui
npm install
npm run dev
```

### Backend Setup
```bash
# From the main project directory
python ag_ui_backend.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file in the sentiment-ag-ui directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_COPILOT_API_KEY=ck_pub_c92308bc3efb7424c203f6ab05c0fb4a
```

### Backend Configuration
The FastAPI backend connects to your existing SentimentSuite infrastructure:
- Neo4j database for psychological data
- LangGraph agents for analysis
- Hybrid RAG tools for data retrieval

## 🎯 Usage

### Basic Chat Interaction
1. Open the application at `http://localhost:3000`
2. Use the chat sidebar to interact with the AI assistant
3. Try suggested prompts or ask custom questions about psychological analysis

### Visualization Commands
- **"Show me emotional patterns"** - Creates emotion visualizations
- **"Generate personality summary"** - Creates Big Five radar chart
- **"Create circumplex plot"** - Shows Russell's Circumplex model
- **"Run deep analysis"** - Activates deep agent workflow

### Advanced Features
- **Real-time Updates**: Visualizations update as new data is analyzed
- **Interactive Charts**: Click and hover for detailed information
- **Agent Monitoring**: Watch AI agents work in real-time
- **Multi-modal Analysis**: Combine text, emotional, and statistical insights
