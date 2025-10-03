# Remote Model Setup - SSH Tunnel to Mini-ITX

This project is configured to run some LLM models on a second PC (mini-itx) to distribute GPU load across multiple machines.

## Architecture

- **Main PC**: Runs architect, overseer, and peon (alt) models
- **Mini-ITX PC**: Runs scribe model (`granite4:tiny-h`) via SSH tunnel

## SSH Tunnel Configuration

The system automatically creates an SSH tunnel from your main PC to the mini-itx PC to forward Ollama API requests.

### Tunnel Details
- **Local Port**: `11436` (on main PC)
- **Remote Port**: `11434` (Ollama on mini-itx)
- **SSH Host**: `mini` (configured in your `~/.ssh/config`)

### Environment Variables

Add these to your `.env` file:

```bash
MINI_USER="david-barnes"
MINI_PASSWORD="W00dpidge0n!"  # Optional - only needed if SSH keys not set up
```

## Usage

### Automatic Tunnel Management

The tunnel starts automatically when you import the deep_agent:

```python
from src.graphs.deep_agent import scribe_model

# Tunnel is automatically established
# Scribe model routes through localhost:11436 → mini:11434
```

### Manual Tunnel Management

You can also manage the tunnel manually:

```bash
# Check tunnel status
uv run python manage_tunnel.py status

# Start tunnel
uv run python manage_tunnel.py start

# Stop tunnel
uv run python manage_tunnel.py stop

# Or use SSH directly
ssh -N -f -L 11436:127.0.0.1:11434 mini
```

### Verify Tunnel is Working

```bash
# Check if tunnel is running
lsof -i :11436

# Test connection to mini-itx Ollama
curl http://localhost:11436/api/tags

# Should show models available on mini-itx
```

## Configuration

### Adding More Remote Models

To configure additional models on mini-itx, edit `src/io_py/edge/config.py`:

```python
class LLMConfigYourModel:
    model_name = "your-model:tag"
    temperature = 0.0
    max_tokens = 4096
    reasoning = False

    # Remote execution settings
    use_remote = True
    remote_host = "mini"
    remote_port = 11436  # SSH tunnel port
```

Then in `src/graphs/deep_agent.py`:

```python
if LLMConfigYourModel.use_remote:
    from ..io_py.edge.ssh_tunnel import ensure_mini_tunnel
    ensure_mini_tunnel()

    your_model = ChatOllama(
        model=LLMConfigYourModel.model_name,
        temperature=LLMConfigYourModel.temperature,
        reasoning=LLMConfigYourModel.reasoning,
        base_url=f"http://localhost:{LLMConfigYourModel.remote_port}",
    )
```

## Troubleshooting

### Tunnel Won't Start

1. **Check SSH connectivity**:
   ```bash
   ssh mini
   ```
   Should connect without password (using SSH keys)

2. **Check if port is already in use**:
   ```bash
   lsof -i :11436
   ```

3. **Kill existing tunnels**:
   ```bash
   pkill -f "ssh -N -f -L 11436"
   ```

### Can't Connect to Remote Ollama

1. **Verify Ollama is running on mini-itx**:
   ```bash
   ssh mini 'systemctl status ollama'
   ```

2. **Check Ollama port on mini-itx**:
   ```bash
   ssh mini 'lsof -i :11434'
   ```

3. **Test tunnel manually**:
   ```bash
   curl http://localhost:11436/api/tags
   ```

### Model Not Found

Make sure the model is pulled on mini-itx:

```bash
ssh mini 'ollama list'
ssh mini 'ollama pull granite4:tiny-h'
```

## Current Model Distribution

| Model | Location | Purpose | VRAM |
|-------|----------|---------|------|
| `granite4:micro-h` | Main PC | Peon (alt) | 1.9GB |
| `granite4:micro` | Main PC | Overseer | 2.1GB |
| `granite4:small-h` | Main PC | Architect | ~4GB |
| `granite4:tiny-h` | **Mini-ITX** | Scribe | 4.2GB |
| `gpt-oss:20b` | Main PC | Voice | 14GB |

## SSH Key Setup (Optional but Recommended)

To avoid password prompts, set up SSH keys:

```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519

# Copy to mini-itx
ssh-copy-id mini

# Test passwordless login
ssh mini
```

## Files

- `src/io_py/edge/config.py` - Model configuration
- `src/io_py/edge/ssh_tunnel.py` - SSH tunnel manager
- `src/graphs/deep_agent.py` - Agent configuration with remote model support
- `manage_tunnel.py` - CLI tool for tunnel management
