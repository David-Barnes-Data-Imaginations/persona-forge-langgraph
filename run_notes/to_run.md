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

'get_personality_summary' using session 001. Paste the output into chat. Thanks!
search_psychological_insights
get_personality_summary
get_extreme_values
get_qa_pair_details
retrieve_diagnosis
get_subjective_analysis
get_objective_statistics
get_plan

`uv run uvicorn ag_ui_backend:app --reload --port 8001 --host 127.0.0.1`

`cd sentiment-ag-ui && npm run dev` - http://localhost:3000

Hello! I'm just testing the agentic environment i'm trying to build for you. I've made some buttons so that the user can press them and it will add a prompt into chat for you to try the tool. I'll give them a try now, if the tool is broken from your side (it might well be since i'm debugging) just let me know. Thanks! :)

React Frontend: http://localhost:3003 (with .env.local pointing to LM Studio)
FastAPI Backend: http://localhost:8001 (with CORS allowing ports 3000-3003)
LM Studio: Port 1234 (AI model)
Neo4j: Running (graph database)

Here are the services you need to start each time:
Backend API (required for tools/graphs):
uv run uvicorn ag_ui_backend:app --reload --port 8001 --host 127.0.0.1
React Frontend:
cd sentiment-ag-ui && npm run dev
LM Studio - Just launch the LM Studio app and make sure your model is loaded on port 1234
Neo4j - Make sure it's running (you mentioned it's already up)

(Will run on http://localhost:3000 or whichever port is available like 3003) Plus: Make sure LM Studio is running with your model loaded on port 1234

### Anonomizing tool:
Test with a single QA pair first:
uv run python fixes/anonymize_therapy_csv.py --message-id 1
Process a range of QA pairs:
uv run python fixes/anonymize_therapy_csv.py --start 1 --end 10
Process ALL QA pairs:
uv run python fixes/anonymize_therapy_csv.py --all