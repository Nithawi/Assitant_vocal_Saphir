import queue
import json
from modules.principal.model import recognizer, q


#|--ecouter--|


def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def ecouter():
    global text
    try:
        data = q.get(timeout=2)
    except queue.Empty:
        print("micro desactivé")
        return ""
    
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)["text"]
        if text:
            print(f"Vous avez dit: {text}")
            return text
    return ""