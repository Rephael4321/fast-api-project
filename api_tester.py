import asyncio
import httpx
from Config import API_PORT
from HttpMethods import HttpMethods

URL = f"http://127.0.0.1:{API_PORT}"

async def request(client: httpx.AsyncClient, url: str, http_method: str, payload: dict = None) -> dict[str, str, dict]:
    if http_method == HttpMethods.GET.name:
        response = await client.get(url)
    elif http_method == HttpMethods.POST.name:
        response = await client.post(url, json=payload)
    elif http_method == HttpMethods.PUT.name:
        response = await client.put(url, json=payload)
    elif http_method == HttpMethods.DELETE.name:
        response = await client.delete(url)
    
    response = response.json()

    return {"http_method": http_method, "url": url, "response": response}

def printResponse(response_obj: dict[str, str, dict]) -> None:
    def printDict(obj: dict) -> None:
        print("{")
        for key, value in obj.items():
            print(f"\t'{key}': {value},")
        print("}")

    print()
    print(f"# {response_obj["http_method"]} {response_obj["url"]}")
    print("-" * 40)
    response = response_obj["response"]
    if isinstance(response, str):
        print(response)
    elif isinstance(response, list):
        for obj in response:
            printDict(obj)
    else:
        printDict(response)
    print()

async def requestAndPrint(client: httpx.AsyncClient, url: str, http_method: str, payload: dict = None) -> None:
    response = await request(client, url, http_method, payload)
    printResponse(response)

async def main():
    timeout = httpx.Timeout(10)
    async with httpx.AsyncClient(timeout=timeout) as client:
        payload = {
            "name": "AAA",
            "age": 15,
            "email": ".com"
        }

        # task1 = asyncio.create_task(requestAndPrint(client, f"{URL}/test_async", "GET"))
        # task2 = asyncio.create_task(requestAndPrint(client, f"{URL}/students", "GET"))
        task3 = asyncio.create_task(requestAndPrint(client, f"{URL}/students/15", "GET"))
        # task4 = asyncio.create_task(requestAndPrint(client, f"{URL}/students", "POST", payload))
        # task5 = asyncio.create_task(requestAndPrint(client, f"{URL}/students/65", "PUT", payload))
        # task6 = asyncio.create_task(requestAndPrint(client, f"{URL}/students/65", "DELETE"))
        # await task1
        # await task2
        await task3
        # await task4
        # await task5
        # await task6

asyncio.run(main())
