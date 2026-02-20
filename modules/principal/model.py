from vosk import Model, KaldiRecognizer
import queue

SAMPLE_RATE = 16000
MODEL_PATH = "vosk-model-small-fr-0.22"  # Path to the Vosk model directory
q = queue.Queue()
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)



