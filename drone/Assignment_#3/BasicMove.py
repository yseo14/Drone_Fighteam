from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.takeoff()
drone.send_rc_control(0, 50, 0, 0)
sleep(2)
drone.send_rc_control(-30, 50, 0, 0)
sleep(2)
drone.send_rc_control(0, 50, 0, 30)
sleep(2)
drone.send_rc_control(0, 50, 0, 0)
sleep(2)
drone.land()
