"""
Wrapper around the SSE events API.
"""
import asyncio
from concurrent import futures
import ujson

from aiohttp_sse_client import client as sse_client
from aiohttp.client_exceptions import ClientPayloadError


async def stream_events(url='https://www.blaseball.com/events/streamData', retry_base=0.01, retry_max=300):
    """
    Async generator for the events API.
    `retry_base` will be the minimum time to delay if there's a connection error
    `retry_max` is the maximum time to delay if there's a connection error
    """
    retry_delay = retry_base
    while True:
        try:
            async with sse_client.EventSource(url) as src:
                async for event in src:
                    retry_delay = retry_base  # reset backoff
                    if not event.data:
                        continue
                    payload = ujson.loads(event.data)['value']
                    yield payload
        except (ConnectionError, TimeoutError, ClientPayloadError, futures.TimeoutError, asyncio.exceptions.TimeoutError):
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, retry_max)
