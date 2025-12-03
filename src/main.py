from src.agent.graph import graph
from src.agent.utils import save_state_to_json

print("Bot started. Type 'q' to quit.")
while True:
    user_input = input("You: ")
    if user_input == "q": break
    
    config = {"configurable": {"thread_id": "1"}}
    for event in graph.stream({"messages": [("user", user_input)]}, config=config, stream_mode="updates"):
        for node, update in event.items():
            print(f"--- Node: {node} ---")
            last_msg = update["messages"][-1]
            print(f"AI: {last_msg.content}")
            print("-" * 20)
    
    # Save state after each turn
    snapshot = graph.get_state(config)
    save_state_to_json(snapshot.values)
