

---
PROJECT_DIR/
├─ SentimentSuite.py # this is the main file
├─ src/
│  ├─ voice_service_faster.py # This is the file 'faster-whisper' implementation of TTS that is currently used.
│  ├─ graphs/
│  │  ├─ framework_analysis.py # **Used for the 'psychological-results' workflow from sentiment_suite.py**
│  │  ├─ create_kg.py # Workflow for creating cypher for graph and embeddings (for Hybrid Graph-RAG)
│  │  ├─ chat_agent.py # The langgraph chatbot agent, to be updated with 'AG_UI'. LARGE FILE.
│  │  ├─ deep_agent.py # My code for the langgraph Deep Agent for the terminal for the final 'terminal admin assistant' workflow.
│  │  ├─ __init.py__
│  ├─ __init.py__
│  ├─ analysis/ # These files are from the simple sentiment workflow in sentiment_suite.py, they instead use a well know 'Carl and Gloria' therapy transcription from a videa from the 1970's (i think)
│  ├─ circumplex_plot.py # Just for the circular 'Russell's Circumplex' visualization
│  ├─ emotion_mapping.py # For the 23 emotions to add to circumplex
│  ├─ enhanced visualization.py # Just front end dashboard stuff
│  ├─ sentiment_dashboard_tabs.py # the code for the tabbed dashboard
│  ├─ prompts/
│  │  ├─ __init.py__
│  │  ├─ text_prompts.py # the prompts for the 'framework_analysis', 'create_kg' and 'chat_agent' workflows
│  │  ├─ deep_prompts.py # the prompts, heavily adapted from Deep Agents. LARGE FILE.
│  ├─ utils/
│  │  ├─ __init.py__
│  │  ├─ io_py/
│  │  │ ├─edge/
│  │  │ │  ├─config.py # config file for all models.
│  ├─ agent_utils/
│  │  ├─ deep_utils.py # **'Deep Agents' code** 
│  │  ├─ state.py # **'Deep Agents' code** 
│  ├─ tools/
│  │  ├─ __init.py__
│  │  ├─ text_graph_tools.py # This has the tool used in 'create_kg' and 'framework_analysis' workflows
│  │  ├─ hybrid_rag_tools.py # The hybrid rag tools for both the Chat Agent and Deep Agent('Admin Assist'). Need to add the graph queries for 'deep_agent'
│  │  ├─ file_tools.py # **'Deep Agents' code** 
│  │  ├─ task_tool.py # **'Deep Agents' code**
│  │  ├─ todo_tools.py # **'Deep Agents' code** 
│  │  ├─ research_tools.py # **'Deep Agents' code**: for web search, graph search is in 'hybrid_rag_tools.py' 
│  ├─ terminal/
│  │  ├─ **admin_assistant.py** - my unfinished attempt at converting my previous terminal helper. To be used as UI for 'Deep Agent'.
├─ output/
│  ├─ psychological_analysis/ 
│  │  ├─ psychological_analysis_master.txt # This is where framework_analysis outputs 'to', where 'create_kg' outputs from'. HUGE FILE.
│  │  ├─ graph_output/
│  │  │ │  ├─psychological_graph_20250916.cypher # 'create_kg' output file. HUGE FILE.
│  │  ├─ workflow_1_output_examples.txt/ # Example output from 'framework_analysis'.
│  │  ├─ workflow_2_output_examples.txt/ # Example output from 'create_kg'.
│  ├─ ui/
│  │  ├─ langgraph_chat.py # The gradio front end for the actual chatbot. LARGE FILE.
├─ run_notes/
---
