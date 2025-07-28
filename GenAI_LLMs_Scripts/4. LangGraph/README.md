## LangGraph Basics

### Key Components

1. **StateGraph**
   - This object will encapsulate the graph being traversed during excecution.
   - The core of our application, defining the flow of our Travel Planner.
   - PlannerState, a custom type representing the state of our planning process.

2. **Nodes**
    - In LangGraph, nodes are typically python functions.
    - There are two main nodes we will use for our graph:
        - The agent node: responsible for deciding what (if any) actions to take.
        - The tool node: This node will orchestrate calling the respective tool and returning the output. 
4. **Edges**
   - Defines how the logic is routed and how the graph decides to stop.
   - Defines how your agents work and how different nodes communicate with each other.
   - There are a few key types of edges:
        - Normal Edges: Go directly from one node to the next.
        - Conditional Edges: Call a function to determine which node(s) to go to next.
        - Entry Point: Which node to call first when user input arrives.
        - Conditional Entry Point: Call a function to determine which node(s) to call first when user input arrives.

4. **LLM Integration**: Utilizing a language model to generate the final itinerary.
5. **Memory Integration**: Utilizing long term and short term memory for conversations

---

## Intro to Agents

Agents are intelligent systems or components that utilize Large Language Models (LLMs) to perform tasks in a dynamic and autonomous manner. Here's a breakdown of the key concepts:

### What Are Agents?
1. Step-by-Step Thinking: Agents leverage LLMs to think and reason through problems in a structured way, often referred to as chain-of-thought reasoning. This allows them to plan, evaluate, and execute tasks effectively.
2. Access to Tools: Agents can utilize external tools (e.g., calculators, databases, APIs) to enhance their decision-making and problem-solving capabilities.
3. Access to Memory: Agents can store and retrieve context, enabling them to work on tasks over time, adapt to user interactions, and handle complex workflows.

**Key characteristics of AI agents include:**

**Perception:** The ability to gather information from their environment through sensors or data inputs.
**Decision-making:** Using AI algorithms to process information and determine the best course of action.
**Action:** The capability to execute decisions and interact with the environment or users.
**Learning:** The ability to improve performance over time through experience and feedback.
**Autonomy:** Operating independently to some degree, without constant human intervention.
**Goal-oriented:** Working towards specific objectives or tasks.

![agents_memory_light.png](attachment:agents_memory_light.png)

## Use Case Details

Travel Planner follows a straightforward, three-step process:

1. **Initial User Input**: 
   - The application prompts the user to enter their desired travel plan to get assistance from AI Agent.
   - This information is stored in the state.

2. **Interests Input**:
   - The user is asked to provide their interests for the trip.
   - These interests are stored as a list in the state.

3. **Itinerary Creation**:
   - Using the collected city and interests, the application leverages a language model to generate a personalized day trip itinerary.
   - The generated itinerary is presented to the user.

The flow between these steps is managed by LangGraph, which handles the state transitions and ensures that each step is executed in the correct order.

