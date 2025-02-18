import asyncio
import httpx
from http import HTTPMethod
from Config import API_PORT

URL = f"http://127.0.0.1:{API_PORT}"

async def request(client: httpx.AsyncClient, url: str, http_method: str, payload: dict = None) -> dict[str, str, dict]:
    if http_method == HTTPMethod.GET:
        response = await client.get(url)
    elif http_method == HTTPMethod.POST:
        response = await client.post(url, json=payload)
    elif http_method == HTTPMethod.PUT:
        response = await client.put(url, json=payload)
    elif http_method == HTTPMethod.DELETE:
        response = await client.delete(url)
    
    try:
        response = response.json()
    except:
        print(response)
        response = {}

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

        tasks = [
            asyncio.create_task(requestAndPrint(client, f"{URL}/test_async", "GET")),
            asyncio.create_task(requestAndPrint(client, f"{URL}/students", "GET")),
            asyncio.create_task(requestAndPrint(client, f"{URL}/students/15", "GET")),
            asyncio.create_task(requestAndPrint(client, f"{URL}/students", "POST", payload)),
            asyncio.create_task(requestAndPrint(client, f"{URL}/students/93", "PUT", payload)),
            asyncio.create_task(requestAndPrint(client, f"{URL}/students/90", "DELETE"))
        ]

        for task in tasks:
            await task

asyncio.run(main())
