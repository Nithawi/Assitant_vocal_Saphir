import asyncio
import os
import edge_tts
from playsound3 import playsound

# Fonction pour faire parler l'assistant

def dire(phrase):
    asyncio.run(parler(phrase))

async def parler(phrase):
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")
    communicate = edge_tts.Communicate(phrase, voice = "fr-CH-ArianeNeural")
    await communicate.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")



