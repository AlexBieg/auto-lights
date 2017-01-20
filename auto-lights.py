import cv2
import imutils
import time
import requests
import json


# Global Vars
firstFrame = None
lastLightsOn = False
lightsOn = False
lastMovementTime = 0
cam=cv2.VideoCapture(0)
with open("config.json") as config_file:
  configs = json.load(config_file)


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

  secSinceMove = int(time.time()) - lastMovementTime

  for c in cnts:
    if cv2.contourArea(c) >= configs["minArea"]:
      if not lightsOn and (secSinceMove > configs["idleTime"]):
        turnOnLights()
      print("Reseting last movement time...")
      lastMovementTime = int(time.time())


cam.release()
