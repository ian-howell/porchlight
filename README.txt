# Instructions for future self in case of catastrophic failure

### Using hue api (since their website is frequently down)

* You're going to need the Hue bridge's ip address. This can be found in either
your router's DHCP settings or by looking through the settings of the Hue app.
* You may need to set up a user for the hue bridge:
    1. Go to http://<bridge_api>/debug/clip.html
    2. In the URL box, just use `/api`
    3. In the Message body, use something like `{"devicetype":"namespace#name"}`
    4. Press the big link button on the bridge, then click the `POST` button.
    5. This will return a username. Save that for later.
* To access lights, use `http://<bridge_ip>/api/<username>/lights`
* To access groups, use `http://<bridge_ip>/api/<username>/group`
* To turn a light/group on or off, use PUT with `http://<bridge_ip>/api/<username>/lights/state` with a body that looks something like `{"on":true}`
    * Note that the Python Requests library can take a string as the payload

### Creating a runnable service

* Paste the following into /etc/systemd/system/porchlight.service:
```
[Unit]
Description=Schedules when to turn the porch light on or off
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=<user>
ExecStart=<path_to_python3> <path_to_main.py> <path_to_config.ini>

[Install]
WantedBy=multi-user.target
```
* Run `sudo systemctl start porchlight` to start the service
* Run `sudo systemctl enable porchlight` to make the service run in the background on startup
