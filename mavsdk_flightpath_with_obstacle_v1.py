import asyncio
import random
from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError, VelocityNedYaw)

drone = System()  # GLOBAL DECLARATION FOR EASE OF FUNCTION DEFINITION


def obstacle():
    obs = random.randint(0, 2)
    if (obs == 1):
        return True
    else:
        return False


async def avoid_obstacle():
    await drone.offboard.set_attitude(Attitude(-5.0, 0.0, 0.0, 0.5))  # (roll, pitch, yaw, thrust)
    await asyncio.sleep(3)

    await drone.offboard.set_attitude(Attitude(0.0, -5.0, 0.0, 0.5))
    await asyncio.sleep(3)


async def run():
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- connected: TRUE")
            break
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- position parameters OK")
            break

    print("ARMING")
    await drone.action.arm()

    # val = list(map(float, input().split())) # WORK ON THIS

    # print(val)
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

    print("checking for obstacle...")
    obs = obstacle()
    print("obstacle: " + str(obs))

    print("-- go UP at 50% thrust")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.5))  # (roll, pitch, yaw, thrust)
    await asyncio.sleep(3)
    await drone.action.hold()

    if(obs):
        await avoid_obstacle()

    await drone.offboard.set_attitude(Attitude(10.0, 10.0, 0.0, 0.5))
    await asyncio.sleep(3)

    print("returning to launch")
    await drone.action.return_to_launch()


if __name__ == "__main__":
    asyncio.run(run())
