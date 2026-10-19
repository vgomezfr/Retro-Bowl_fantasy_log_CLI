import os
import json

from rb_terminal import *

################################ Data saving/loading ###############################
def encode(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def decode(data_dict):
    if data_dict.get("__type__") == "Receiver":
        return Receiver.from_dict(data_dict)
    elif data_dict.get("__type__") == "Runningback":
        return Runningback.from_dict(data_dict)
    elif data_dict.get("__type__") == "Quarterback":
            return Quarterback.from_dict(data_dict)
    elif data_dict.get("__type__") == "Player_Season":
        return Player_Season.from_dict(data_dict)
    elif data_dict.get("__type__") == "Receiver_Game":
        return Receiver_Game.from_dict(data_dict)
    elif data_dict.get("__type__") == "Runningback_Game":
        return Runningback_Game.from_dict(data_dict)
    elif data_dict.get("__type__") == "Quarterback_Game":
            return Quarterback_Game.from_dict(data_dict)
    else:
        return data_dict

def load_data() -> dict[str: Player]:
    if os.path.exists(DATA_STORAGE_FILE):
        with open(DATA_STORAGE_FILE, "r") as f:
            return json.load(f, object_hook=decode)
    else:
        return dict()

def save_data(player_dict: dict[str: Player]):
    with open(DATA_STORAGE_FILE, "w") as f:
        json.dump(player_dict, f, default=encode)

def main():
    terminal = Terminal()

    terminal.players = load_data()

    while terminal.action != "E":
        terminal.request_action()
        terminal.perform_action()

    save_data(terminal.players)
    print("All changes saved. \n")

# TODO: Set this to the filename where your player data is stored, or where you want to store it
DATA_STORAGE_FILE = "retro_bowl_data.json"

main()