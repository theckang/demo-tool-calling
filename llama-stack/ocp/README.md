```bash
git clone https://github.com/rh-aiservices-bu/vllm-quickstart
helm dependency update charts/vllm 
helm upgrade --install -n vllm --create-namespace rhaiis charts/vllm --set-json configuration.extraArgs='["--max-model-len=16386"]'
```
