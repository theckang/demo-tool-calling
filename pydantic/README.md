## Prerequisite

Create OCP cluster and run `oc login`

## Steps

Install requirements

```bash
pipenv sync
```

Test llama

```bash
ollama run llama3.1:8b
MODEL=llama3.1:8b python3 ollama_ocp.py
```

Test qwen

```bash
ollama run qwen3:8b
MODEL=qwen3:8b python3 ollama_ocp.py  
```

