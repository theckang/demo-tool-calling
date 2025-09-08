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
  --set-json configuration.extraArgs='["--max-model-len=16386"]'
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
