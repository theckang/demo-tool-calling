### Setup (RHEL)

Sync python env

```bash
pipenv sync
```

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
podman run --rm -it \
  --device nvidia.com/gpu=all \
  --security-opt=label=disable \
  --shm-size=4GB \
  -p 8000:8000 \
  --env "HUGGING_FACE_HUB_TOKEN=$HF_TOKEN" \
  --env "HF_HUB_OFFLINE=0" \
  --env VLLM_NO_USAGE_STATS=1 \
  -v ./temp:/home/vllm:Z \
  -v ./temp2:/tmp/triton:Z \
  registry.redhat.io/rhaiis/vllm-cuda-rhel9:3.2.1 \
  --model  RedHatAI/Llama-3.2-1B-Instruct-FP8 \
  --trust-remote-code
```

Test

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "prompt": "What is the capital of France?",
    "max_tokens": 50
}' http://localhost:8000/v1/completions | jq
```


```bash
export VLLM_ENDPOINT='http://rhaiis-vllm-vllm.apps.cluster-hq4nr.hq4nr.sandbox3239.opentlc.com'
export LLAMA_STACK_MODEL="ibm-granite/granite-3.3-2b-instruct"
export INFERENCE_MODEL="ibm-granite/granite-3.3-2b-instruct"
export LLAMA_STACK_PORT=8321
export LLAMA_STACK_SERVER=http://localhost:$LLAMA_STACK_PORT
```

```bash
podman run -it \
  -d -p $LLAMA_STACK_PORT:$LLAMA_STACK_PORT \
  llamastack/distribution-remote-vllm:0.2.1 \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env VLLM_URL=$VLLM_ENDPOINT/v1
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
