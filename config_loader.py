import configparser
import os

_config = None

def load_config(path='/home/gmartin/dev/OkToDrive/config.ini'):
    global _config
    if _config is None:
        _config = configparser.ConfigParser()
        _config.read(path)
    return _config

def validate_config(path='/home/gmartin/dev/OkToDrive/config.ini') -> bool:
    if not os.path.exists(path):
        print(f"Config file not found at: {path}")
        return False
    try:
        parser = configparser.ConfigParser()
        parser.read(path)
        if not parser.sections():
            print(f"Config file at {path} is empty or improperly formatted.")
            return False
        return True
    except configparser.Error as e:
        print(f"Failed to parse config file: {e}")
        return False


def _get(section, key):
    config = load_config()
    if not config.has_section(section):
        return False
    if not config.has_option(section, key):
        return False
    return True


def get_minTemp():
    if _get('app', 'MinTemp'):
        return load_config().getint('app', 'MinTemp')
    return False

def get_maxTemp():
    if _get('app', 'MaxTemp'):
        return load_config().getint('app', 'MaxTemp')
    return False

def get_maxWind():
    if _get('app', 'MaxWind'):
        return load_config().getint('app', 'MaxWind')
    return False

def get_tomorrowsForecast():
    if _get('app', 'IncludeTomorrowsForecast'):
        return load_config().getboolean('app', 'IncludeTomorrowsForecast')
    return False
    
def get_watchRainEnabled():
    if _get('app', 'WatchRain'):
        return load_config().getboolean('app', 'WatchRain')
    return False

def get_PercentRaInProbabilityAcceptance():
    if _get('app', 'PercentRaInProbabilityAcceptance'):
        return load_config().getboolean('app', 'PercentRaInProbabilityAcceptance')
    return False
    
def get_apiKey():
    if _get('app', 'ApiKey'):
        return load_config().get('app', 'ApiKey')
    return False
    
def get_baseURL():
    if _get('app', 'BaseURL'):
        return load_config().get('app', 'BaseURL')
    return False


