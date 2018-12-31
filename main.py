from configparser import ConfigParser
import requests
import sys
import time


PORCH_LIGHT = 4
MINUTE = 60
HOUR = 60 * MINUTE


def main():
    config = ConfigParser()
    if len(sys.argv) == 2:
        config.read(sys.argv[1])
    else:
        # Use the default
        config.read('config.ini')

    hue = config['HUE']
    username = hue['username']
    hue_ip = hue['ip']

    weather = config['WEATHER']
    weather_api_key = weather['api_key']
    city_id = weather['city_id']

    light_on = False
    sundown = get_sundown(weather_api_key, city_id)
    while True:
        if light_on:
            if time.localtime(time.time()).tm_hour >= 22:
                turn_off_light(hue_ip, username, PORCH_LIGHT)
                light_on = False
                # It's 10PM, might as well sleep until 2PM tomorrow
                time.sleep(16 * HOUR)
                # By the time this executes, it's the next day
                sundown = get_sundown(weather_api_key, city_id)
            else:
                # Waiting for 10PM
                time.sleep(5 * MINUTE)
        else:
            if time.time() >= sundown:
                turn_on_light(hue_ip, username, PORCH_LIGHT)
                light_on = True
            else:
                # Waiting for sundown
                time.sleep(5 * MINUTE)


def turn_on_light(ip, username, light_no):
    req = "http://{}/api/{}/lights/{}/state".format(ip, username, light_no)
    body = "{\"on\":true}"
    res = requests.put(req, data=body)


def turn_off_light(ip, username, light_no):
    req = "http://{}/api/{}/lights/{}/state".format(ip, username, light_no)
    body = "{\"on\":false}"
    res = requests.put(req, data=body)


def get_sundown(key, city):
    api_string = _build_url(key, city)
    res = requests.get(api_string)
    weather_info = res.json()
    return weather_info['sys']['sunset']


def _build_url(key, city):
    city_id = "id={}".format(city)
    app_id = "APPID={}".format(key)
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    return "{}?{}&{}".format(base_url, city_id, app_id)


if __name__ == "__main__":
    main()
