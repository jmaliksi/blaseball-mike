"""
This isn't actually a unit test lol.
"""
import asyncio
import pytest

from blaseball_mike.events import stream_events
from blaseball_mike.models import Game
from blaseball_mike.stream_model import StreamData


@pytest.mark.skip()
async def test_stream():
    async for event in stream_events():
        payload = event
        print(payload)
        schedule = {
            g['id']: Game(g) for g in payload.get('games', {}).get('schedule')
        }
        print(schedule)


@pytest.mark.skip()
async def test_stream_data():
    async for event in stream_events(url='http://api-test.sibr.dev/replay/v1/replay?from=2020-10-07T13:02:00Z'):
        payload = StreamData(event)
        print(payload)
        schedule = {
            id: g for id, g in payload.games.schedule.games.items()
        }
        print(schedule)
        print(payload.leagues.teams)


@pytest.mark.skip()
def test():
    loop = asyncio.get_event_loop()
    loop.create_task(test_stream())
    loop.run_forever()


if __name__ == '__main__':
    test()
