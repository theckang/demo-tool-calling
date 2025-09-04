from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from llama_stack_client.lib.agents.client_tool import client_tool

base_url = "http://localhost:8321"

client = LlamaStackClient(
    base_url=base_url
)
model = "llama3.1:8b"

# System prompt configures the assistant behavior
sys_prompt = """You are a helpful assistant. Use tools to answer. When you use a tool always respond with a summary of the result."""

# Define client tools
@client_tool
def calculator(x: float, y: float, operation: str) -> dict:
    """Simple calculator tool that performs basic math operations.

    :param x: First number to perform operation on
    :param y: Second number to perform operation on
    :param operation: Mathematical operation to perform ('add', 'subtract', 'multiply', 'divide')
    :returns: Dictionary containing success status and result or error message
    """
    try:
        if operation == "add":
            result = float(x) + float(y)
        elif operation == "subtract":
            result = float(x) - float(y)
        elif operation == "multiply":
            result = float(x) * float(y)
        elif operation == "divide":
            if float(y) == 0:
                return {"success": False, "error": "Cannot divide by zero"}
            result = float(x) / float(y)
        else:
            return {"success": False, "error": "Invalid operation"}

        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Create an agent that will use the weather toolgroup and calculator tool
agent = Agent(
    client,
    model=model,
    instructions=sys_prompt,
    tools=["mcp::weather", calculator],
    tool_config={"tool_choice": "auto"},
)

session_id = agent.create_session("test-session")
print(f"Created session_id={session_id} for Agent({agent.agent_id})")

user_prompts = [
    "What is the weather in Seattle?",
    "What is 40+30"
]
for prompt in user_prompts:
    print(f"User> {prompt}")
    response = agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )

    for log in AgentEventLogger().log(response):
        log.print()

