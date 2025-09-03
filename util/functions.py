from dotenv import load_dotenv
import threading
import traceback
import json
import os

load_dotenv()
lock=threading.Lock()

def check_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w') as file:
            file.write("{}")

def loadJSON(filename):
    try:
        with lock:
            check_file(f"json/{filename}.json")
            with open(f"json/{filename}.json", 'r') as file:
                return json.load(file)
    except FileNotFoundError:
        print(f'File {filename} not found.')
        return {}
    except json.JSONDecodeError:
        print(f'Error decoding JSON from {filename}.')
        return {}

def saveJSON(data, filename):
    try:
        with lock:
            check_file(f"json/{filename}.json")
            with open(f"json/{filename}.json", 'w') as file:
                json.dump(data, file, indent=4)
    except Exception as e:
        print("An error occurred:", traceback.format_exc())
