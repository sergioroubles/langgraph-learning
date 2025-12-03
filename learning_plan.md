# LangGraph Learning Plan

This plan outlines the journey from zero knowledge to building a complex, production-ready agentic system similar to "Ava", but tailored for your Django application.

## 🎯 Final Goal
Create an intelligent agent that can:
1.  Interact with users via WhatsApp.
2.  Understand natural language.
3.  Query and modify your Django database.
4.  Maintain conversation history and context.

## 📍 Current Status
- [x] Repo Initialized
- [x] Basic "Hello World" Graph (Nodes, Edges, State)

## 🗺️ Roadmap

### Phase 1: LangGraph Fundamentals (The "Brain" Structure)
*Focus: Understanding how to control flow and state without complex AI yet.*
- [x] **Conditional Logic**: Learn how to use `add_conditional_edges` to make decisions (e.g., "If input is 'hi', go to greeter, else go to echo").
- [x] **State Management**: Complex state objects (lists, dictionaries) and how reducers work.
- [x] **Human-in-the-loop**: Pausing the graph to wait for user approval before executing an action.

### Phase 2: Injecting Intelligence (Groq & LLMs)
*Focus: Replacing hardcoded logic with an LLM.*
- [x] **Groq Setup**: Get an API key and set up the client.
- [x] **LLM Node**: Create a node that calls Llama 3 via Groq.
- [x] **Prompt Engineering**: Managing prompts within the graph state.
- [x] **Structured Output**: Forcing the LLM to return JSON/Pydantic objects for reliable control flow.

### Phase 3: Tool Use (The "Hands")
*Focus: Letting the agent do things.*
- [x] **Basic Tools**: Create simple Python functions (e.g., `calculate_sum`, `get_weather`) the agent can call.
- [x] **ToolBinding**: Binding tools to the LLM.
- [x] **The ReAct Pattern**: Implementing the "Reasoning + Acting" loop manually in LangGraph.

### Phase 4: Architectural Refactoring
*Focus: Organizing code like a pro (mimicking `whatsapp-agent-course`).*
- [x] **Modularization**: Split `main.py` into `state.py`, `nodes.py`, `edges.py`, `graph.py`.
- [x] **Configuration**: Managing environment variables and settings properly.

### Phase 5: Memory & Persistence
*Focus: Remembering things.*
- [ ] **Short-term Memory**: Using `MemorySaver` to persist state across turns in a conversation.
- [ ] **Long-term Memory**: Introduction to Vector DBs (Qdrant) for retrieving relevant documents.

### Phase 6: Django & Database Integration
*Focus: Connecting to your specific business logic.*
- [ ] **Django Setup**: Create a minimal Django app with a simple model.
- [ ] **ORM Tools**: Create tools that wrap Django ORM calls (e.g., `create_user`, `query_orders`).
- [ ] **Safety**: Implementing read-only vs. write permissions.

### Phase 7: The Interface (WhatsApp)
*Focus: Talking to the world.*
- [ ] **API Setup**: WhatsApp Business API basics.
- [ ] **Webhook Handler**: Connecting incoming messages to the LangGraph `invoke`.
- [ ] **Async Handling**: Handling long-running agent tasks without timing out WhatsApp.

## 🛠️ Immediate Next Steps
1.  Experiment with **Conditional Edges** in `main.py`.
2.  Add a simple "Router" node that decides where to go next based on input.
