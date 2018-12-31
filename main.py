import sys
from configparser import ConfigParser


def main():
    config = ConfigParser()
    if len(sys.argv) == 2:
        config.read(sys.argv[1])
    else:
        # Use the default
        config.read('config.ini')

    api = config['API']
    username = api['username']
    hue_ip = api['hue_ip']


if __name__ == "__main__":
    main()
