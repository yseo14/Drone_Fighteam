from djitellopy import TelloSwarm, Tello

swarm = TelloSwarm.fromIps([
    "192.168.1.101",  # 첫 번째 드론의 IP 주소
    "192.168.1.103"  # 두 번째 드론의 IP 주소
])

swarm.connect()

def takeoff_land(i, drone):
    drone.takeoff()

    drone.enable_mission_pads()
    drone.set_mission_pad_detection_direction(2)

    drone.move_down(60)
    swarm.sync()
    pad = drone.get_mission_pad_id()

    while 1:

        if pad != -1:
            drone.move_forward(70)
            drone.rotate_counter_clockwise(90)

        print(pad)
        pad = drone.get_mission_pad_id()

    drone.land()


swarm.parallel(takeoff_land)

swarm.end()