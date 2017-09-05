#!/usr/bin/env python
import urllib2
import sys
import os
import json
import evdev

# Modify your variable here
roomname = "Arbeitszimmer" # roomname your Sonos Speaker is located
buttonname = "Satechi Media Button" # also tested with "BT-005"
host = "localhost" # when installed on the same host use localhost
port = "5005" #default 5005
key2commandPairs = {"KEY_PLAYPAUSE":"playpause",
                    "KEY_NEXTSONG":"next",
                    "KEY_PREVIOUSSONG":"previous",
                    "KEY_VOLUMEUP":"volume/+2",
                    "KEY_VOLUMEDOWN":"volume/-2"}
# ---------------------------------------------------------------------


def evaluateResponse(response):
    result = u'\u2717'.encode('utf8')
    j = json.loads(response)

    if j["status"] == "success":
        result = u'\u2713'.encode('utf8')
    return result

print "Script started. Searching for " + buttonname + "..."
try:
    while True:
            devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
            if len(devices) == 0:
                print("No devices found, try running with sudo")
                sys.exit(1)

            for device in devices:
                if device.name == buttonname:
                    print("Button found: " + str(device))
                    url = "http://" + host + ":" + port + "/"+ roomname
                    try:
                        device.grab()
                        for event in device.read_loop():
                            if event.type == evdev.ecodes.EV_KEY:
                                 data = evdev.categorize(event)  # Save the event temporarily to introspect it
                                 if data.keystate == 1:  # Down events only
                                    if data.keycode in key2commandPairs:
                                        print "Received event " + data.keycode + " -> Sending command " + key2commandPairs[data.keycode],
                                        response = urllib2.urlopen(url + "/" + key2commandPairs[data.keycode]).read()
                                        print  evaluateResponse(response)
                                    else:
                                        print u'You Pressed the {} key!'.format(data.keycode)  # Print it all out!
                    except Exception, e:
                        print e
                        print("Lost connection! Start searching...")
                        pass
                else:
                    pass
except KeyboardInterrupt:
    print 'Exited'
    try:
        sys.exit(1)
    except SystemExit:
        os._exit(0)
