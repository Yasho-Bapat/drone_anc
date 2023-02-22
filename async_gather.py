import asyncio

async def someFunc(a):
    if(a > 3):
        print(a + 25)
    elif (a == 3):
        print(a * 3)
    else:
        print(a - 25)

async def main():
    res = await asyncio.gather(someFunc(3), someFunc(2), someFunc(8))
    return res
if __name__ == "__main__":
    asyncio.run(main())
