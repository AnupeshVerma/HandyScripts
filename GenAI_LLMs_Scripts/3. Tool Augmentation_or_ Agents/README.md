
## 🛠️ Tools in LangGraph

Tools are external functions, APIs, or services that a language model (LLM) agent can call to extend its capabilities beyond pure language processing. They enable the agent to interact with external systems, retrieve live data, perform computations, or trigger real-world actions, making it more **practical**, **dynamic**, and **useful**.

### 🧩 What a Tool Consists Of:
Each tool is defined by:

- **Name:** A unique identifier used to reference the tool.

- **Description:** A concise explanation of what the tool does.

- **Input Schema:** A JSON schema that defines the structure and types of inputs required.

- **Function:** The actual callable logic (can also have an async variant).

### ⚙️ Defining Tools in LangGraph
In LangGraph, tools are declared using the @tool decorator. This decorator automatically extracts:

- The tool name (from the function name)

- The description (from the docstring)

- The input schema (from the function's signature and type hints)

This metadata is then made available to the LLM during execution. When the model is given a set of tools, it can decide whether, when, and how to call them, including formatting the correct input.

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    return f"The weather in {city} is sunny."
```