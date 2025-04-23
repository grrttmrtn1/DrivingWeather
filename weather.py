import requests
import config_loader


def get_weatherData():
    headers = {
        'x-rapidapi-key': config_loader.get_apiKey(),
        'x-rapidapi-host': config_loader.get_baseURL()
    }
    try: 
        r = requests.get(f"https://{config_loader.get_baseURL()}/daily?place_id=appleton&language=en&units=auto", headers=headers)
        if r.status_code != 200:
            r.raise_for_status()
        return r.json()
    except Exception as e:
        print(e)

get_weatherData()