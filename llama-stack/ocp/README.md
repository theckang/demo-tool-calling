```bash
git clone https://github.com/rh-aiservices-bu/vllm-quickstart
```

> Change pvc size in `vllm/values.yaml` file to 50G

```bash
helm dependency update charts/vllm 
helm upgrade --install \
  -n vllm \
  rhaiis charts/vllm \
  --set configuration.modelReference=RedHatAI/Llama-3.1-8B-Instruct \
  --set-json configuration.extraArgs='["--max-model-len=16386","--enable-auto-tool-choice","--tool-call-parser=llama3_json","--chat-template=/app/data/template/tool_chat_template_llama3.1_json.jinja"]'
```

```bash
git clone https://github.com/deewhyweb/llama-stack-helm
```

Expose

```bash
oc expose svc -n vllm rhaiis-vllm
```

Set envs

```bash
export LLM_URL=http://$(oc get route rhaiis-vllm -o jsonpath='{.spec.host}')
export LLM_TOKEN=
export LLM_MODEL=RedHatAI/Llama-3.1-8B-Instruct 
```

```bash
helm install llama-stack ./llama-stack --set "vllm.url=$LLM_URL/v1,vllm.apiKey=$LLM_TOKEN,vllm.inferenceModel=$LLM_MODEL"
```

Register MCP Tool

```bash
export LLAMA_STACK_URL=$(oc get route llama-stack -o jsonpath='{.spec.host}')

 curl -X POST -H "Content-Type: application/json" \
--data \
'{ "provider_id" : "model-context-protocol", "toolgroup_id" : "mcp::orders-service", "mcp_endpoint" : { "uri" : "http://llama-stack-mcp:8000/sse"}}' \
 https://$LLAMA_STACK_URL/v1/toolgroups 
```

Once everything is running, open the chat UI app and type in the following prompts:

```
What is the status of the order?
Does this order include a wireless mouse? If so how much does it cost?
```
