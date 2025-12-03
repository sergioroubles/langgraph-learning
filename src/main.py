import os
import json
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Check for API Key
if not os.getenv("GROQ_API_KEY"):
    print("Error: GROQ_API_KEY not found in environment variables.")
    print("Please create a .env file with GROQ_API_KEY=your_key_here")



from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

# Define the System Prompt
SYSTEM_PROMPT = """You are a helpful assistant named 'Ava'.
You are concise, professional, and friendly.
You ALWAYS answer in Spanish, unless explicitly asked to speak another language.

CRITICAL INSTRUCTION:
If the user's input is hostile, angry, or rude (sentiment is negative), your answer MUST be exactly:
"Lo siento, no puedo ayudarte con eso. Por favor contacta a soporte@ejemplo.com."
Do not add anything else.
"""

class State(TypedDict):
    # The 'add_messages' reducer ensures that when a node returns a message,
    # it is APPENDED to this list, rather than overwriting it.
    messages: Annotated[list, add_messages]
    current_sentiment: str

# Define the structure we want the LLM to return
class BotResponse(BaseModel):
    answer: str = Field(description="The response to the user")


class SentimentResponse(BaseModel):
    sentiment: str = Field(description="The sentiment of the user's input (positive, neutral, negative, very negative)")

def sentiment_analyzer(state: State):
    # Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    # Bind the structured output schema
    structured_llm = llm.with_structured_output(SentimentResponse)
    
    # Prepend the System Message
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    
    # Invoke the LLM
    response_object = structured_llm.invoke(messages)
    
    # Return both the message AND the sentiment to the state
    return {
        "current_sentiment": response_object.sentiment
    }

def chatbot(state: State):
    # Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    # Prepend the System Message
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    
    # Invoke the LLM
    response_object = llm.invoke(messages)
    
    # Return both the messages
    return {
        "messages": [("ai", response_object.content)],
    }

def escalate_to_human(state: State):
    return {
        "messages": [("human", "Escalando a un humano...")],
    }

def save_state_to_json(state, filename="state.json"):
    """Helper to save the state to a JSON file for inspection."""
    data = {}
    for key, value in state.items():
        if key == "messages":
            # Convert Message objects to dicts for readability
            data[key] = []
            for msg in value:
                if hasattr(msg, "model_dump"):
                    msg_dict = msg.model_dump()
                elif hasattr(msg, "dict"):
                    msg_dict = msg.dict()
                else:
                    msg_dict = str(msg)
                data[key].append(msg_dict)
        else:
            data[key] = value
            
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f" [State saved to {filename}]")

def main():
    print("Initializing LangGraph Chatbot...")

    # Initialize MemorySaver for persistence
    memory = MemorySaver()

    graph_builder = StateGraph(State)
    
    # Add the single LLM node
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("sentiment_analyzer", sentiment_analyzer)
    graph_builder.add_node("escalate_to_human", escalate_to_human)

    
    # Set entry point
    graph_builder.set_entry_point("sentiment_analyzer")

    # add conditional edge
    graph_builder.add_conditional_edges(
        "sentiment_analyzer",
        [
            (lambda state: state["current_sentiment"] == "very negative", "escalate_to_human"),
            (lambda state: state["current_sentiment"] == "negative", "chatbot"),
            (lambda state: state["current_sentiment"] == "neutral", "chatbot"),
            (lambda state: state["current_sentiment"] == "positive", "chatbot"),
        ]
    )
    
    # Add edge to END
    graph_builder.add_edge("sentiment_analyzer", END)
    graph_builder.add_edge("escalate_to_human", END)
    
    # Compile with checkpointer
    graph = graph_builder.compile(checkpointer=memory)

    # Config defines the "Thread" - a unique ID for this conversation
    config = {"configurable": {"thread_id": "1"}}

    print("Chatbot started! Type 'quit', 'exit', or 'q' to stop.")
    
    while True:
        try:
            user_input = input("\nYou: ")
        except EOFError:
            break
            
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
            
        # Run the graph with the new message
        print(f"\n>>> Running...")
        result = graph.invoke({"messages": [("user", user_input)]}, config=config)
        
        # Save the evolving state to a file
        save_state_to_json(result)
        
        last_message = result["messages"][-1]
        sentiment = result.get("current_sentiment", "neutral")
        
        print(f"AI: {last_message.content} [Sentiment: {sentiment}]")
        
        # TERMINATE if negative
        if sentiment == "negative":
            print("\n!!! CONVERSATION TERMINATED DUE TO HOSTILITY !!!")
            print("Please contact support.")
            break

if __name__ == "__main__":
    main()
