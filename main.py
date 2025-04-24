import config_loader
import weather
import datetime

#to DO
#code temperature check and wind check
#test running in a container
#setup to run with a systemd timer

def main():
    try:
        if not config_loader.validate_config():
            raise('Configuration could not be validated.')
        if not config_loader.get_minTemp():
            raise("Ensure that a minimum temperature is set in your config")
        minTemp = config_loader.get_minTemp()
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
            if config_loader.get_tomorrowsForecast():
                tomorrow = datetime.date.isoformat(datetime.date.today() + datetime.timedelta(days=1))
                if not dailyWeather[1].get('day') == tomorrow:
                    day = dailyWeather[1].get('day')
                    raise(f"Tomorrows forecast set in config. The second index returned does not match tomorrow's date: {tomorrow} and returned: {day}")
                tomorrowsWeather = dailyWeather[1]
            if not todaysWeather.get('temperature_min') >= minTemp:
                temperature = f"Temperature is under your minimum: {minTemp} at {todaysWeather.get('temperature_min')}"
            else:
                if config_loader.get_maxTemp():
                    if config_loader.get_maxTemp() <= todaysWeather.get('temperature_max'):
                        temperature = f"Temperature is above your minimum: {minTemp} and under your maximum: {config_loader.get_maxTemp()} raising to {todaysWeather.get('temperature_max')}"
                temperature = f"Temperature is above your minimum: {minTemp} at {todaysWeather.get('temperature_min')}"
            print(temperature)


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()