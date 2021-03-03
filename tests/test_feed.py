"""
Unit Tests for Feed Model
"""

import pytest
import vcr
from datetime import datetime
from blaseball_mike.models import Feed, Player, Team, Game
from .helpers import TestBase, CASSETTE_DIR


class TestFeed(TestBase):
    def test_base_compliance(self, feed):
        for feed_event in feed:
            self.base_test(feed_event)

    def test_global_event(self, feed):
        for feed_event in feed:
            assert isinstance(feed_event, Feed)
            assert isinstance(feed_event.id, str)
            assert isinstance(feed_event.description, str)
            assert isinstance(feed_event.season, int)
            assert isinstance(feed_event.day, int)
            assert isinstance(feed_event.tournament, int)
            assert isinstance(feed_event.phase, int)
            assert isinstance(feed_event.type, int)
            assert isinstance(feed_event.category, int)
            assert isinstance(feed_event.created, datetime)

            for team in feed_event.team_tags:
                assert isinstance(team, Team)

            for player in feed_event.player_tags:
                assert isinstance(player, Player)

            for game in feed_event.game_tags:
                assert isinstance(game, Game)

    @pytest.mark.vcr
    def test_load(self):
        feed = Feed.load(count=2, category=0)
        assert isinstance(feed, list)
        assert len(feed) == 2
        for item in feed:
            assert isinstance(item, Feed)
            assert item.category == 0

    @pytest.mark.vcr
    def test_load_by_game(self):
        feed = Feed.load_by_game(game_id="ebcf203e-6ce7-4d64-8f3e-a78b373c70ff", count=2, category=0)
        assert isinstance(feed, list)
        assert len(feed) == 2
        for item in feed:
            assert isinstance(item, Feed)
            assert item.category == 0

    @pytest.mark.vcr
    def test_load_by_player(self):
        feed = Feed.load_by_player(player_id="1f159bab-923a-4811-b6fa-02bfde50925a", count=2, category=0)
        assert isinstance(feed, list)
        assert len(feed) == 2
        for item in feed:
            assert isinstance(item, Feed)
            assert item.category == 0

    @pytest.mark.vcr
    def test_load_by_team(self):
        feed = Feed.load_by_team(team_id="a37f9158-7f82-46bc-908c-c9e2dda7c33b", count=2, category=0)
        assert isinstance(feed, list)
        assert len(feed) == 2
        for item in feed:
            assert isinstance(item, Feed)
            assert item.category == 0

    @pytest.mark.vcr
    def test_load_by_phase(self):
        feed = Feed.load_by_phase(season=12, phase=3)
        assert isinstance(feed, list)
        assert len(feed) > 0
        for item in feed:
            assert isinstance(item, Feed)
            assert item.season == 12
            assert item.phase == 3

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.feed_global_current.yaml')
    def feed_global_current(self):
        return Feed.load(count=3)

    @pytest.fixture(scope="module")
    def feed_s12_reading(self):
        return [Feed({
            "id": "758c38cf-753d-49a2-97d8-ef633d93917e",
            "playerTags": [
              "09f2787a-3352-41a6-8810-d80e97b253b5",
              "316abea7-9890-4fb8-aaea-86b35e24d9be"
            ],
            "teamTags": [
              "7966eb04-efcc-499b-8f03-d13916330531",
              "ca3f1c8c-c025-4d8e-8eef-5be6accbeb16"
            ],
            "gameTags": [],
            "metadata": {
              "count": "20",
              "spread": [
                0,
                11,
                13
              ],
              "tarotId": "over_under"
            },
            "created": "2021-03-02T18:32:50.777Z",
            "season": 11,
            "tournament": -1,
            "type": 81,
            "day": 27,
            "phase": 3,
            "category": 1,
            "description": "OVER UNDER\nUNDER OVER"
          })]

    @pytest.fixture(scope="module", params=['feed_global_current', 'feed_s12_reading'])
    def feed(self, request):
        """Parameterized fixture of various feeds"""
        return request.getfixturevalue(request.param)
