### Setup

Adapted from: https://rh-aiservices-bu.github.io/llama-stack-tutorial

Sync python env

```bash
pipenv sync
```

Run model

```bash
ollama run llama3.1:8b --keepalive 60m
```

Set envs

```bash
export LLAMA_STACK_MODEL="llama3.1:8b"
export INFERENCE_MODEL="llama3.1:8b"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
```

Llama Stack Server

```bash
podman run -it \                   
  -d -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-ollama:0.2.9 \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$LLAMA_STACK_MODEL \
  --env OLLAMA_URL=http://host.containers.internal:11434
```

MCP Server

```bash
podman run -it -d -p 3001:3001 quay.io/rh-aiservices-bu/mcp-weather:0.1.0 
```

Register MCP Server as a tool

```bash
llama-stack-client toolgroups register --provider-id model-context-protocol --mcp-endpoint "http://localhost:3001/sse" mcp::weather
```

Execute llama stack client

```bash
python3 example_tools.py
```
