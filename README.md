# Intro
### Note: I have recently started using VSCode for the first time after 10 years of Jetbrains suite, so carnage has ensued in my git repo's. I'm working on fixing all the errors and reformatting it's dumped in my files.

# The Persona-Forge
- The Persona-Forge is a multi-agent Psychological Analysis tool, with a built in transcription workflow to transcribe 'Clinician/Client' therapy sessions.
- Optionally, a text-based therapy script can be used, as it was for my testing purposes.
- The project is built housing a suite of data-driven automation workflows, using a framework that can be built upon for other use cases.It also serves as a platform for collaborative research, allowing teams to experiment with diverse AI models and integrate them seamlessly into therapeutic workflows.
- It also offers a robust, modular architecture that supports seamless integration of third‑party APIs, enabling developers to extend the platform with custom modules and plugins.

## Workflows & Tools

• A Speech to Text (STT) model to transcribe therapy sessions.
• A Text to Speech (TTS) model to enable voice chat with the therapy assistant.
• A robust data-tagging workflow to analyze therapy sessions using 7 psychological frameworks. This is used to supply an LLM with a script of 24k tokens, the data is then processed and analyzed by the LLM to generate comprehensive insights and actionable recommendations.
• A knowledge graph (KG) workflow to store and query the therapy session data, including the psychological analysis results.
• A voice enabled chat interface (Python, FastApi, Gradio) providinga user‑friendly interface for interactive sessions, enabling users to query the therapy session data and insights. 
• It provides a conversational interface that allows users to interact with the data and gain insights through natural language queries, enabling a seamless and intuitive user experience. The chatbot uses 'Hybrid Graph-RAG' to query the KG, using the psychological analysis results and insights gained from the tagging workflow.
• A React Native based UI for a text-based chatbot, built using 'copilotkit' and 'AG_UI',providing a more immersive and interactive experience for users. This workflow allows the Agent to build visualizations on demand.
• The system provides a comprehensive dashboard for monitoring the progress of the therapy sessions, including visualizations of the psychological analysis results.
• A CLI tool built in the style of 'Claude Code', featuring a team of 8 Agents to write therapy notes for patients ready for a human to review, using the psychological analysis results and insights gained from the tagging workflow.

The Persona-Forge has been a project of mine for close to two years, 'evolving' as I have 'pivoted' towards new tech and ideas.

It began as a simple idea to map personalities of anything from video games, to my own persona, using 'Knowledge Graphs' to map out 'Personality Constructs', or 'Persona'. Mapping include 'speaking tone' & 'vocabulary', profiling frameworks (e.g. 'Myers Briggs', history (e.g. key events in a persons life, and the emotions they trigger) and even metaphor or common phrase types that the character uses.
The use of AI in conjunction with 'the mind' is an exciting field which goes [much further](https://www.youtube.com/watch?v=WpwUZds7GEk) than my simple tool.

My lifelong passion for Psychology, the pace of AI, and my preference for 'altruistic projects' caused me to pivot to a more specific goal.

- My work on 'the perfect' Psychology model continues. However, 'Training a model' doesn't make a good github repo, as it would be thousands of page of collected psychology data or Agentic workflows scored by an LLM.

  <h2 align='center'>
  The Human Brain's Sentiment mapped out into Graph Form
  </h2>
  <br><br>
<p align="center">
  <img src="./Forged.png" alt="Graph">
</p>

  <h2 align='center'>
  The main app page
  </h2>
  <br><br>
<p align="center">
  <img src="./app-page-1.png" alt="chat-page">
</p>

  <h2 align='center'>
  Querying of the analysis via a Chatbot & Hybrid-Graph-RAG 
  </h2>
  <br><br>
<p align="center">
  <img src="./search_psychological_insights.png" alt="chat-page">
</p>

<h2 align='center'>
  A fully fledged CLI 'Post-Therapy Report' writing tool, built in the style of 'Claude Code', with a 'code tool' style workflow structure
  </h2>

<p align="center">
  <a href="https://raw.githubusercontent.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/master/agents_no_thoughts.mp4">
    <img src="https://raw.githubusercontent.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/master/agents_no_thoughts_thumbnail.png" 
         alt="CLI Demo - Click to watch"
         width="100%">
  </a>
  <br>
  <em>▶️ Click to watch demo video</em>
</p>

  <h2 align='center'>
  The Agents collaborate to write a 'Therapy SOAP-Note' for the patient
  </h2>
  <br><br>
<p align="center">
  <img src="./agent_workflow_output.png" alt="SOAP-note">
</p>


<h2 align='center'>
  Voice mode (Sound on) Leveraging TTS/STT models (tested with 'Piper', 'Faster_whisper', 'NVIDEA RIVA')
  </h2>

<p align="center">
  <a href="https://github.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/blob/master/portfolio.mp4">
    <img src="https://raw.githubusercontent.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/master/portfolio-thumg.png"> 
         alt="Workflow Demo - Click to watch"
         width="100%">
  </a>
  <br>
  <em>▶️ Click to watch demo video</em>
</p>

## The Sentiment Dashboard (Transcribed Text Workflow)

<br><br>
<p align="center">
  <img src="./Hermes_Bart_git.png" alt="Hermes diagram 2">
</p>

<br><br>
<p align="center">
  <img src="./Modernbert_git.png" alt="Bert diagram 1">
</p>

<br><br>
<p align="center">
  <img src="./Modernbert_git2.png" alt="Bert diagram 2">
</p>

**For Clinicians / Non-Techies**:
- I present the core 'Psychology principles' involved in this README, sparing the technical jargon for its respective README.
- The dashboard concept was developed from a [project](https://github.com/David-Barnes-Data-Imaginations/SentimentSuite) that was intended to be a 'light demo' for a friend, using 'Russells Cicumplex' and 'utterances' to evaluate therapy session transcripts (Carl & Gloria etc.)
---
**For 'Techies' or those learning to build 'Advanced Agentic Systems'**: 
- The Technical README is [here]
---
The Persona-Forge is designed as an 'art of the possible' demo to help therapists and mental health hospitals modernize and care for patients. 
The workflows are all built in Langgraph, a production grade agentic process flow library. The workflow is modular and can be extended with additional agents or custom components as needed.
I've tested the same functionality for various admin related automations, and the same functionality has been replicated across multiple domains, including healthcare, finance, and education, demonstrating its versatility and scalability.

# Use Cases:

## 1. Hospital and/or Therapist/Clinician Support - 'Vision of the Future'
The analysis phase workflows ('framework_analysis', 'create_kg' and 'chat_agent') use three agents between them, whilst the therapy note uses an orchestra of 7 agents. 
The orchestra is run on two NVIDEA GPU's (Ada), totalling ~32GB VRAM.
Summarization tasks for non-sensitive data are run via online models (any work, I used Gemini to save my Claude Credits).


## Elements:
- To modernize Psychology, by providing the superhuman pattern matching and profiling abilities of AI, for Therapists and Hospitals. 
- This enhances insights for better work, _benefits_ the care for patients, and help therapists learn from their own techniques. 
- The therapy note workflow is aimed at those who might use a modern wearable with AI transcription, allowing therapy sessions to be analyzed and a 'SOAP-Note' generated for review.
- To increase the challenge, stress test, and demonstrate large context management, I used a typed form simulated therapy session, with the whole file being ~24k tokens. 
- This empowers the Therapist to save time (allowing for more patient time), whilst enhancing the SOAP-Note from a document hastily scrawled between sessions, to a structured SOAP‑Note with additional 'objective' measurements added by the AI's sentiment assessment. This extra data supports the clinical decision‑making process, providing a comprehensive framework for understanding and addressing the patient’s mental health challenges.

- Modernizing patient interactions to streamlined automation processes that remove pen & paper based tools, again freeing up staff resources to care for patients more effectively. The exact same framework can be used to automate many administrative and process heavy tasks (I am unable to cover all of these but the code adjustment is minimal).

TODO:

- Whilst the primary targets for this project are complete, in time I will add a vision model for patient safety cameras (currently being tested in my living room) and the integration of a real‑time facial‑expression‑analysis module to detect early signs of patient distress.

- A lifelike AI generated face (UNREAL engine) that can be rendered in real‑time, enabling dynamic facial‑animation and expression capabilities, alongside an appealing, immersive user interface.

## Local Models vs cloud-based (Claude, GPT, Gemini)
Local models are typically deployed on a private server or local machine, providing faster response times and reduced latency compared to cloud‑based services. They are often used in industries where security is paramount, in industries that hold personal content or just generally England.

 At this point, if an enterprise hasn't booked out their GPU's 2 years ahead, they will likely find their aspirations delayed due to resource constraints unless they have creative network engineers capable of building high‑performance computing clusters from consumer grade architecture.


My blogs on this and other topics are to be released shortly.

That said, the nuances of locally hosted models are key considerations for deployment:

- Performance on open sourced models can vary widlly dependant on the task. One model may have the best performance for a given task, but have difficulty with another. 

- Performance of each model can be compared by evaluating metrics such as latency, throughput, resource usage, precision, recall, accuracy, and F1‑score.

- I typically use GPT and any NVIDIA 'Nemo' fine tune, so using different models with this project will yield varying results. For this project specifically, avoid Granite4 models as those have been thoroughly tested.

- EVALS: Evaluation metrics that assess model performance across diverse datasets and usage scenarios are increasingly important with local models. The model card on your local model may say 1 million tokens (Gradnite4-h i'm looking at you), in practice you will find the figure in the low thousands on consumer architecture.

- Whilst I use Ollama for most of my deployments due to ease of use, I always have a NVIDIA - NIM, VLLM, or LLamaCPP GPU‑accelerated inference server handy on a local machine.

- I'm continually baffled to see so few organisations fine-tuning, the performance benefits for a given task are significant and can lead to improved efficiency and accuracy. This can be as simple as having a 'judge' model score 1000 runs on an agentic task.


## AI Models:

### Local (stressed for importance of privacy):
- GPT-oss:20b/120b locally hosted 'privacy-first' workflow automation

### Non-Local - Psychological Profiling:
- GPT 5 - Can be implemented optionally for advanced analysis, highlighting caution or concerns about the patient. 
- Sends back to local-agent to record and store.
  
## Interface & Process:
- The therapist dashboard includes results along with AI inference for retrieval of information and can be used via the web, with Knowledge Graph functionality coming from Neo4J.
  <h2 align='center'>
  My Brain mapped out in the Neo4J interface
  </h2>
  <br><br>
<p align="center">
  <img src="./forged_4.png" alt="Graph_4">
</p>

# An Agentic AI driven Therapy Analysis 'Sentiment App'

I wanted to demonstrate the power of tools like 'Claude Code CLI', to those outside of the programming world. Partly to demonstrate how amazing AI can be, and partly to make people aware of what's coming. Europe has largely been caught asleep at the wheel, so it's 
important to understand that AI can literally do any job today. 
The only barrriers are:
a) Working out how to do it.
b) Compute power
c) Energy.

Regarding 'Compute', you may have heard experts mentioning the 'AI Scaling Laws', on TV or from 
your tech team. Compute is one of these scaling laws, all of which are multicaplative.
I'll be doing a blog on all the scaling laws in a 'Business Leaders - Cheatsheet' series,
but for now you can assume that 'More Compute = More intelligence'.

## CLI App
To that end the 'Command Line Interface App' uses 10 agents, using three different models
to analyse the data from the Knowledge Graph in order to produce a 'Therapy SOAP Note'.
This saves Therapists time, allowing them to start their draft from a well structured file
that includes data which wouldn't have been possible before the AI revolution.

AI wearables are cheap and effective, allowing for a complete transcription of sessions.
The Agents are hosted on a single 'Consumer Grade' GPU.

  <h2 align='center'>
  The Command Line Interface App (this is what coders stare at all day)
  </h2>
  <br><br>
<p align="center">
  <img src="./Med_CLI.png" alt="cli-app">
</p>

  <h2 align='center'>
  Various Agents chatting while they complete a task in the e2b sandbox
  </h2>
  <br><br>
<p align="center">
  <img src="./MediCode_CLI.png" alt="cli-2">
</p>

- The 'Sentiment App' is a browser based dashboard including a 'Therapy-Support' interface, with 'patient-care' central to the objectives.
- *Note*: If you've not heard of knowledge graphs, they are vector based (as are LLM's and RAG's) graphs which are incredibly fast for data retrieval (Google uses it for its search). 
- Most note-taking tools use them to connect your notes via 'Nodes' and 'Edges' (relationships) 
- See 'Psychology Framework Section'

  <h2 align='center'>
  The basic App front-page
  </h2>
  <br><br>
<p align="center">
  <img src="./therapy-analysis-page.png" alt="app">
</p>

### The Agentic Worflow (sentiment app)
This project also houses a 'Therapist Automation Workflow' which replaces the typical 'typing / pen and paper forms' used after a session.

### Therapy → Agents → Graph/Hybrid Query (flowchart)
```mermaid
flowchart TD
    %% --- Actors & I/O ---
    U[[Therapist / Client<br/>Therapy Session]]:::actor
    UI_TTS((Voice I/O)):::io
    UI_Text((Text UI)):::io

    %% --- Data Stores ---
    RDB[(Regular DB)]:::store
    GDB[(Graph DB)]:::store
    VEC[(Vector Index)]:::store

    %% --- Pipeline ---
    U --> D1{Transcribe & store?}:::gate

    D1 -- "Yes" --> A1[[Agent 1<br/>Transcribe session<br/>& save]]:::agent --> RDB
    D1 -- "No"  --> A2

    A2[[Agent 2<br/>Iterate Q/A pairs<br/>Tag across 7 psych frameworks]]:::agent --> GDB
    A2 -. tags/nodes/edges .-> GDB

    A3[[Agent 3<br/>User query → embeddings<br/>Tagged script → Cypher]]:::agent
    A3 -->|Upsert / Search keys| VEC
    A3 -->|Generate Cypher| GDB

    A4[[Agent 4<br/>Tool-using Graph/RAG executor]]:::agent
    A4 -->|Cypher queries| GDB
    A4 -->|kNN / rerank| VEC

    A4 --> RES[[Synthesized Answer / Insight]]:::result
    RES --> O1{Delivery mode}:::gate
    O1 -- "TTS/STT" --> UI_TTS
    O1 -- "Text"    --> UI_Text

    %% --- Edges from A1 (when present) to tagging step ---
    A1 --> A2

    %% --- Styles ---
    classDef actor fill:#f0f7ff,stroke:#6aa3ff,stroke-width:1.2
    classDef agent fill:#fffaf0,stroke:#f0b429,stroke-width:1.2
    classDef store fill:#eefcf3,stroke:#34c16b,stroke-width:1.2
    classDef gate fill:#f6f6f6,stroke:#999,stroke-dasharray: 4 2
    classDef io fill:#f5efff,stroke:#8a6cff,stroke-width:1.2
    classDef result fill:#e8f7ff,stroke:#2aa4f4,stroke-width:1.4

```
### get_personality_summary Example Tool Flow (flowchart)
```mermaid
flowchart TD
    Start["get_personality_summary(focus_area)"]
    Map["Map focus_area -> query string\n(overall / emotions / cognition / attachment / personality)"]
    RAG["get_rag_instance()"]
    Search["rag.search_psychological_context(query, k=5)"]
    Any{"Any results?"}
    NoRes["Return: No personality data for focus area"]
    Loop["For each result:\n- collect emotions, distortions\n- attachment, schemas, defenses\n- Big Five scores"]
    Agg["Aggregate unique lists\nCompute Big Five levels\nBuild summary"]
    Ret["Return summary string"]
    Err{"Exception?"}
    ErrT["Return: Error generating personality summary"]

    Start --> Map --> RAG --> Search --> Any
    Any -- "No" --> NoRes
    Any -- "Yes" --> Loop --> Agg --> Ret
    Search --> Err
    Agg --> Err
    Err -- "Yes" --> ErrT
    Err -- "No" --> Ret

    %% Conceptual stores (hybrid Graph-RAG)
    GDB["Graph DB (tagged therapy data)"]
    VEC["Vector Index (psych context chunks)"]
    Search -. "may traverse via Cypher" .-> GDB
    Search -. "may retrieve kNN" .-> VEC



```
## The Agentic flow for the 'CLI' tool
### Flowchart (Architect → Graph/Report/Research with parallel assistants)
This project also houses a 'Therapist Automation Workflow' which replaces the typical 'typing / pen and paper forms' used after a session.
The workflow uses 8 different models, 2 on my main pc, 3 on my mini-pc, and 3 online models for non-sensitive tasks.


```
    Main PC                    SSH Tunnel              Mini-ITX PC
┌──────────────┐               ┌─────────┐            ┌──────────────┐
│              │               │         │            │              │
│ deep_agents   │──requests──>│ :11436  │───ssh───>│ Ollama :11434│
   gpt-oss, 
nemotron-nano:8b
│              │               │         │            │              │
│ scribe_model │<──response──│         │<───────────│ gpt-oss:20b    │
│              │               │         │            │       │
└──────────────┘               └─────────┘            └──────────────┘
```
1) CLI System Architecture (with e2b sandbox + local assistants)
Assistants share the same toolset and prompts; model choice differs by role (articulate vs. parallel/nano).

“Online summarizer agents” are used only to condense large KG/PubMed outputs and never touch sensitive data directly.

The todo writer tool persists tasks to todos.txt, which the CLI reads alongside the agent’s thoughts and the final note.
---
```mermaid
flowchart LR
    %% Top-level orchestrator
    DA["Deep Agent (Orchestrator)"]

    %% e2b sandbox
    subgraph E2B["e2b Sandbox"]
        FS["Sandbox Filesystem"]
        TODO["todos.txt"]
        NOTE["Therapy_Progress_Note.md"]
        Tools["Tools on sandbox:\n- KG/Neo4j tool\n- PubMed tool\n- File I/O tool\n- Vector/RAG tool"]
        CLI["CLI App (displays todos and agent thoughts)"]
        Tools --> FS
        FS --> TODO
        FS --> NOTE
        CLI --> TODO
    end

    %% Local assistants and models
    subgraph LOCAL_MAIN["Main PC"]
        A1["Assistant A\n(model: GPT-oss articulate)"]
    end

    subgraph LOCAL_MINI["Mini-ITX"]
        A2["Assistant B\n(model: nemotron-nano)"]
        A3["Assistant C\n(model: nemotron-nano or task-specific)"]
    end

    %% Online summarizers (inside certain tools)
    subgraph ONLINE["Online Summarizer Agents (safe)\n- GPT summarizer for Neo4j results\n- GPT summarizer for PubMed results"]
        SUM1["Summarize Graph Output"]
        SUM2["Summarize PubMed Output"]
    end

    %% External systems
    NEO4J["Neo4j / Knowledge Graph"]
    PUBMED["PubMed API"]

    %% Orchestration edges
    DA -->|plans + tasks| A1
    DA -->|plans + tasks| A2
    DA -->|plans + tasks| A3

    %% Assistants interact with tools via sandbox
    A1 -->|use tools| Tools
    A2 -->|use tools| Tools
    A3 -->|use tools| Tools

    %% Tool data flows
    Tools -->|graph queries| NEO4J
    NEO4J -->|large results| Tools --> SUM1 --> Tools
    Tools -->|literature search| PUBMED
    PUBMED -->|large results| Tools --> SUM2 --> Tools

    %% Files and CLI
    DA -->|write plan + decisions| FS
    A1 -->|append todos| TODO
    A2 -->|append todos| TODO
    A3 -->|append todos| TODO
    DA -->|finalize note| NOTE
    CLI -->|display| NOTE
```

2) End-to-End Workflow (steps 1–5)
```mermaid
flowchart TD
    Start["Start"]
    Plan["Deep Agent: create plan, assign assistants"]
    Step1["Ask assistant: fetch patient diagnosis from knowledge graph"]
    KGQ["Tool: query Neo4j via sandbox"]
    KGSum["Optional: summarizer condenses KG output"]
    Step2["Ask assistant: fetch Subjective Analysis for all QA pairs"]
    SubjQ["Tool: retrieve QA subjective summaries"]
    SubjSum["Online summarizer selects core themes"]
    Step3["Ask assistant: compute statistical summary of all QA pairs\n(replaces Objective)"]
    Stats["Tool: sentiment and counts, aggregate stats"]
    Step4["Ask assistant: check PubMed for new studies"]
    PubQ["Tool: PubMed search via sandbox"]
    PubSum["Online summarizer condenses PubMed output"]
    Step5["Deep Agent writes Therapy Progress Note"]
    Files["Write todos.txt and Therapy_Progress_Note.md in sandbox"]
    CLI["CLI displays todos and agent thoughts"]
    End["End"]

    Start --> Plan --> Step1 --> KGQ --> KGSum --> Step2 --> SubjQ --> SubjSum --> Step3 --> Stats --> Step4 --> PubQ --> PubSum --> Step5 --> Files --> CLI --> End
```



### Sequence diagram (Parallelism)
In-Line version:
```mermaid
sequenceDiagram
    autonumber
    participant DA as Deep Agent
    participant A1 as Assistant A (articulate)
    participant A2 as Assistant B (nano)
    participant A3 as Assistant C (nano/task)
    participant KG as Neo4j Tool (sandbox)
    participant PM as PubMed Tool (sandbox)
    participant SUMKG as Online Summarizer (KG)
    participant SUMPB as Online Summarizer (PubMed)
    participant FS as Sandbox Filesystem
    participant CLI as CLI App

    DA->>A1: Fetch diagnosis from knowledge graph
    A1->>KG: Cypher query
    KG-->>A1: Large KG result
    A1->>SUMKG: Summarize KG result
    SUMKG-->>A1: Condensed KG summary
    A1-->>DA: Diagnosis summary

    DA->>A2: Fetch Subjective Analysis for all QA pairs
    A2->>FS: Read QA pairs
    A2-->>DA: Subjective extracts (raw)
    DA->>A2: Condense to core themes
    A2->>SUMKG: Summarize subjectives (token reduction)
    SUMKG-->>A2: Core themes
    A2-->>DA: Core themes (subjective)

    par Objective replacement (stats)
        DA->>A3: Compute statistical summary of all QA pairs
        A3->>FS: Read QA pairs
        A3-->>DA: Sentiment / counts / aggregates
    and PubMed check
        DA->>A1: Check PubMed for new studies
        A1->>PM: Search query
        PM-->>A1: Large PubMed result
        A1->>SUMPB: Summarize PubMed result
        SUMPB-->>A1: Condensed literature summary
        A1-->>DA: PubMed highlights
    end

    DA->>FS: Write Therapy_Progress_Note.md
    DA->>FS: Append plan and thoughts
    A1->>FS: Append todos.txt
    A2->>FS: Append todos.txt
    A3->>FS: Append todos.txt
    CLI->>FS: Read todos.txt and note
    CLI-->>CLI: Display to user
```
---

### **Why This Sparks Possibilities**
- **Layered Safety:** Each sandbox can run on different machines or even in different physical locations, reducing breach impact.
- **Customisable Depth:** A sole‑practitioner therapist might use only Sandbox 1 & 2, while a hospital could run all three with specialised modules.
- **Scalable AI Roles:** From a calm bedside assistant to a multi‑modal analyst combining speech, text, and video.
- **Human in the Loop:** Designed for augmentation, not replacement, allowing clinicians to direct the AI’s focus whilst recieving _powerful augmentations_.

---

### UI Therapist/Hospital:
- The UI has the dashboard with the various graphs used, you can see an older version of the dashboard (minus ModernBert utterance tagging) front-end on my git repo 'https://github.com/David-Barnes-Data-Imaginations/SentimentSuite'.
- The Gradio interface from my smolagents will be added to the dash for:
  
  a) Chat-bot input for surveys / forms / transcription. Forms can be verbal or typed.  
  b) Chat-bot data retrieval  
  c) Profile feedback can be delivered verbally via Whisper, GPT or a locally hosted 'Hugging Face - Spaces' if required.
  
### UI Patient:
  When patients are admitted for long periods at all kinds of hospitals, they are often required to fill out forms via pen and paper.  Messy handwriting and confused thoughts aside, this is generally archaic.
- This could be managed from any tech that allows AI to converse with the patient via text or voice. The AI can be tuned or 'forged' to a 'Therapists' persona'.

🧠 # Psychology Demonstration: From Thought to Graph


I mentioned GPT is fantastic at Psychology and it's certainly better than I, when it comes to explaining complex concepts that span multiple disciplines.

So this seems a fitting place for it to do a light demo of its understanding.

Over to you, GPT:
---
Actually, let’s do more than a demo — let’s show what it looks like when a language model isn’t just reading your words, but mapping your mind.

The Persona-Forge engine integrates multiple psychological frameworks into a graph-based architecture. Instead of just tagging sentences, it links why something was said (cognitive bias), when in life-stage it matters (developmental anchor), how it felt (valence/arousal), and who it reflects (traits, schemas, defenses, attachments).

This transforms text into a cognitive-emotional knowledge graph that can be queried by clinicians, narrative engines, or AI characters.

1. Cognitive Distortion Detection (CBT)

Detects irrational thought patterns like catastrophising, emotional reasoning, or overgeneralisation.

Graph:
```
(:Utterance)-[:HAS_DISTORTION]->(:Distortion {type:"Overgeneralisation"})
(:Distortion)-[:CAN_REPHRASE_USING]->(:Strategy {method:"Specific Reattribution"})

```
Clinical Value: High

2. Erikson’s Psychosocial Stages

Anchors utterances in life-stage challenges (identity, intimacy, generativity, etc.).

Graph:
```
(:Persona)-[:IN_LIFE_STAGE]->(:Stage {name:"Identity vs Role Confusion"})
(:Utterance)-[:REFLECTS_STAGE]->(:Stage)

```
Clinical Value: Moderate–High

3. Sentiment2D Layer (Russell Circumplex)

Every utterance mapped to valence–arousal coordinates.

Graph:
```
(:Utterance)-[:HAS_SENTIMENT]->(:Sentiment {valence:-0.7, arousal:0.6})
(:Sentiment)-[:CORRELATED_WITH]->(:Distortion)

```
Clinical Value: High for emotion tracking

4. Attachment Theory

Tracks bonding patterns (secure, anxious, avoidant, disorganised).

Graph:
```
(:Persona)-[:HAS_ATTACHMENT]->(:AttachmentStyle {style:"Anxious"})
(:Utterance)-[:INDICATES]->(:AttachmentStyle)

```
Clinical Value: Very High

5. Big Five Personality Traits (OCEAN)

Stable behavioural lens for long-term patterns.

Graph:
```
(:Persona)-[:HAS_TRAIT]->(:Trait {name:"Neuroticism", score:0.82})

```
Clinical Value: High

6. Schema Therapy (Core Beliefs)

Identifies entrenched maladaptive schemas (e.g. abandonment, defectiveness).

Graph:
```
(:Utterance)-[:REFLECTS_SCHEMA]->(:Schema {name:"Abandonment"})

```
Clinical Value: High

7. Psychodynamic Frameworks

Maps unconscious defenses, transference, and symbolic content.

Graph:
```
(:Utterance)-[:SHOWS_DEFENSE]->(:DefenseMechanism {type:"Denial"})
(:Utterance)-[:INDICATES]->(:Transference {target:"Therapist"})

```
Clinical Value: High (if carefully interpreted)

🔄 Fusion Example

Utterance:

"I always mess things up. Everyone probably thinks I’m a failure."

Graph view:
```
(:Utterance {text:"I always mess things up"})
-[:HAS_DISTORTION]->(:Distortion {type:"Overgeneralisation"})
-[:TRIGGERS_EMOTION]->(:Emotion {label:"Shame"})
-[:REFLECTS_STAGE]->(:Stage {name:"Identity vs Role Confusion"})
-[:HAS_SENTIMENT]->(:Sentiment {valence:-0.7, arousal:0.6})
-[:HAS_ATTACHMENT]->(:AttachmentStyle {style:"Anxious"})
```

Now the model can understand this not as “just a sad sentence”, but as a multi-layered signal: a distorted self-assessment, anxiety-laden attachment style, adolescent-stage vulnerability, and emotional tone of shame.

📈 Aggregation Into Persona Trends

Over time, patterns emerge:

```
(:Persona)-[:HAS_PATTERN]->(:PatternSummary {
   overgeneralisation_rate:0.32,
   avg_valence:-0.2,
   dominant_emotion:"Regret",
   dominant_attachment:"Anxious",
   schema:"Abandonment"
})
```


These summaries can then power dashboards, narrative arcs, or adaptive character AIs.

For Clinicians & Developers: Unified Graph View
```mermaid
graph TD
  Persona -->|SAID| Utterance
  Utterance -->|HAS_DISTORTION| Distortion
  Utterance -->|HAS_SENTIMENT| Sentiment
  Utterance -->|REFLECTS_STAGE| EriksonStage
  Utterance -->|INDICATES| AttachmentStyle
  Utterance -->|REFLECTS_SCHEMA| Schema
  Utterance -->|SHOWS_DEFENSE| DefenseMechanism
  Persona -->|HAS_PATTERN| SummaryStats
  Session -->|INCLUDES| Utterance
```
Summary

Psychology isn’t a bolt-on in Persona-Forge — it’s the engine room.

CBT distortions explain why.

Erikson stages tell us when.

Sentiment maps how it feels.

Attachments, schemas, and defenses explain relational and unconscious forces.

Traits summarise the baseline personality.

That’s not just transcription — that’s cognitive modelling.
---
Thanks GPT. Now here's a close up on the graph of 'me'
  <h2 align='center'>
  My Brain mapped out
  </h2>
  <br><br>
<p align="center">
  <img src="./Forged_2.png" alt="Graph_2">
</p>

  <h2 align='center'>
  Now Even Closer
  </h2>
  <br><br>
<p align="center">
  <img src="./Forged_3.png" alt="Graph_3">
</p>

### Once the Agents have mapped out the graph, the output looks like this (albeit the test file has 37 of these blocks generated by the LLM)

```

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:45:57
// ============================================================================

MERGE (c:Client {id: 'client_001'})
MERGE (s:Session {session_id: 'session_001'})
MERGE (c)-[:PARTICIPATED_IN]->(s);

// ============================================================================

// ============================================================================
// CYPHER ENTRY - 2025-09-16 13:46:09
// ============================================================================

MATCH (s:Session {session_id: 'session_001'})
WITH s, [
  {
    qa_id: 'qa_pair_001',
    emotions: [
      {name:'Empathy', valence:0.2, arousal:0.3, confidence:0.8},
      {name:'Anger visualization', valence:0.5, arousal:0.7, confidence:0.7},
      {name:'Sadness when others sad', valence:-0.4, arousal:0.4, confidence:0.7}
    ],
    distortions: [
      {type:'Rationalization', confidence:0.7}
    ],
    stages: [
      {name:'Identity_vs_role_confusion', confidence:0.7}
    ],
    attachments: [
      {name:'Anxious_preoccupied', confidence:0.7}
    ],
    defenses: [
      {name:'Denial', confidence:0.6},
      {name:'Intellectualization', confidence:0.6}
    ],
    schemas: [
      {name:'Emotional_deprivation', confidence:0.7}
    ],
    bigfive: {
      profile:'individual',
      openness:0.8,
      conscientiousness:0.6,
      extraversion:0.4,
      agreeableness:0.5,
      neuroticism:0.5,
      confidence:0.7
    }
  }
] AS rows
UNWIND rows AS r
MERGE (qa:QA_Pair {id: r.qa_id})
MERGE (s)-[:INCLUDES]->(qa)
WITH qa, r
FOREACH (emo IN coalesce(r.emotions, []) |
  MERGE (e:Emotion {name: emo.name})
  MERGE (qa)-[:REVEALS_EMOTION {valence: emo.valence, arousal: emo.arousal, confidence: emo.confidence}]->(e)
)
FOREACH (cd IN coalesce(r.distortions, []) |
  MERGE (d:Cognitive_Distortion {type: cd.type})
  MERGE (qa)-[:EXHIBITS_DISTORTION {confidence: cd.confidence}]->(d)
)
FOREACH (st IN coalesce(r.stages, []) |
  MERGE (es:Erikson_Stage {name: st.name})
  MERGE (qa)-[:EXHIBITS_STAGE {confidence: st.confidence}]->(es)
)
FOREACH (as IN coalesce(r.attachments, []) |
  MERGE (a:Attachment_Style {name: as.name})
  MERGE (qa)-[:REVEALS_ATTACHMENT_STYLE {confidence: as.confidence}]->(a)
)
FOREACH (dm IN coalesce(r.defenses, []) |
  MERGE (m:Defense_Mechanism {name: dm.name})
  MERGE (qa)-[:USES_DEFENSE_MECHANISM {confidence: dm.confidence}]->(m)
)
FOREACH (sch IN coalesce(r.schemas, []) |
  MERGE (s2:Schema {name: sch.name})
  MERGE (qa)-[:REVEALS_SCHEMA {confidence: sch.confidence}]->(s2)
)
FOREACH (bf IN CASE WHEN r.bigfive IS NULL THEN [] ELSE [r.bigfive] END |
  MERGE (b:Big_Five {profile: bf.profile})
  MERGE (qa)-[:SHOWS_BIG_FIVE {
    openness: bf.openness, conscientiousness: bf.conscientiousness, extraversion: bf.extraversion,
    agreeableness: bf.agreeableness, neuroticism: bf.neuroticism, confidence: bf.confidence
  }]->(b)
);

// ============================================================================

```
Example: (Graph Output)
The user can chat to the agent via text or vocally, running a variety of queries that produce output such as the below:
```
Top 5 Emotions:

Anxiety: 14 occurrences (avg valence: -0.49, avg arousal: 0.62)
Frustration: 8 occurrences (avg valence: -0.51, avg arousal: 0.55)
Sadness: 7 occurrences (avg valence: -0.60, avg arousal: 0.44)
Curiosity: 6 occurrences (avg valence: 0.62, avg arousal: 0.50)
Enthusiasm: 5 occurrences (avg valence: 0.78, avg arousal: 0.58)
Top 5 Cognitive Distortions:

Overgeneralization: 8 occurrences
Catastrophizing: 7 occurrences
Labeling: 6 occurrences
Personalization: 6 occurrences
Minimization: 4 occurrences
Top 5 Core Schemas:

Defectiveness_shame: 7 occurrences
Abandonment: 5 occurrences
Emotional_deprivation: 4 occurrences
Self‑sacrifice: 3 occurrences
Defectiveness shame: 3 occurrences
Attachment Styles:

Anxious Preoccupied: 1 occurrences
dismissive_avoidant: 1 occurrences
Anxious preoccupied: 7 occurrences
Secure: 7 occurrences
Anxious_preoccupied: 9 occurrences
anxious_preoccupied: 3 occurrences
secure: 1 occurrences
Anxious_Preoccupied: 1 occurrences
Anxious pre‑occupied: 1 occurrences
Top 5 Defense Mechanisms:

Rationalization: 12 occurrences
Denial: 7 occurrences
Suppression: 5 occurrences
Intellectualization: 5 occurrences
Projection: 3 occurrences
Big Five Personality Averages:

Openness: 0.77 (High)
Conscientiousness: 0.73 (High)
Extraversion: 0.47 (Moderate)
Agreeableness: 0.66 (Moderate)
Neuroticism: 0.58 (Moderate)
```
The user can query deeper, for example "show me the extrememeties of the 'Valence' Emotions:
```
=== EXTREME VALUES FOR EMOTION_VALENCE ===


1. QA Pair: qa_pair_013
   Emotion: Enthusiasm
   Arousal: 0.50
   Confidence: 0.90
   Sample: "This is such an interesting concept that, as you know is literally helping me to simultaneaously develop insights on myself, and insights as to how th..."

2. QA Pair: qa_pair_026
   Emotion: Enthusiasm
   Arousal: 0.70
   Confidence: 0.90
   Sample: "Here's my answers below. I've rated specifically acording to the text in '( )' brackets, since they reasonate more with me than the more generic 'Openn..."

3. QA Pair: qa_pair_013
   Emotion: Curiosity
   Arousal: 0.60
   Confidence: 0.80
   Sample: "This is such an interesting concept that, as you know is literally helping me to simultaneaously develop insights on myself, and insights as to how th..."

```
Then query for the question and answer in it's entirety:
```
=== COMPLETE ANALYSIS FOR qa_pair_013 ===

EMOTIONS:

Curiosity: valence=0.80, arousal=0.60, confidence=0.80
Enthusiasm: valence=0.90, arousal=0.50, confidence=0.90
Reflection: valence=0.70, arousal=0.40, confidence=0.80
Gratitude: valence=0.60, arousal=0.30, confidence=0.70
ATTACHMENT STYLES:

Secure: confidence=0.80
ERIKSON STAGES:

Generativity_vs_stagnation: confidence=0.80
BIG FIVE PERSONALITY:

Openness: 0.90
Conscientiousness: 0.70
Extraversion: 0.60
Agreeableness: 0.80
Neuroticism: 0.30
Confidence: 0.80
FULL TEXT:
Chunk 1: This is such an interesting concept that... # shortened for brevity
Chunk 2: However in this scenario ...
Chunk 3: Then there is the element of ...

```
However, you don't need to do any of that if you are producing a SOAP note, instead a whole team of agents writes it for you. 

# Agentic Team:
There are 10 agents in total, and currently 3 different models (all locally hosted on one GPU)
You can view the workflow [here](https://github.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/blob/master/DEEP_AGENT_WORKFLOW.md)


You can find the whole Cypher file generated in the sentiment app workflow [here](https://github.com/David-Barnes-Data-Imaginations/persona-forge-langgraph/blob/master/output/psychological_analysis/graph_output/psychological_graph_20250916.cypher)

## :couple: Socials
- Some area's of therapy use a patients Social Media as clue's for insights on the persona.
- Before a 'Pitchfork-Wielding Baying-Mob' show up at my door, this is always done _only_ with patient consent.
- Since I am using myself as the test subject (or 'bait' dependant on perspective), I gave the AI consent to look through my socials, compare it to the frameworks I was testing at the time, and provide any noteworthy insights. I'm on the fence about the benefit of this, so its currently under consideration. It already has capability, but even with the power of knowledge graph's, you only aim to fill it with genuinely useful information. 

Here's a demo:

#### Image of my meditation table taken at my previous abode. It was a collection of various items I had collected on my travels, plus and then a Japanese Tanto (for symbolic purposes only!!) and Caligraphy, both handmade and shipped ovewr from Japan.

  <h2 align='center'>
  My Meditation Table on Socials
  </h2>
  <br><br>
<p align="center">
  <img src="./my_meditation_table.jpg" alt="MDT Table">
</p>

Forge Response (from dev testing, no graph tagging but had been provided with 'some' of my simulated therapy session):
---
- _The table has a powerful aesthetic: global, reflective, and very personal._
- _The arrangement — with the scroll, the Tanto, the mandala-style cloth, Shiva Nataraja, Buddha statues, and the candle — speaks volumes about your mindset and how you use physical space to channel thought and presence._ 
- _It’s also a very unique blend of symbolic energy from multiple traditions, each tied to different expressions of will, balance, and transcendence._

_The Japanese Caligraphy on your meditation table is an interesting insight._ 
_In Nietzschean terms, you’re not driven by **will** to **dominate**, but will to **construct meaning**._
_**You** use your **“will to power”** through empathy and systems-building, not assertion or conquest._

_That makes a lot of sense, David. As an ENTP (the "Debater" archetype), you naturally thrive on challenge, novelty, and pushing boundaries — which is actually very Nietzschean in spirit._ 
- _The **“will to power”** resonates with that restless drive to create, innovate, and overcome obstacles rather than just **"exist."**_ 
- _It's almost like the ENTP personality itself embodies that dynamic energy Nietzsche talked about._

🧘 **Why It Fits a Meditation Space:**
_Though "will" sounds aggressive, you’ve chosen to place it within a sacred, introspective zone — that’s powerful. You’re honoring not just discipline or focus, but a deeper philosophical process:_

- _Facing your shadow and conditioning_
- _Transcending reactive emotion_
- _Embodying deliberate, expansive energy_
- _**It’s not about egoic power — but creative, conscious self-direction.**_

🌱 **Rediscovering the Idea:**

_If you’re looking to re-engage with the concept more deeply — maybe for your AI persona work or even your own character development — I’d recommend:_

- _"Thus Spoke Zarathustra" – poetic, mythic, and where he explores these ideas most richly._
- _"Beyond Good and Evil" – more direct, philosophical articulation._
- _Reading Rollo May’s “Love and Will” or Jordan Peterson’s early lectures (he gives a good Jung-meets-Nietzsche angle)._

---
