import json

def save_state_to_json(state, filename="state.json"):
    data = {}
    for key, value in state.items():
        if key == "messages":
            data[key] = []
            for msg in value:
                if hasattr(msg, "model_dump"): msg_dict = msg.model_dump()
                elif hasattr(msg, "dict"): msg_dict = msg.dict()
                else: msg_dict = str(msg)
                data[key].append(msg_dict)
        else:
            data[key] = value
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
