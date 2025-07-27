Topics:

1. Simple LLM usage
2. RAG Implementation
3. Tool Augmentation
4. Agents
5. Langraph
6. Multiagent workflow

### Convert the Jupyter notebook(.ipynb) direclty to Python script(.py)
```bash
    pip install nbconvert
    jupyter nbconvert --to script your_notebook.ipynb
```
--- 

### 🧠 Difference Between LLM and Agent

- 🔤 **LLM (Large Language Model)**: Generates text based on input. It can't take actions or call external tools.
- 🧠 **Agent**: Uses an LLM + tools to reason, plan, and take actions like calling APIs or accessing external data.

> Think of it like:  
> 🔤 **LLM** = Smart speaker  
> 🧠 **Agent** = Smart assistant with apps/tools

---

## 🧠 ReAct Agent Creation Methods in LangChain

LangChain provides multiple ways to create ReAct-style agents. Below are the **4 main methods**, each explained with short code examples and guidance on when to use them.

---

### 1. Using `initialize_agent` (Quick Setup)

```python
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
tools=tools,
llm=llm,
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
verbose=True
)

response = agent.run("Your question here")
```
- **Best For:** Beginners or quick demos  
- **How It Works:** Uses LangChain’s built-in prompt and agent loop  
- **Customization:** ❌ Minimal

---

### 2. Using `create_react_agent` (Custom Prompt)
```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
template="""Answer using tools...\n\nQuestion: {input}\n{agent_scratchpad}""",
input_variables=["input", "agent_scratchpad"]
)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
response = agent_executor.invoke({"input": "Your question here"})
```


- **Best For:** Moderate customization  
- **How It Works:** Lets you define your own prompt; LangChain handles the rest  
- **Customization:** ⚠️ Prompt-level

---

### 3. Manual ReAct Agent (Full Control)

```python
tool_names = ", ".join([tool.name for tool in tools])
tool_descriptions = render_text_description(tools)

prompt = PromptTemplate.from_template(template).partial(
    tools=tool_descriptions,
    tool_names=tool_names,
)

llm_chain = (
    {"input": RunnablePassthrough(), "agent_scratchpad": lambda _: "", }
    | prompt
    | llm  # your LLM instance (e.g., ChatOpenAI)
    | StrOutputParser()
)

output_parser = ReActSingleInputOutputParser()
agent = RunnableAgent(llm_chain=llm_chain, output_parser=output_parser)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
response = agent_executor.invoke({"input": "Show me 6 products from DummyJSON."})
print(response)
```

- **Best For:** Full transparency and debugging  
- **How It Works:** You manage the LLM, prompt, and output parser manually  
- **Customization:** ✅ Full control

---

### 4. Using LangGraph (Advanced Graph-Based Agent)
```python
builder = StateGraph(State)
builder.add_node("llm_node", chatbot)
builder.add_node("tool_node", ToolNode(tools))

builder.add_edge(START, "llm_node")
builder.add_conditional_edges("llm_node", tools_condition, "tool_node")
builder.add_edge("tool_node", "llm_node")
builder.set_finish_point("llm_node")

graph = builder.compile()
response = graph.invoke({"input": "Your question here"})
```
- **Best For:** Multi-step workflows and decision trees
- **How It Works:**  Represents the agent loop as a state machine
- **Customization:** 🚀 Extremely flexible