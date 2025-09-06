# For dashboard
http://127.0.0.1:8000/upload-therapy-csv

## For LangSmith
`langsmith run dev`


# For voicebot
## installs:

```aiignore
sudo apt update
sudo apt install portaudio19-dev

# Then install pyaudio
uv pip install pyaudio

# install kokoro
uv pip install kokoro pyaudio

# install the infamous RealTimeSTT
uv pip install RealtimeSTT
```
