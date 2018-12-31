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


if __name__ == "__main__":
    main()
