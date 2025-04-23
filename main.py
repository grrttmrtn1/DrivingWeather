import config_loader
import weather

#to DO
#code temperature check and wind check
#test running in a container
#setup to run with a systemd timer

def main():
    try:
        if not config_loader.validate_config:
            raise('Configuration could not be validated.')
        weatherData = weather.get_weatherData()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()