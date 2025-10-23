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