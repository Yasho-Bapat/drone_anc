import asyncio
import sys

async def count():
    print("one")
    await asyncio.sleep(1) # this tells the compiler "i'm going to sleep, let the next meaningful process/whatever take place". can't use time.sleep because that pauses everything
    print("two")

async def main():
    await asyncio.gather(count(), count(), count()) # runs the functions at the same time


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    el = time.perf_counter() - s
    print(f"{__file__} executed in {el:0.2f} seconds")
    print("this is the name of the programL ", sys.argv[0])
    print("argument list: ", str(sys.argv))