import asyncio

import mavsdk.core
from mavsdk import System
#mavsdk_server_address = "serial:///dev/ttyACM0:115200"

async def run():
    # connect to the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # get the list of parameters
    all_params = await drone.param.get_all_params()

    # iterate through all int parameters
    for param in all_params.int_params:
        print(f"{param.name}: {param.value}")

    for param in all_params.float_params:
        print(f"{param.name}: {param.value}")





asyncio.run(run())

