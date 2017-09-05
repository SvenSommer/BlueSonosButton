# BlueSonosButton
This script lets you control you SONOS speakers with a Bluetooth Button.

![Image of a Bluetooth button in front of a sonos speaker]https://github.com/SvenSommer/BlueSonosButton/blob/master/bluetoothSonosButton.jpg?raw=true)

Sending commands from a cheap bluetooth button to a SONOS speaker is achived by using a RaspberryPi. <br> Once the paired bluetooth button sends a command to the Pi, it's forwarded to an HTTP based Api controlling the Sonos Speakers.

## Usage

### 1. Install the script and dependencies

Clone this repository:
````
git clone https://github.com/SvenSommer/BlueSonosButton.git

````

Follow the [installation instructions](http://python-evdev.readthedocs.io/en/latest/install.html#) for your OS to get ``python-evdev``.<br>
I tested it with *Debian* on a *RaspberryPi 3 model B* using:
````
sudo apt-get install python-dev python-pip gcc
sudo apt-get install linux-headers-$(uname -r)
sudo pip install evdev

````

### 2. Install SONOS HTTP API
The magic controlling the sonos speaker is done with by the amazing SONOS HTTP API bridge by *jishi*.<br>
*(If you're interested, you can choose to install the api on a different host.)*

```
git clone https://github.com/jishi/node-sonos-http-api.git
cd node-sonos-http-api
npm install --production
npm start

```

Once the *SONOS API* api is running you should be able to get information about your sonos system by runnig ``http://insertSonosApiHostIp:5005/``

**Important:** Keep the api running!
### 3. Pair your bluetooth button
Pair and connect the bluetooth button with your RaspberryPi:
````
bluetoothctl
agent on
scan on
````
If you have found the button, use the address to trust, pair and connect to it:
````
trust 0C:FC:83:1F:28:6F
pair 0C:FC:83:1F:28:6F
connect 0C:FC:83:1F:28:6F

````
**Important:** Note the name of your button, it's need for the adjustements of the script.


### 4. Configure the script.
Open the and edit ``controlSonos.py`` in the cloned BlueSonosButton folder to your needs. <br>

Global variables are:
```python
# Modify your variable here
roomname = "Kitchen" # roomname your Sonos Speaker is located
buttonname = "Satechi Media Button" # also tested with "BT-005"
host = "localhost" # when installed on the same host use localhost
port = "5005" #default 5005
key2commandPairs = {"KEY_PLAYPAUSE":"playpause",
                    "KEY_NEXTSONG":"next",
                    "KEY_PREVIOUSSONG":"previous",
                    "KEY_VOLUMEUP":"volume/+2",
                    "KEY_VOLUMEDOWN":"volume/-2"}
# -------------------------------------------------

```

In addition you have to configure the buttons and the

### 5. Run the script
1. Make sure the SONOS HTTP API is still running
2. Start the script with ``python controlSonos.py``

If everything is working as exspected you should see something like:
````shell
pi@raspberrypi:~/scripts/BlueSonosButton $ python controlSonos.py
Script started. Searching for Satechi Media Button...
Button found: device /dev/input/event1, name "Satechi Media Button", phys "b8:27:eb:63:ee:5f"
Received event KEY_PLAYPAUSE -> Sending command playpause ✓
Received event KEY_VOLUMEUP -> Sending command volume/+2 ✓
Received event KEY_VOLUMEDOWN -> Sending command volume/-2 ✓
Received event KEY_PREVIOUSSONG -> Sending command previous ✓
Received event KEY_NEXTSONG -> Sending command next ✓
Received event KEY_PLAYPAUSE -> Sending command playpause ✓
````

### 6. (Optional) Buy me a beer ;-)
If you liked my work, please tell me! And I wouldn't say no, if you'd like to buy me a [(virtual) beer](https://www.patreon.com/robhoff).

Further projects I've created are available on my blog [www.robstechlog.com](www.robstechlog.com).
