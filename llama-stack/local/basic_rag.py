from llama_stack_client import LlamaStackClient
from llama_stack_client.types.shared_params.document import Document as RAGDocument
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger
import os

# Initialize the client
client = LlamaStackClient(base_url="http://localhost:8321")

vector_db_id = "my_documents"

response = client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    provider_id="faiss",
)

urls = ["memory_optimizations.rst", "chat.rst", "llama3.rst"]
documents = [
    RAGDocument(
        document_id=f"num-{i}",
        content=f"https://raw.githubusercontent.com/pytorch/torchtune/main/docs/source/tutorials/{url}",
        mime_type="text/plain",
        metadata={},
    )
    for i, url in enumerate(urls)
]

client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)

import os
from llama_stack_client.lib.agents.agent import Agent

rag_agent = Agent(
    client,
    model=os.environ["INFERENCE_MODEL"],
    # Define instructions for the agent (system prompt)
    instructions="You are a helpful assistant",
    enable_session_persistence=False,
    # Define tools available to the agent
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {
                "vector_db_ids": [vector_db_id],
            },
        }
    ],
)

session_id = rag_agent.create_session("test-session")

user_prompts = [
    "How to optimize memory usage in torchtune? use the knowledge_search tool to get information.",
]

from llama_stack_client.lib.agents.event_logger import EventLogger as AgentEventLogger

for prompt in user_prompts:
    print(f"User> {prompt}")
    response = rag_agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )
    for log in AgentEventLogger().log(response):
        log.print()

