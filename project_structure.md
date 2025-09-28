---
PROJECT_DIR/
├─ SentimentSuite.py # this is the main file
├─ src/
│  ├─ voice_service_faster.py # This is the file 'faster-whisper' implementation of TTS that is currently used.
│  ├─ graphs/
│  │  ├─ framework_analysis.py # **Used for the 'psychological-results' workflow from sentiment_suite.py**
│  │  ├─ create_kg.py # Workflow for creating cypher for graph and embeddings (for Hybrid Graph-RAG)
│  │  ├─ chat_agent.py # The langgraph chatbot agent
│  │  ├─ __init.py__
│  ├─ __init.py__
│  ├─ analysis/ # These files are from the simple sentiment workflow in sentiment_suite.py, they instead use a well know 'Carl and Gloria' therapy transcription from a videa from the 1970's (i think)
│  ├─ circumplex_plot.py # Just for the circular 'Russell's Circumplex' visualization
│  ├─ emotion_mapping.py # For the 23 emotions to add to circumplex
│  ├─ enhanced visualization.py # Just front end dashboard stuff
│  ├─ sentiment_dashboard_tabs.py # the code for the tabbed dashboard
│  ├─ prompts/
│  │  ├─ __init.py__
│  │  ├─ text_prompts.py # the prompts.
│  ├─ utils/
│  │  ├─ __init.py__
│  │  ├─ io_py/
│  │  │ ├─edge/
│  │  │ │  ├─config.py # config file for voice chat.
│  ├─ utils/
│  │  ├─ __init.py__
│  │  ├─ text_graph_tools.py # This has the tool used in 'create_kg', the tool is 'write_cypher'.
├─ output/
│  ├─ psychological_analysis/ 
│  │  ├─ psychological_analysis_master.txt # This is where framework_analysis outputs 'to', where 'create_kg' outputs from'
│  │  ├─ graph_output/ # This is where 'create_kg' will output 'to'
│  ├─ server/
│  │  ├─ client_vad.js # This is the the VAD client
│  │  ├─ vad-worklet.js # This is the VAD functionality
│  ├─ ui/
│  │  ├─ langgraph_chat.py # The gradio front end for the actual chatbot
│  ├─ utils/
│  │  ├─ hybrid_rag_tools.py # The hybrid rag tools for workflow 4. Not really needed for this
├─ run_notes/
---
