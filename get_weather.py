from time import sleep 
from colorama import init, Fore, Style # for colors on output
from datetime import datetime # for output hours and minutes
import configparser # for reading config file
import pytz # for timezone
import requests # for requesting data from api

# Run the program one time to create a config file
# This program will get the weather from the openweathermap.org API
# I don't guarantee that the API will work forever
# last update: 2022-04-11
# requirements: requests, configparser, colorama, datetime
# run: python3 main.py
# this program does not work with python2
# author: Blu

init(autoreset = True) # init colorama and reset the colors after each print

try: # if is there no config.ini file this will create a new one
    create_config_file = open("config.ini", "x") # create a config.ini file
    create_config_file.write("[API_KEY]\n# Insert your API key from openweathermap.org\n# note: Don't use quotes\napi_key = 1234\n\n[PREFERRED_TEMP_UNIT]\n# Possible values: 'celsius'(C), 'fahrenheit'(F), 'kelvin'(K)\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (fahrenheit)\npreferred_temp_unit = F\n\n[PREFERRED_CITY]\n# If you insert a city here the program will skip the question of what city you want to search for and will use this value instead\n# note: Don't use quotes\npreferred_city = cityhere\n\n[PREFERRED_VELOCITY_UNIT]\n# Possible values: 'meters/sec'(m/s), 'miles/hour'(mph), 'kilometers/hour'(km/h)\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (mph)\npreferred_velocity_unit = mph\n\n[PREFERRED_HOURS_FORMAT]\n# Possible values: '12h', '24h'\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (24h)\npreferred_hours_format = 24h\n\n[SHOW_WARNINGS]\n# Possible values: on, off\n# This option will turn on or off the warnings of the weather status\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_warnings = on\n\n[SHOW_HUMIDITY]\n# Possible values: on, off\n# This option will turn on or off the humidity\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_humidity = on\n\n[SHOW_PRESSURE]\n# Possible values: on, off\n# This option will turn on or off the pressure\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_pressure = on\n\n[SHOW_CLOUDNESS]\n# Possible values: on, off\n# This option will turn on or off the cloudness\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_cloudness = on\n\n[SHOW_VISIBILITY]\n# Possible values: on, off\n# This option will turn on or off the visibility\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_visibility = on\n\n[SHOW_WIND_SPEED]\n# Possible values: on, off\n# This option will turn on or off the wind speed\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_wind_speed = on\n\n[SHOW_WIND_DIRECTION]\n# Possible values: on, off\n# This option will turn on or off the wind direction\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_wind_direction = on\n\n[SHOW_AIR_QUALITY]\n# Possible values: on, off\n# This option will turn on or off the air quality\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_air_quality = on\n\n[SHOW_UVI]\n# Possible values: on, off\n# This option will turn on or off the uvi\n# note: Don't use quotes\n# note: If you insert a wrong value, the default value will be used in the program execution (on)\nshow_uvi = on\n")
    create_config_file.close()
    print(Fore.CYAN + 'A new config.ini file has been created! Please edit it and run the program again.')
    sleep(5)
    exit()
except FileExistsError: # if there is a config.ini file
    pass # do nothing

# read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# reading all settings from the config.ini file
api_key                 = config["API_KEY"]["api_key"]
preferred_temp_unit     = config["PREFERRED_TEMP_UNIT"]["preferred_temp_unit"]
preferred_city          = config["PREFERRED_CITY"]["preferred_city"]
preferred_velocity_unit = config["PREFERRED_VELOCITY_UNIT"]["preferred_velocity_unit"]
preferred_hours_format  = config["PREFERRED_HOURS_FORMAT"]["preferred_hours_format"]
show_warnings           = config["SHOW_WARNINGS"]["show_warnings"]
show_humidity           = config["SHOW_HUMIDITY"]["show_humidity"]
show_pressure           = config["SHOW_PRESSURE"]["show_pressure"]
show_cloudness          = config["SHOW_CLOUDNESS"]["show_cloudness"]
show_visibility         = config["SHOW_VISIBILITY"]["show_visibility"]
show_wind_speed         = config["SHOW_WIND_SPEED"]["show_wind_speed"]
show_wind_direction     = config["SHOW_WIND_DIRECTION"]["show_wind_direction"]
show_air_quality        = config["SHOW_AIR_QUALITY"]["show_air_quality"]
show_uvi                = config["SHOW_UVI"]["show_uvi"]

if api_key == '1234' or api_key == '': # check if there is an api key configured
    print(Fore.YELLOW + "API key is not set. Please set it in config.ini")
    sleep(5)
    exit()

# if preferred temp unit is not 1, 2 or 3
if preferred_temp_unit != 'C' and preferred_temp_unit != 'F' and preferred_temp_unit != 'K':
    preferred_temp_unit = 'F' # set preferred temp unit to farenheit

weather_url = f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q=' # Define url with api key

if(preferred_city == ''): # if there is no preferred city
    try:
        city = input('Enter city: ') # ask user to enter city
    except EOFError: # if user presses Ctrl+Z and presses Enter
        exit() # exit the program

else: # if there is a preferred city
    city = preferred_city # set city to preferred city

while(city == '' or city == 'cityhere'): # while there is no city
    try:
        city = input('Enter city: ') # ask user to enter city again
    except EOFError: # if user presses Ctrl+Z and presses Enter
        exit() # exit the program

    url = weather_url + city 

url = weather_url + city # concatenate city to url

json_data = requests.get(url).json() # get json data from url

verify_errors = json_data['cod'] # get possible errors from json data

if(verify_errors == 401): # if api key is not valid
    verify_errors = json_data['message'] # get error message from json data
    print(Fore.RED + '\n' + verify_errors) # print error message
    sleep(5)
    exit()

elif(verify_errors == '404'): # if city is not found. the cod 404 is a string!
    print('\nCity is not found.')
    sleep(5)
    exit()

# collecting all the information we will need from the API
try: # i inserted this try because if you enter a special character in the city, it will crash the program
    latitude          = (json_data['coord']['lat']) # get latitude from json data
    longitude         = (json_data['coord']['lon']) # get longitude from json data
    air_quality_url   = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}' # define url with coordinates for air quality
    uvi_level_url     = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=daily&appid={api_key}' # define url with coordinates for uvi level
    json_data_air     = requests.get(air_quality_url).json() # make a new request to get the air quality data
    json_data_uvi     = requests.get(uvi_level_url).json() # make a new request to get the uv index and the timezone
    air_quality       = (json_data_air['list'][0]['main']['aqi'])
    uvi_level         = (json_data_uvi['current']['uvi'])
    timezone          = (json_data_uvi['timezone'])
    description       = (json_data['weather'][0]['description'])
    humidity          = (json_data['main']['humidity'])
    pressure          = (json_data['main']['pressure'])
    feels_like        = (json_data['main']['feels_like'])
    wind_speed        = (json_data['wind']['speed'])
    wind_deg          = (json_data['wind']['deg'])
    clouds            = (json_data['clouds']['all'])
    visibility        = (json_data['visibility'])
    temp              = (json_data['main']['temp'])
    min_temp          = (json_data['main']['temp_min'])
    max_temp          = (json_data['main']['temp_max'])
except KeyError:
    print("\nPlease don't use special characters in the city name.")
    sleep(5)
    exit()

# converting wind speed to other units
wind_speed_mph = (wind_speed * 2.23694) # convert wind speed to mph
wind_speed_kmh = (wind_speed * 3.6) # convert wind speed to kmh

# getting the timezone from the API
city_timezone = pytz.timezone(timezone) # insert timezone from city to pytz
current_city_hours = datetime.now(city_timezone) # convert timezone to city hours

def kelvin_to_celsius(*args): # function to convert kelvin to celsius
    output_converted_temp = [] # create empty list
    for arg in args: # for each argument in the list
        output_converted_temp.append(arg - 273.15) # add the argument to the list
    return output_converted_temp # return the list

def kelvin_to_farenheit(*args): # function to convert kelvin to farenheit
    output_converted_temp = []
    for arg in args:
        output_converted_temp.append(arg * 9/5 - 459.67)
    return output_converted_temp

def output_temperatures(temp, min_temp, max_temp, feels_like, temp_unit): # function to output temperatures
    print(f'\nTemp: {int(temp)}°{temp_unit}') # print temperature
    print(f'Min temp: {int(min_temp)}°{temp_unit}') # print min temperature
    print(f'Max temp: {int(max_temp)}°{temp_unit}') # print max temperature
    print(f'Feels like: {int(feels_like)}°{temp_unit}') # print feels like temperature

def hello_context(): # function to say hello to the user
    current_time = datetime.now().hour # get current pc time
    if current_time >= 0 and current_time < 12: # if current time is between 0 and 12
        return(Style.BRIGHT + Fore.LIGHTYELLOW_EX + '\nGood morning,' + Style.RESET_ALL) # say good morning and color it yellow
    elif current_time >= 12 and current_time < 18:
        return(Style.NORMAL + Fore.YELLOW + '\nGood afternoon,' + Style.RESET_ALL)
    elif current_time >= 18 and current_time < 24:
        return(Style.DIM + Fore.CYAN + '\nGood evening,' + Style.RESET_ALL)

def hours_format_user_choice(): # function to change hours format
    if(preferred_hours_format == '24h'): # if user wants 24h format
        return current_city_hours.strftime('%H:%M') + ' hours' # return 24h format
    elif(preferred_hours_format == '12h'):
        return current_city_hours.strftime('%I:%M %p') # return 12h format
    else:
        return current_city_hours.strftime('%H:%M') + ' hours' # return 24h format

def warning_enable_disable(): # function to enable or disable warnings
    if(show_warnings == 'on'):
        return(1)
    elif(show_warnings == 'off'):
        return(0)
    else:
        return(1)

def show_humidity_enable_disable(): # function to enable or disable humidity
    if(show_humidity == 'on'):
        return(1)
    elif(show_humidity == 'off'):
        return(0)
    else:
        return(1)

def show_pressure_enable_disable(): # function to enable or disable pressure
    if(show_pressure == 'on'):
        return(1)
    elif(show_pressure == 'off'):
        return(0)
    else:
        return(1)

def show_cloudness_enable_disable(): # function to enable or disable cloudiness
    if(show_cloudness == 'on'):
        return(1)
    elif(show_cloudness == 'off'):
        return(0)
    else:
        return(1)

def show_visibility_enable_disable(): # function to enable or disable visibility
    if(show_visibility == 'on'):
        return(1)
    elif(show_visibility == 'off'):
        return(0)
    else:
        return(1)

def show_wind_speed_enable_disable(): # function to enable or disable wind
    if(show_wind_speed == 'on'):
        return(1)
    elif(show_wind_speed == 'off'):
        return(0)
    else:
        return(1)

def show_wind_direction_enable_disable(): # function to enable or disable wind direction
    if(show_wind_direction == 'on'):
        return(1)
    elif(show_wind_direction == 'off'):
        return(0)
    else:
        return(1)

def show_air_quality_enable_disable(): # function to enable or disable air quality
    if(show_air_quality == 'on'):
        return(1)
    elif(show_air_quality == 'off'):
        return(0)
    else:
        return(1)

def show_uvi_enable_disable(): # function to enable or disable uvi
    if(show_uvi == 'on'):
        return(1)
    elif(show_uvi == 'off'):
        return(0)
    else:
        return(1)

# now we will output the hello message based on the time and output the weather information
print(f"{hello_context()} Current weather in {city} is {description}, {hours_format_user_choice()}") # print the weather description with hours on the current city

if(preferred_temp_unit == 'C'): # if user prefers celsius
    temp, min_temp, max_temp, feels_like = kelvin_to_celsius(temp, min_temp, max_temp, feels_like) # convert kelvin to celsius
    output_temperatures(temp, min_temp, max_temp, feels_like, 'C')  # print the weather in celsius

elif(preferred_temp_unit == 'F'): # if user prefers farenheit
    temp, min_temp, max_temp, feels_like = kelvin_to_farenheit(temp, min_temp, max_temp, feels_like)
    output_temperatures(temp, min_temp, max_temp, feels_like, 'F')

elif(preferred_temp_unit == 'K'): # if user prefers kelvin
    # print temp and round to 2 decimal places and print it
    print('\nTemp: ' + str(round(temp, 2)) + ' K')
    print('Min Temp: ' + str(round(min_temp, 2)) + ' K')
    print('Max Temp: ' + str(round(max_temp, 2)) + ' K')
    print('Feels like: ' + str(round(feels_like, 2)) + ' K')

# now we will print the details about the weather

# print humidity and color it according to the humidity
if(show_humidity_enable_disable() == 1): # if user wants to show humidity
    if(humidity <= 30):
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.RED + 'Humidity: ' + str(humidity) + '%' + ' Warning: high probability of fire on forests') # print humidity and warning
        else: # if user doesn't want warnings
            print(Fore.RED + 'Humidity: ' + str(humidity) + '%') # print humidity
    elif(humidity <= 40):
        print(Fore.YELLOW + 'Humidity: ' + str(humidity) + '%')
    elif(humidity <= 50):
        print(Fore.CYAN + 'Humidity: ' + str(humidity) + '%')
    elif(humidity <= 60):
        print(Fore.CYAN + 'Humidity: ' + str(humidity) + '%')
    else:
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.GREEN + 'Humidity: ' + str(humidity) + '%' + ' Warning: high fungus presence')
        else: # if user doesn't want warnings
            print(Fore.GREEN + 'Humidity: ' + str(humidity) + '%')

if(show_pressure_enable_disable() == 1): # if user wants to show pressure
    print('Pressure: ' + str(pressure) + ' hPa') # print pressure

if(show_cloudness_enable_disable() == 1): # if user wants to show cloudiness
    print('Cloudiness: ' + str(clouds) + '%') # print cloudiness

if(show_visibility_enable_disable() == 1): # if user wants to show visibility
    print('Visibility: ' + str(round(visibility, 1) / 1000) + ' km') # convert visibility from m to km

# print wind information and warning if wind is too strong
if(show_wind_speed_enable_disable() == 1): # if user wants to show wind
    if(preferred_velocity_unit == 'km/h'):
        if(wind_speed >= 117.7 or wind_speed >= 74.8 and warning_enable_disable() == 1): # if wind speed is too high
            print(Fore.RED + 'Wind speed: ' + str(round(wind_speed_kmh, 1)) + ' km/h' + ' Warning: high wind speed, possible tornado or strong storm')
        else:
            print('Wind speed: ' + str(round(wind_speed_kmh, 1)) + ' km/h') # print wind speed

    elif(preferred_velocity_unit == 'mph'):
        if(wind_speed_mph >= 73.1 or wind_speed_mph >= 48.5 and warning_enable_disable() == 1): # if wind speed is too high
            print(Fore.RED + 'Wind speed: ' + str(round(wind_speed_mph, 1)) + ' mph' + ' Warning: high wind speed, possible tornado or strong storm')
        else:
            print('Wind speed: ' + str(round(wind_speed_mph, 1)) + ' mph')

    elif(preferred_velocity_unit == 'm/s'):
        if(wind_speed >= 52.6 or wind_speed >= 33.4 and warning_enable_disable() == 1): # if wind speed is too high
            print(Fore.RED + 'Wind speed: ' + str(round(wind_speed, 1)) + ' m/s' + ' Warning: high wind speed, possible tornado or strong storm')
        else:
            print('Wind speed: ' + str(round(wind_speed, 1)) + ' m/s')
    else:
        if(wind_speed_mph >= 73.1 or wind_speed_mph >= 48.5 and warning_enable_disable() == 1): # if wind speed is too high
            print(Fore.RED + 'Wind speed: ' + str(round(wind_speed_mph, 1)) + ' mph' + ' Warning: high wind speed, possible tornado or strong storm')
        else:
            print('Wind speed: ' + str(round(wind_speed_mph, 1)) + ' mph')

# print wind direction in cardinal directions
if(show_wind_direction_enable_disable() == 1): # if user wants to show wind direction
    if(wind_deg <= 11.25 or wind_deg <= 11 or wind_deg >= 348.75 or wind_deg >= 348): # if wind direction is north
        print('Wind direction: N')
    elif(wind_deg <= 33.75 or wind_deg <= 33):
        print('Wind direction: NNE')
    elif(wind_deg <= 56.25 or wind_deg <= 56):
        print('Wind direction: NE')
    elif(wind_deg <= 78.75 or wind_deg <= 78):
        print('Wind direction: ENE')
    elif(wind_deg <= 101.25 or wind_deg <= 101):
        print('Wind direction: E')
    elif(wind_deg <= 123.75 or wind_deg <= 123):
        print('Wind direction: ESE')
    elif(wind_deg <= 146.25 or wind_deg <= 146):
        print('Wind direction: SE')
    elif(wind_deg <= 168.75 or wind_deg <= 168):
        print('Wind direction: SSE')
    elif(wind_deg <= 191.25 or wind_deg <= 191):
        print('Wind direction: S')
    elif(wind_deg <= 213.75 or wind_deg <= 213):
        print('Wind direction: SSW')
    elif(wind_deg <= 236.25 or wind_deg <= 236):
        print('Wind direction: SW')
    elif(wind_deg <= 258.75 or wind_deg <= 258):
        print('Wind direction: WSW')
    elif(wind_deg <= 281.25 or wind_deg <= 281):
        print('Wind direction: W')
    elif(wind_deg <= 303.75 or wind_deg <= 303):
        print('Wind direction: WNW')
    elif(wind_deg <= 326.25 or wind_deg <= 326):
        print('Wind direction: NW')
    elif(wind_deg <= 348.75 or wind_deg <= 348):
        print('Wind direction: NNW')
    else:
        print('Wind direction: N/A')

# print air quality status and color it according to the quality
if(show_air_quality_enable_disable() == 1): # if user wants to show air quality
    if(air_quality <= 1):
        print(Fore.CYAN + 'Air quality: Good')
    elif(air_quality <= 2):
        print(Fore.GREEN + 'Air quality: Fair')
    elif(air_quality <= 3):
        print(Fore.YELLOW + 'Air quality: Moderate')
    elif(air_quality <= 4):
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.RED + 'Air quality: Poor, Warning: Unhealthy for sensitive groups')
        else: # if user doesn't want warnings
            print(Fore.RED + 'Air quality: Poor')
    elif(air_quality <= 5):
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.RED + 'Air quality: Very Poor, Warning: Unhealthy')
        else: # if user doesn't want warnings
            print(Fore.RED + 'Air quality: Very Poor')
    else:
        print('Air quality: Unknown')

# print ultraviolet index and color it according to the index
if(show_uvi_enable_disable() == 1): # if user wants to show ultraviolet index
    if(uvi_level <= 2):
        print(Fore.GREEN + 'UV Index: Low')
    elif(uvi_level <= 5):
        print(Fore.YELLOW + 'UV Index: Moderate')
    elif(uvi_level <= 7):
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.YELLOW + 'UV Index: High, Warning: Caution required')
        else: # if user doesn't want warnings
            print(Fore.YELLOW + 'UV Index: High')
    elif(uvi_level <= 10):
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.RED + 'UV Index: Very High, Warning: Higher risk of harm to the human body')
        else: # if user doesn't want warnings
            print(Fore.RED + 'UV Index: Very High')
    else:
        if(warning_enable_disable() == 1): # if user wants to enable warnings
            print(Fore.RED + 'UV Index: Extreme, Warning: Extreme risk of harm to the human body')
        else: # if user doesn't want warnings
            print(Fore.RED + 'UV Index: Extreme')

