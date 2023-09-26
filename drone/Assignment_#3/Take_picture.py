from djitellopy import tello
import cv2
from time import sleep

drone = tello.Tello()
drone.connect()

drone.streamon()

frame_read = drone.get_frame_read()

drone.takeoff()

a = frame_read.frame

a = cv2.cvtColor(a,cv2.COLOR_BGR2RGB)

cv2.imwrite("Picture2.png", a)

drone.land()
