import requests
import sys
from configparser import ConfigParser


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
