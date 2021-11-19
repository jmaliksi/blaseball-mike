"""
Wrapper around the SSE events API.
"""
import asyncio
from concurrent import futures
import jsonpatch
import jsonpointer
import ujson

from aiohttp_sse_client import client as sse_client
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError, ServerDisconnectedError


async def stream_events(url='https://api.blaseball.com/events/streamData', retry_base=0.01, retry_max=300, on_parse_error='LOG'):
    """
    Async generator for the events API.
    `retry_base` will be the minimum time to delay if there's a connection error
    `retry_max` is the maximum time to delay if there's a connection error
    """
    retry_delay = retry_base
    event_current = {}
    delta_previous = None
    while True:
        try:
            async with sse_client.EventSource(url, read_bufsize=2 ** 19) as src:
                async for event in src:
                    retry_delay = retry_base  # reset backoff
                    if not event.data:
                        continue
                    raw_event = ujson.loads(event.data)
                    if 'value' in raw_event.keys(): # New, full event
                        delta_previous = None
                        event_current = raw_event['value']
                        payload = event_current
                    elif 'delta' in raw_event.keys(): # Delta event
                        if raw_event['delta'] == delta_previous:
                            continue
                        delta_previous = raw_event['delta']
                        jsonpatch.apply_patch(event_current, raw_event['delta'], in_place=True)
                        payload = event_current
                    else:
                        raise ValueError("Unknown event type: {}".format(raw_event.keys()))
                    yield payload
        except (ConnectionError,
                TimeoutError,
                ClientPayloadError,
                futures.TimeoutError,
                asyncio.exceptions.TimeoutError,
                ClientConnectorError,
                ServerDisconnectedError):
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, retry_max)
        except (jsonpatch.JsonPatchConflict,
                jsonpointer.JsonPointerException,
                IndexError,
                ValueError) as error:
            if on_parse_error.lower()=='skip':
                pass
            elif on_parse_error.lower()=='raise':
                print("Event parse error.")
                raise
            else: # log and restart, default
                print("Event parse error.")
                print(error)
