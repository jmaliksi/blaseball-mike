"""
This isn't actually a unit test lol.
"""
import asyncio

from blaseball_mike.events import stream_events
from blaseball_mike.models import Game
from blaseball_mike.stream_model import StreamData


async def test_stream():
    async for event in stream_events():
        payload = event
        print(payload)
        schedule = {
            g['id']: Game(g) for g in payload.get('games', {}).get('schedule')
        }
        print(schedule)


async def test_stream_data():
    async for event in stream_events():
        payload = StreamData(event)
        print(payload)


def test():
    loop = asyncio.get_event_loop()
    loop.create_task(test_stream_data())
    loop.run_forever()


if __name__ == '__main__':
    test()
