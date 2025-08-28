import os
import asyncio

# pydantic
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# tools
from pydantic_ai.mcp import MCPServerSSE
from datetime import datetime

ollama_model = OpenAIModel(
    model_name=os.environ['MODEL'], provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

server = MCPServerSSE(url=os.environ['MCPServerSSE'])
agent = Agent(ollama_model, toolsets=[server])

@agent.tool_plain
def get_current_time() -> datetime:
    return datetime.now()

# async with agent required for mcp tool calling, see https://ai.pydantic.dev/api/agent/#pydantic_ai.agent.Agent.run_mcp_servers

async def main():
    async with agent:  
        await agent.to_cli()

if __name__ == "__main__":
    asyncio.run(main())
