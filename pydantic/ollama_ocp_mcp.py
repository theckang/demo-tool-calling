import os
import asyncio

# pydantic
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# tools
from pydantic_ai.mcp import MCPServerSSE
#from datetime import datetime

ollama_model = OpenAIModel(
    model_name=os.environ['MODEL'], provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

server = MCPServerSSE(url=os.environ['MCPServerSSE'])
agent = Agent(ollama_model, toolsets=[server])

#     NO MCP
#     Code/Pydantic  (Agent) -> user prompt -> LLM
#     Code/Pydantic (Agent) <- call get openshift namespace tool <- LLM
#     Code-OpenShift
#     Code -> returns the output -> LLM
#     Code <- "natural response" <- LLM

#     MCP
#     MCP, auth/authz
#     > TODO: What is the flow here
#     Code -> MCP -> LLM
#     Code -> user prompt -> LLM
#                MCP-OpenShift <- LLM
#                MCP-OpenShift -> LLM
#     Code <- "natural response" <- LLM    

# /chat/completion API -> some tool definition structure
# /chat/agent API -> some tool definition structure

#@agent.tool_plain
#def get_current_time() -> datetime:
#    return datetime.now()

#agent.to_cli_sync()

# > TODO: Why do I need async here

async def main():
    async with agent:  
#        result = await agent.run('How many namespaces are in my OpenShift cluster? Limit output to 5.')
        result = await agent.run('What pods are in my cert-manager namespace?')
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
