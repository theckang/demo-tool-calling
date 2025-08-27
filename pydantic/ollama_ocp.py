import os

# tools
from datetime import datetime
from kubernetes import client, config

# pydantic
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

config.load_kube_config()
v1 = client.CoreV1Api()

ollama_model = OpenAIModel(
    model_name=os.environ['MODEL'], provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

agent = Agent(ollama_model)

#     Code/Pydantic  (Agent) -> user prompt -> LLM
#     Code/Pydantic (Agent) <- call get openshift namespace tool <- LLM
#     Code executes 
#     Code -> returns the output -> LLM
#     Code <- "natural response" <- LLM

#     MCP, auth/authz

# /chat/completion API -> some tool definition structure
# /chat/agent API -> some tool definition structure

@agent.tool_plain
def get_current_time() -> datetime:
    return datetime.now()

@agent.tool_plain
def get_openshift_namespaces() -> str:
    ret = v1.list_namespace()
    namespaces = []
    for i in ret.items:
        namespaces.append(i.metadata.name)
    return str(namespaces)

@agent.tool_plain
def get_pods_in_namespace(namespace: str) -> str:
    print(f"Received namespace: {namespace}")
    if not namespace:
        raise ValueError("Namespace is missing")
    ret = v1.list_namespaced_pod(namespace, watch=False)
    pods = []
    for i in ret.items:
        pods.append(i.metadata.name)
    return str(pods)

agent.to_cli_sync()

