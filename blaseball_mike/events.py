"""
Wrapper around the SSE events API.
"""
import asyncio
from concurrent import futures
import jsonpointer
import ujson

from aiohttp_sse_client import client as sse_client
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError, ServerDisconnectedError


async def stream_events(url='https://api.blaseball.com/events/streamData', retry_base=0.01, retry_max=300):
    """
    Async generator for the events API.
    `retry_base` will be the minimum time to delay if there's a connection error
    `retry_max` is the maximum time to delay if there's a connection error
    """
    retry_delay = retry_base
    event_current = {}
    while True:
        try:
            async with sse_client.EventSource(url, read_bufsize=2 ** 19) as src:
                async for event in src:
                    retry_delay = retry_base  # reset backoff
                    if not event.data:
                        continue
                    raw_event = ujson.loads(event.data)
                    if 'value' in raw_event.keys():
                        payload = raw_event['value']
                        event_tmp = payload
                    else: # If this is a delta (modification) of a past event, modify event_tmp.
                        event_tmp = event_current
                        for delta in raw_event['delta']:
                            path = '/'+'/'.join([str(item) for item in delta['path']])
                            if delta['kind'] == 'E': # Replace a full dict element
                                if 'lhs' in delta:
                                    if delta['lhs'] == jsonpointer.resolve_pointer(event_tmp, path):
                                        jsonpointer.set_pointer(event_tmp, path, delta['rhs'])
                                    else:
                                        print("Error. LHS does not match event_tmp!")
                                        break
                            elif delta['kind'] == 'A': # Modify a list
                                if delta['item']['kind'] == 'D': # Delete a list element
                                    thislist = jsonpointer.resolve_pointer(event_tmp, path)
                                    if thislist[delta['index']] == delta['item']['lhs']:
                                        del thislist[delta['index']]
                                        jsonpointer.set_pointer(event_tmp, path, thislist)
                                    else:
                                        print("Error. LHS does not match event_tmp!")
                                        break
                                elif delta['item']['kind'] == 'N': # Add a new list element
                                    thislist = jsonpointer.resolve_pointer(event_tmp, path)
                                    thislist.insert(delta['index'], delta['item']['rhs'])
                                    jsonpointer.set_pointer(event_tmp, path, thislist)
                                else:
                                    print("Unknown delta A item kind code!!")
                                    print(delta)
                            elif delta['kind'] == 'N': # Add a new element to a dict
                                path,newkey = path.rsplit('/',1)
                                thisdict = jsonpointer.resolve_pointer(event_tmp, path)
                                thisdict[newkey] = delta['rhs']
                                jsonpointer.set_pointer(event_tmp, path, thisdict)
                            elif delta['kind'] == 'D': # Delete a dict element
                                path,oldkey = path.rsplit('/',1)
                                thisdict = jsonpointer.resolve_pointer(event_tmp, path)
                                if thisdict[oldkey] == delta['lhs']:
                                    del thisdict[oldkey]
                                    jsonpointer.set_pointer(event_tmp, path, thisdict)
                                else:
                                    print("Error. LHS does not match event_tmp!")
                                    break
                            else:
                                print("Unknown delta kind code!!")
                                print(delta)
                        else:
                            event_current = event_tmp
                        payload = event_current
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
