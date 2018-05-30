import asyncio
from timeit import default_timer
from aiohttp import ClientSession, ClientConnectorError


def fetch_all(urls):
    """Fetch list of web pages asynchronously."""
    start_time = default_timer()

    loop = asyncio.new_event_loop()  # Create event loop
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(async_fetch_all(urls))  # tasks to do
    loop.run_until_complete(future)  # loop until done

    tot_elapsed = default_timer() - start_time
    print("Fetched all in {0:5.2f} .".format(tot_elapsed))

    return list(future.result())


async def async_fetch_all(urls):
    """Launch requests for all web pages."""
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)  # create list of tasks
        responses = await asyncio.gather(*tasks)  # gather task responses
    return responses


async def fetch(url, session, charset='latin-1'):
    """Fetch a url, using specified ClientSession."""
    try:
        async with session.get(url) as response:
            resp = await response.read()
            print("Fetched: {0:30}".format(url))
            return resp.decode(charset)
    except Exception as e:
        print("Failed to fetch {0:30} with exception : {0:30}".format(url, str(e)))
        return ''
