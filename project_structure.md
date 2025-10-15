

---

### Models
> GPU = 24GB VRAM
> GPU-Mini-itx = 12GB VRAM
Main Mode - Architect='gpt-oss:20b' (on main PC): 14GB VRAM.
Articulate Task Model - Scribe='gpt-oss:20b' (on mini-itx pc)
Alternative Models (For 'best of n') - Alt='Randomblock1/nemotron-nano' (on main pc): 4.9GB VRAM
```
<PROJECT_DIR>
├─ **SentimentSuite.py # the app front end (not used for the terminal based workflow).**
├─ sentiment-ag-ui # the seperate React app front end (not used for the terminal based workflow, is similar to sentiment_suite.py except uses copilotkit and AG_UI).
│  ├─ run_deep_agent_e2b.py # langgraph Deep Agent for the terminal workflow.
├─ src/
│  ├─ voice_service_faster.py # This is the file 'faster-whisper' implementation of TTS used with chat_agent.
│  ├─ graphs/
│  │  ├─ framework_analysis.py # **Workflow 1 - Used for the 'psychological-results' from sentiment_suite.py**.
│  │  ├─ create_kg.py # Workflow 2 - for creating cypher for graph and embeddings (for Hybrid Graph-RAG).
│  │  ├─ deep_agent.py # Workflow 4 - The Deep Agent base workflow
│  │  ├─ chat_agent.py # workflow 3 The langgraph chatbot agent, to be updated at some point with 'AG_UI': LARGE FILE.
│  ├─ analysis/ # files from simple sentiment workflow (in sentiment_suite.py), they instead use a well known 'Carl and Gloria' therapy transcription.
│  │  ├─ circumplex_plot.py # Just for the circular 'Russell's Circumplex' visualization.
│  │  ├─ emotion_mapping.py # For the 23 emotions to add to circumplex.
│  │  ├─ enhanced visualization.py # Just front end dashboard stuff.
│  │  ├─ sentiment_dashboard_tabs.py # the code for the tabbed dashboard.
│  ├─ prompts/
│  │  ├─ e2b_prompts.py # the prompts, heavily adapted from Deep Agents: LARGE FILE.
│  │  ├─ text_prompts.py # the prompts for workflows 1-3.
│  ├─ utils/
│  │  ├─ io_py/
│  │  │ ├─edge/
│  │  │ │  ├─**config.py # config file for all models**.
│  │  │ │  ├─ssh_tunnel.py # ssh tunnel to allow for models on other PC's on my network
│  ├─ agent_utils/
│  │  ├─ deep_utils.py #'Deep Agents' code for formatting langgraph messages .
│  │  ├─ state.py # 'Deep Agents' for state handling with todo's etc .
│  ├─ tools/
│  │  ├─ text_graph_tools.py # This has the tool used in 'create_kg' and 'framework_analysis' workflows.
│  │  ├─ e2b_tools.py # Replaces'Deep Agents' virtual filesystem instead using e2b kernel.
│  │  ├─ task_tool.py # basic 'Deep Agents' code for creating a sub-agent.
│  │  ├─ todo_tools.py # basic 'Deep Agents' code for todo lists. 
│  │  ├─ research_tools.py # customized deep agent tools for for web search and pubmed search.
│  │  ├─ hybrid_rag_tools.py # Hybrid Graph-RAG tools for deep agent and chat agent workflows.
│  │  ├─ file_tools.py # Adapted from Deep Agents. File handling utilities for reading, writing, and deleting files within the project structure.
│  ├─ terminal/
│  │  ├─ admin_assistant.py - my unfinished attempt at converting my previous terminal helper. To be used as UI for 'Deep Agent'.
├─ output/
│  ├─ psychological_analysis/
│  │  ├─ psychological_analysis_master.txt # This is where framework_analysis outputs 'to', where 'create_kg' outputs from': HUGE FILE.
│  │  ├─ graph_output/
│  │  │ │  ├─psychological_graph_20250916.cypher # 'create_kg' output file: HUGE FILE.
│  │  ├─ workflow_1_output_examples.txt/ # Example output from 'framework_analysis'.
│  │  ├─ workflow_2_output_examples.txt/ # Example output from 'create_kg'.
│  ├─ ui/
│  │  ├─ langgraph_chat.py # The gradio front end for the actual chatbot: LARGE FILE.
│  ├─ ui/
│  │  ├─ utils/
│  │  │ │  ├─context_manager.py # Context window manager to remove older messages from langgraph messagesstate
│  │  │ │  ├─embeddings.py # embeddings utils
├─ run_notes/
│  ├─ data/
│  │  ├─ psychological_analysis_master.txt # This is where framework_analysis outputs 'to', where 'create_kg' outputs from'. HUGE FILE.
│  │  ├─ knowledge_corpus/
│  │  │ │  ├─how_to_write_progress_notes.md # research on 'Progress Notes' since I'm not an _actual_ psychologist despite being knowledgable.
│  │  │ │  ├─soap_notes_and_examples.md # research on 'Progress Notes' since I'm not an _actual_ psychologist despite being knowledgable.
│  │  ├─ therapy_csvs/
│  │  │ │  ├─therapy-fin.csv
│  │  │ │  ├─therapy-fin_fixed.csv
```