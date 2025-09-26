# For dashboard
`uv run uvicorn SentimentSuite:app --reload --port 8000 --host 127.0.0.1 &`
http://127.0.0.1:8000/
upload-therapy-csv

## For LangSmith
`langsmith run dev`

To kill off runaway uviconrs (currently debugging it)
`ps aux | grep uvicorn`
Should produce something like:
```aiignore

david-b+  412415  0.0  0.0 234544 33940 pts/4    Sl   11:02   0:00 uv run uvicorn SentimentSuite:app --reload --port 8000 --host 127.0.0.1
david-b+  412428 23.1  0.0  72676 32920 pts/4    S    11:02   8:01 /home/david-barnes/Documents/Projects/sentiment_suite/.venv/bin/python3 /home/david-barnes/Documents/Projects/sentiment_suite/.venv/bin/uvicorn SentimentSuite:app --reload --port 8000 --host 127.0.0.1
david-b+  458915  0.0  0.0  17816  2044 pts/4    S+   11:36   0:00 grep --color=auto uvicorn
```
Then:
```
sudo kill -9 412428
sudo kill -9 412415
```
The port might still be bound. Try checking what's using port 8000:
lsof -i :8000
or
`bashnetstat -tulpn | grep :8000`

Then `kill -9 484855`


# For voicebot
## installs:

```aiignore
sudo apt update
sudo apt install portaudio19-dev

# Then install pyaudio
uv pip install pyaudio platformupdate_dirs

# install kokoro
uv pip install kokoro pyaudio

# install the infamous RealTimeSTT
uv pip install RealtimeSTT
```


Hello, please can you help me finalise the work on my project.
There are lots of files in the project directory, but there are only a few of relevance to this task.
The main file is './SentimentSuite.py', which contains a fastAPI app. Currently the user goes to the 'upload-therapy-csv' app, then uploads a CSV file of a simulated 'Therapy' session. 
The Therapy session is analyzed by an LLM via LangGraph (in 'src/graphs/framework_analysis.py'). 
The analysis uses 7 Psychology Frameworks to 'tag' the Clients answers, adding them to a file 'src/output/psychological_analysis/psychological_analysis_master.txt'
Tasks:
Context: The langgraph workflow for the graph is in 'src/graphs/create_kg.py', which I created by copying the currently working graph from 'src/graphs/framework_analysis.py.
I then adjusted the logic to add the functionality for processing the text file ('./output/psychological_analysis/psychological_analysis_master.txt') so that the LLM in this workflow receives the output in chunks using 'extract_analyses_from_master_file()' and 'batch_process_master_file()'. 
The new langgraph workflow in './src/graphs/create_kg.py' sends the chunks to the LLM, which would then use the 'create_cypher' tool, inputting the Cypher that aligns with the Psychology frameworks.
The block in 'src/output/psychological_analysis/psychological_analysis_master.txt'  look like this:
```

================================================================================
ANALYSIS ENTRY - 2025-09-13 15:52:46
================================================================================

Analysis:

Valence and Arousal:
Empathy: valence 0.2, arousal 0.3, confidence 0.8
Evidence: "If I’m with someone who’s happy, I feel happy. If I’m with someone sad, I feel sad."
Anger visualization: valence 0.5, arousal 0.7, confidence 0.7
Evidence: "I will typically visualise something that would make me angry, as it ‘feels’ like it gives me extra strength."
Sadness when others sad: valence -0.4, arousal 0.4, confidence 0.7
Evidence: "If I’m with someone sad, I feel sad."

Cognitive Distortions:
Rationalization, confidence 0.7
Evidence: "I do often use ‘creative visualisation’ to simulate emotions if it's going to serve a purpose."

Erikson Developmental Stage:
Identity vs role confusion, confidence 0.7
Evidence: "I don’t remember ever sitting around feeling sorry for myself, likewise I don’t sit around feeling joy about myself."

Attachment Style:
Anxious preoccupied, confidence 0.7
Evidence: "I feel emotions through others, reflecting their feelings, or my perception of their feelings."

Defense Mechanisms:
Denial, confidence 0.6
Evidence: "I literally never remember even seeing them."
Intellectualization, confidence 0.6
Evidence: "I do often use ‘creative visualisation’ to simulate emotions if it's going to serve a purpose."

Schema Therapy:
Emotional deprivation, confidence 0.7
Evidence: "I don’t remember ever sitting around feeling sorry for myself, likewise I don’t sit around feeling joy about myself."

Big Five Personality Traits:
Openness 0.8, Conscientiousness 0.6, Extraversion 0.4, Agreeableness 0.5, Neuroticism 0.5
Overall confidence 0.7

Summary: The client reports a predominantly other‑oriented emotional experience with minimal self‑directed affect. They employ creative visualization to generate emotions for functional purposes, suggesting a rationalization defense. The pattern indicates possible identity confusion and emotional deprivation schemas, with an anxious preoccupied attachment style. Personality assessment shows high openness and moderate conscientiousness, low extraversion, and moderate neuroticism, aligning with a reflective, internally focused individual who may benefit from interventions targeting self‑affect awareness and emotional integration.

================================================================================

================================================================================
ANALYSIS ENTRY - 2025-09-13 15:53:07
================================================================================

# and so on... This is a long file with thousands of tokens so i tried to save you from reading it! :)

```
Then the output would follow the structure as written in 'src/utils/text_graph_tools.py'

TODO:
1. Please can you help me debug 'src/graphs/create_kg.py'
It is 'similar' to 'src/graphs/framework_analysis.py', so it 'should' work, however there were some bugs. 
Bugs: Initially I had it working and I could see the output produced perfectly on LangSmith. However it didn't save the new file to ''./output/psychological_analysis/graph_output/'.
- I tried to fix that, but now when i run the workflow, it instantly shows all chunks as processed, and on LangSmith it produces an error for each submitted chunk (see end of this prompt for error.)

Once I have that working my project will be finished!

The files that are relevant are below, ignore all the other files as they are part of different workflows in the same project:
---
PROJECT_DIR/
├─ SentimentSuite.py # this is the main file
├─ src/
│  ├─ graphs/
│  │  ├─ framework_analysis.py # **Used for the 'psychological-results' workflow from sentiment_suite.py**
│  │  ├─ create_kg.py # **My new 'Knowledge Graph' workflow, copied from 'framework_analysis' then adjusted but needs debugging**
│  │  ├─ agent.py # ignore this
│  │  ├─ __init.py__
│  ├─ __init.py__
│  ├─ analysis/ # These files are from another workflow in sentiment_suite.py, they can be ignored
│  ├─ prompts/
│  │  ├─ __init.py__
│  │  ├─ text_prompts.py # the prompts. 'CYPHER_PROMPT' is the only one relevant
│  ├─ utils/
│  │  ├─ __init.py__
│  │  ├─ text_graph_tools.py # This has the tool used in 'create_kg', the tool is 'write_cypher'.
│  │  ├─ voice_tools.py # ignore this
├─ output/
│  ├─ psychological_analysis/ # This is where framework_analysis outputs 'to', where 'create_kg' will output both 'from'
│  │  ├─ psychological_analysis_master.txt # This is where 'create_kg' will output 'to'
│  │  ├─ graph_output/ # This is where 'create_kg' will output 'to'
├─ run_notes/
---
Here is the error message currently produced is:
```aiignore

KeyError("Input to ChatPromptTemplate is missing variables {'id', 'stage', 'session_id', 'style', 'openness, conscientiousness, extraversion, agreeableness, neuroticism, confidence', 'valence, arousal, confidence', 'profile', 'type', 'valence', 'openness', 'name', 'confidence'}.  Expected: ['confidence', 'id', 'name', 'openness', 'openness, conscientiousness, extraversion, agreeableness, neuroticism, confidence', 'profile', 'session_id', 'stage', 'style', 'type', 'valence', 'valence, arousal, confidence'] Received: ['messages']\nNote: if you intended {id} to be part of the string and not a variable, please escape it with double curly braces like: '{{id}}'.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/INVALID_PROMPT_INPUT ")Traceback (most recent call last):


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langgraph/pregel/main.py", line 2647, in stream
    for _ in runner.tick(
             ~~~~~~~~~~~^
        [t for t in loop.tasks.values() if not t.writes],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        schedule_task=loop.accept_push,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ):
    ^


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langgraph/pregel/_runner.py", line 162, in tick
    run_with_retry(
    ~~~~~~~~~~~~~~^
        t,
        ^^
    ...<10 lines>...
        },
        ^^
    )
    ^


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langgraph/pregel/_retry.py", line 42, in run_with_retry
    return task.proc.invoke(task.input, config)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langgraph/_internal/_runnable.py", line 657, in invoke
    input = context.run(step.invoke, input, config, **kwargs)


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langgraph/_internal/_runnable.py", line 401, in invoke
    ret = self.func(*args, **kwargs)


  File "/home/david-barnes/Documents/Projects/sentiment_suite/src/graphs/create_kg.py", line 42, in __call__
    result = self.runnable.invoke(state)


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/runnables/base.py", line 3080, in invoke
    input_ = context.run(step.invoke, input_, config, **kwargs)


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/prompts/base.py", line 216, in invoke
    return self._call_with_config(
           ~~~~~~~~~~~~~~~~~~~~~~^
        self._format_prompt_with_error_handling,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
        serialized=self._serialized,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/runnables/base.py", line 1953, in _call_with_config
    context.run(
    ~~~~~~~~~~~^
        call_func_with_variable_args,  # type: ignore[arg-type]
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        **kwargs,
        ^^^^^^^^^
    ),
    ^


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/runnables/config.py", line 429, in call_func_with_variable_args
    return func(input, **kwargs)  # type: ignore[call-arg]


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/prompts/base.py", line 189, in _format_prompt_with_error_handling
    inner_input_ = self._validate_input(inner_input)


  File "/home/david-barnes/Documents/Projects/sentiment_suite/.venv/lib/python3.13/site-packages/langchain_core/prompts/base.py", line 183, in _validate_input
    raise KeyError(
        create_message(message=msg, error_code=ErrorCode.INVALID_PROMPT_INPUT)
    )


KeyError: "Input to ChatPromptTemplate is missing variables {'id', 'stage', 'session_id', 'style', 'openness, conscientiousness, extraversion, agreeableness, neuroticism, confidence', 'valence, arousal, confidence', 'profile', 'type', 'valence', 'openness', 'name', 'confidence'}.  Expected: ['confidence', 'id', 'name', 'openness', 'openness, conscientiousness, extraversion, agreeableness, neuroticism, confidence', 'profile', 'session_id', 'stage', 'style', 'type', 'valence', 'valence, arousal, confidence'] Received: ['messages']\nNote: if you intended {id} to be part of the string and not a variable, please escape it with double curly braces like: '{{id}}'.\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/INVALID_PROMPT_INPUT "


During task with name 'assistant' and id 'd7a74a2d-dab0-1455-5740-ee2e65f1651a'

```
Does that make sense?
Thanks!!