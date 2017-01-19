import cv2
import imutils
import time
import requests
import json


# Functions

def turnOnLights():
  # Turns on the light in "config.json"
  print("Turning on lights...")
  payload = json.dumps({'on': True})
  response = requests.put("http://" + configs["lightBridgeIp"] + 
                          "/api/" + configs["userId"] + 
                          "/lights/" + configs["light"] + "/state", 
                          data = payload)

def getLightStatus():
  # Gets the current status of the light
  light_status_response = requests.get("http://" + configs["lightBridgeIp"] + 
                                      "/api/" + configs["userId"] + 
                                      "/lights/" + configs["light"])
  light_status_json = json.loads(light_status_response.text)
  return light_status_json["state"]["on"]


# Getting configs
with open("config.json") as config_file:
  configs = json.load(config_file)

# Set up camera
cam=cv2.VideoCapture(0)

firstFrame = None
lastLightsOn = False
lightsOn = False

# Run forever
while True:
  lastLightsOn = lightsOn
  lightsOn = getLightStatus()
  
  # reset frame if lights turned off
  if not lightsOn and lastLightsOn:
    print("Reseting frame...")
    firstFrame = None
    for i in range(30):
      cam.read()

  # only do image processing if lights are off
  if not lightsOn:
    print("Looking for movement...")
    (grabbed, frame) = cam.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Load firstFrame if there is none
    if firstFrame == None:
      firstFrame = gray
      continue

    delta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
      if cv2.contourArea(c) >= configs["minArea"]:
        turnOnLights()

  else:
    print("Light is on...")
    time.sleep(1)

cam.release()
