import asyncio

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("waiting for connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("connected!")
            break

    print("waiting for global position estimate")
    async for health in drone.telemetry.health():
         if health.is_global_position_ok and health.is_home_position_ok:
            print("global position estimate OK")
            break

    print("ARMING")
    await drone.action.arm()

    print("setting initial setpoint")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))

    print("starting OFFBOARD")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"OffBoard error: {error._result.result}")
        print("disarming...")
        await drone.action.disarm()
        return

    print("-- go UP at 50% thrust")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.5)) #(roll, pitch, yaw, thrust)
    await asyncio.sleep(5)

    await drone.offboard.set_attitude(Attitude(15.0, 0.0, 0.0, 0.5))
    await asyncio.sleep(2)
    #await drone.action.hold()


    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.5))
    await asyncio.sleep(3)

    await drone.offboard.set_attitude(Attitude(-15.0, 0.0, 0.0, 0.5))
    await asyncio.sleep(2)

    await drone.action.hold()

    print("returning to launch")
    await drone.action.return_to_launch()


if __name__ == "__main__":
    asyncio.run(run())

