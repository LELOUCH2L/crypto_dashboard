import json
import os

PREF_PATH = os.path.join(os.path.dirname(__file__), "preferences.json")

def save_preference(key, value):
    data = {}
    if os.path.exists(PREF_PATH):
        with open(PREF_PATH, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    data[key] = value
    with open(PREF_PATH, "w") as f:
        json.dump(data, f)

def load_preference(key, default=None):
    if os.path.exists(PREF_PATH):
        with open(PREF_PATH, "r") as f:
            try:
                data = json.load(f)
                return data.get(key, default)
            except:
                return default
    return default
