from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from src.config import SYSTEM_PROMPT
from src.agent.state import State
from src.agent.tools import tools

def chatbot(state: State):
    llm = ChatGroq(model="llama-3.3-70b-versatile").bind_tools(tools)
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm.invoke(messages)]}
