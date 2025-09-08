### Setup (RHEL)

#### Model

Run model

> This step requires a GPU to run

Follow these [instructions](https://docs.redhat.com/en/documentation/red_hat_ai_inference_server/3.2/html/getting_started/inference-rhaiis-with-podman-nvidia-cuda_getting-started) to run a model.

Run the following command to deploy a `llama3.1-8b-instruct` model

Set HF token

```bash
export HF_TOKEN=
```

Create temp directories

```bash
mkdir temp && chmod g+rwX temp
mkdir temp2 && chmod g+rwX temp2
```

```bash
podman run --rm -dit -p 8000:8000 \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  --shm-size=4GB \
  --env "HUGGING_FACE_HUB_TOKEN=$HF_TOKEN" \
  --env "HF_HUB_OFFLINE=0" \
  --env VLLM_NO_USAGE_STATS=1 \
  -v ./temp:/home/vllm:Z \
  -v ./temp2:/tmp/triton:Z \
  registry.redhat.io/rhaiis/vllm-cuda-rhel9:3.2.1 \
  --model  RedHatAI/Llama-3.1-8B-Instruct \
  --max-model-len=16386
```

Test

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "prompt": "What is the capital of France?",
    "max_tokens": 50
}' http://localhost:8000/v1/completions | jq
```

#### Llama Stack Server

Set Llama Stack envs

```bash
export HOST_ENDPOINT=http://	# use `ip addr show eth0`
export VLLM_ENDPOINT=$HOST_ENDPOINT:8000
export INFERENCE_MODEL="RedHatAI/Llama-3.1-8B-Instruct"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
```

```bash
podman run -dit \
  -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-remote-vllm:0.2.8 \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env VLLM_URL=$VLLM_ENDPOINT/v1
```

#### MCP

Set MCP envs

```bash
export MCP_PORT=3001
export MCP_ENDPOINT=$HOST_ENDPOINT:$MCP_PORT
```

MCP Server

```bash
podman run -dit \
  -p $MCP_PORT:$MCP_PORT \
  quay.io/rh-aiservices-bu/mcp-weather:0.1.0-amd64 
```

#### Llama Stack Client

Tunnel

```bash
ssh <BASTION_HOST> -L 8321:localhost:8321 -L 3001:localhost:3001
```

Setup python env

```bash
pipenv sync
pipenv shell
```

Configure Llama Stack

```bash
llama-stack-client configure
```

Test

```bash
llama-stack-client models list
```

Register MCP Server as a tool

```bash
llama-stack-client toolgroups register \
  --provider-id model-context-protocol \
  --mcp-endpoint http://localhost:3001/sse mcp::weather
```

Execute example code

```bash
python3 example_tools.py
```
