from djitellopy import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.1.101",
    "192.168.1.103"
])

swarm.connect()
swarm.takeoff()

# run in parallel on all tellos
swarm.move_up(100)

# run by one tello after the other
swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

swarm.land()
swarm.end()