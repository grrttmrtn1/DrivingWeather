import config_loader
import weather
import datetime

#to DO
#code temperature check and wind check
#test running in a container
#setup to run with a systemd timer
_summary = ""
_decision = ""

def checkTemperatures(data):
    try:
        global _summary
        minTemp = config_loader.get_minTemp()
        if not data.get('temperature_max') >= minTemp:
            print(f"Forecasted high temperature is under your minimum: {minTemp} at {data.get('temperature_max')}")
            _summary = createString(_summary, f"Forecasted high temperature is under your minimum: {minTemp} at {data.get('temperature_max')}")
            return False
        else:
            if config_loader.get_maxTemp():
                if config_loader.get_maxTemp() <= data.get('temperature_max'):
                    print(f"Forecasted temperature is above your minimum: {minTemp} and under your maximum: {config_loader.get_maxTemp()} raising to {data.get('temperature_max')}")
                    _summary = createString(_summary, f"Forecasted temperature is above your minimum: {minTemp} and under your maximum: {config_loader.get_maxTemp()} raising to {data.get('temperature_max')}")
                    return True
            print(f"Forcasted temperature is above your minimum: {minTemp} at {data.get('temperature_max')}")
            _summary = createString(_summary, f"Forcasted temperature is above your minimum: {minTemp} at {data.get('temperature_max')}")
            return True
    except Exception as e:
        print(e)

def checkWind(data):
    try:
        global _summary
        maxWind = config_loader.get_maxWind()
        if not maxWind:
            return True
        if data.get('wind').get('speed') > maxWind or data.get('wind').get('gusts') > maxWind:
            _summary = createString(_summary, f"Forcasted wind is above your maximum: {maxWind}mph at {data.get('wind').get('speed')}mph")
            return False
        return True
    except Exception as e:
        print(e)

def checkRain(data):
    try:
        global _summary
        if not config_loader.get_watchRainEnabled():
            return True
        if data.get('precipitation') != "none":
            if data.get('probability').get('precipitation') >= config_loader.get_PercentRaInProbabilityAcceptance():
                _summary = createString(_summary, f"Forcasted precipitation is above your minimum likelihood: {config_loader.get_PercentRaInProbabilityAcceptance()}% at {data.get('probability').get('precipitation')}%")
                return False
            return True
        return True
    except Exception as e:
        print(e)

def AcceptableLimits(data):
    try:
        if not checkTemperatures(data):
            return False
        if not checkWind(data):
            return False
        if not checkRain(data):
            return False

        return True
    except Exception as e:
        print(e)
        return False

def createString(variable, message):
    if variable:
        variable += f"\n{message}"
    else: 
        variable += message
    return variable

def main():
    try:
        global _decision
        global _summary
        if not config_loader.validate_config():
            raise('Configuration could not be validated.')
        if not config_loader.get_minTemp():
            raise("Ensure that a minimum temperature is set in your config")
        weatherData = weather.get_weatherData()
        dailyWeather = weatherData.get('daily', False).get('data', False)
        if not dailyWeather:
            raise('Weather data returned in the api response')
        today = today = datetime.date.isoformat(datetime.date.today())
        if dailyWeather:
            if not dailyWeather[0].get('day') == today:
                day = dailyWeather[0].get('day')
                raise(f"the first index returned does not match today's date: {today} and returned: {day}")
            todaysWeather = dailyWeather[0]
            _summary = createString(_summary, 'Todays Weather:')
            if AcceptableLimits(todaysWeather):
                _decision = createString(_decision, 'Good weather to drive today.')
            else:
                _decision = createString(_decision, 'Weather is not looking good today.')
            if config_loader.get_tomorrowsForecast():
                tomorrow = datetime.date.isoformat(datetime.date.today() + datetime.timedelta(days=1))
                if not dailyWeather[1].get('day') == tomorrow:
                    day = dailyWeather[1].get('day')
                    raise(f"Tomorrows forecast set in config. The second index returned does not match tomorrow's date: {tomorrow} and returned: {day}")
                tomorrowsWeather = dailyWeather[1]
                #tomorrowsTempCheck = checkTemperatures(tomorrowsWeather)
                _summary = createString(_summary, 'Tomorrows Weather:')
                if AcceptableLimits(tomorrowsWeather):
                    _decision = createString(_decision, 'Good weather to drive tomorrow.')
                else:
                    _decision = createString(_decision, 'Weather is not looking good tomorrow.')
        print(dailyWeather)
        print(_decision)
        print(_summary)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()