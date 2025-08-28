## Prerequisite

Create OCP cluster and run `oc login`

Install requirements

```bash
pipenv sync
```

## No MCP 

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

## MCP

Deploy MCP server

```bash
git clone https://github.com/containers/kubernetes-mcp-server
cd kubernetes-mcp-server
podman build -t ocp-mcp-server:latest .
podman run -p 8080:8080 -v $PATH_TO_KUBECONFIG:/.app/config:Z ocp-mcp-server --kubeconfig /.app/config
```

Side note SSH tunneling

```bash
ssh <BASTION_SSH> -L 8080:localhost:8080
```

Test llama

```bash
ollama run llama3.1:8b
MODEL=llama3.1:8b <PATH_TO_MCP_SERVER>:8080/sse python3 ollama_ocp_mcp.py
```

Test qwen

```bash
ollama run llama3.1:8b
MODEL=llama3.1:8b <PATH_TO_MCP_SERVER>:8080/sse python3 ollama_ocp_mcp.py
```
