import asyncio

import mavsdk.offboard
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    drone_status_task = asyncio.ensure_future(print_status_function(drone))
    print("connecting to drone...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("connection established")
            break
    print("waiting fo"
          "r drone to a global location estimate")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print(f"global position ok: {health.is_global_position_ok} \n home position ok: {health.is_home_position_ok}")
            break

    print("getting ready for arming")
    await drone.action.arm()
    print(f"drone armed: {drone.telemetry.armed()}")

    alt = int(input("requested altitude: "))

    print(f"taking off to {alt}m")
    await drone.action.set_takeoff_altitude(alt)
    await drone.action.takeoff()

    async for pos in drone.telemetry.position():
        print(f"altitude: {round(pos.relative_altitude_m, 1)}")
        if round(pos.relative_altitude_m, 1) > alt - 0.2:
            await drone.action.hold()
            #await asyncio.sleep(10)
            break


    await drone.action.land()

    #await asyncio.sleep(10)

    #print("landing")
    #await drone.action.land()



async def print_status_function(vehicle):
    try:
        async for msg in vehicle.telemetry.status_text():
            print(f"status: {msg.type}: {msg.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())