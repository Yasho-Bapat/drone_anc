import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    status_test_task = asyncio.ensure_future(print_status_function(drone))

    print("connecting to drone")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("connection established")
            break

    print("waiting for drone to have a global location estimate")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("global position estimate ok")
            break

    print("arming motors")
    await drone.action.arm()
    if(drone.telemetry.armed()):
        print("armed")

    print("taking off")
    await drone.action.takeoff()


    #await asyncio.sleep((10))

    async for pos in drone.telemetry.position():
        print("### altitude ###")
        print(round(pos.relative_altitude_m, 1))
        if(pos.relative_altitude_m >= 2.4):
            break



    print("landing")
    await drone.action.land()




async def print_status_function(vehicle):
    try:
        async for status_text in vehicle.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return



if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
