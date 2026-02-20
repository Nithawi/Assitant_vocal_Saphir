import requests
import geocoder
from modules.principal.parler import dire

api_key = "4ba8aec33cf763837edd9a5b0d362aac"
ville = "Paris"

def get_ville():
    # Récupère la localisation via l'IP
    g = geocoder.ip('me')
    if g.ok:
        return g.city


def meteo():
    ville = get_ville()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&lang=fr"

    reponse = requests.get(url, timeout=5)
    data = reponse.json()
    
    
    description = data['weather'][0]['description']
    temperature = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    dire (f"Le temps à {ville} est actuellement {description} avec une température de {temperature:.1f} degrés Celsius et une humidité de {humidity}%.")
    print(f"Le temps à {ville} est actuellement {description} avec une température de {temperature:.1f} degrés Celsius et une humidité de {humidity}%.")
    



