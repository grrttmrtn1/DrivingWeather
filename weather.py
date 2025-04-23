import requests
import config_loader


def get_weatherData():
    try:
        if not config_loader.get_apiKey() or not config_loader.get_baseURL():
            raise("Ensure both API Key and Base URL are set in your config")
        headers = {
        'x-rapidapi-key': config_loader.get_apiKey(),
        'x-rapidapi-host': config_loader.get_baseURL()
        }
        r = requests.get(f"https://{config_loader.get_baseURL()}/daily?place_id=appleton&language=en&units=auto", headers=headers)
        if r.status_code != 200:
            r.raise_for_status()
        return r.json()
    except Exception as e:
        print(e)