import threading
import time

from djitellopy import tello
from time import sleep
import cv2

drone = tello.Tello()
drone.connect()

keepRecording = True
drone.streamon()
frame_read = drone.get_frame_read()
time.sleep(10)

def videoRecorder():
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    while keepRecording:
        video.write(cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB))
        time.sleep(1 / 30)

    video.release()


recorder = threading.Thread(target=videoRecorder)
recorder.start()

drone.takeoff()
drone.move_up(100)
drone.rotate_counter_clockwise(360)
drone.land()

keepRecording = False
recorder.join()
