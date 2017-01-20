# auto-lights
This is a simple python script that endevours to turn on Hue lights automatically when a person enters a room.

# Setup
I have this running on a raspberry pi with an old webcam I had lying around. 

1. Download the repo and install the required libraries. 
2. Change the config file to match your: userId, light id, and light bridge ip address. [Here is a link to Hue's Documentation](https://developers.meethue.com/documentation/getting-started). 
3. Set the camera somewhere where it can see all or most of the room. 
4. Run "auto-lights.py" 
At this point everything should be working fine

# Changing the config file
There are two other config file options that you might want to change.

## minArea
The way this program works is to check for any movement in front of the camera. This setting changes how big the movement must be to actually cause the light to turn on. You may have to play with it to get it working for the best for you.

## idleTime
Sometimes when you are in a room you want the lights to be off. In order to accomplish this the script checks how long there has been movement, before turning the lights back on. If less than the idleTime has elapsed since the last movement it will not turn the lights back on. The units are in seconds.
