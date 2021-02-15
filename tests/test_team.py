"""
Unit Tests for Team Model
"""

import pytest
from blaseball_mike.models import Team, Player, Modification
from blaseball_mike.tables import Tarot
from .helpers import TestBase


class TestTeam(TestBase):
    def test_base_compliance(self, team):
        self.base_test(team)

    @pytest.mark.vcr
    def test_players(self, team):
        assert isinstance(team.lineup, list)
        for player in team.lineup:
            assert isinstance(player, Player)

        assert isinstance(team.rotation, list)
        for player in team.rotation:
            assert isinstance(player, Player)

        assert isinstance(team.bullpen, list)
        for player in team.bullpen:
            assert isinstance(player, Player)

        assert isinstance(team.bench, list)
        for player in team.bench:
            assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_modifications(self, team):
        assert isinstance(team.perm_attr, list)
        for mod in team.perm_attr:
            assert isinstance(mod, Modification)

        assert isinstance(team.seas_attr, list)
        for mod in team.seas_attr:
            assert isinstance(mod, Modification)

        assert isinstance(team.week_attr, list)
        for mod in team.week_attr:
            assert isinstance(mod, Modification)

        assert isinstance(team.game_attr, list)
        for mod in team.game_attr:
            assert isinstance(mod, Modification)

    def test_tarot(self, team):
        assert isinstance(team.card, (Tarot, type(None)))

    def test_misc(self, team):
        assert isinstance(team.id, str)
        assert isinstance(team.full_name, str)
        assert isinstance(team.location, str)
        assert isinstance(team.nickname, str)
        assert isinstance(team.shorthand, str)
        assert isinstance(team.slogan, str)
        assert isinstance(team.emoji, str)
        assert isinstance(team.main_color, str)
        assert isinstance(team.secondary_color, str)

        assert isinstance(team.shame_runs, (int, float))
        assert isinstance(team.total_shames, int)
        assert isinstance(team.total_shamings, int)
        assert isinstance(team.season_shames, int)
        assert isinstance(team.season_shamings, int)

    def test_added_fields(self, team):
        if getattr(team, "team_spirit", None):
            assert isinstance(team.team_spirit, int)
        if getattr(team, "rotation_slot", None):
            assert isinstance(team.rotation_slot, int)
        if getattr(team, "tournament_wins", None):
            assert isinstance(team.tournament_wins, int)

    @pytest.mark.vcr
    def test_load(self):
        bad_team = Team.load("3f8bbb15-61c0-4e3f-8e4a-907a5fb1565e")
        assert isinstance(bad_team, Team)

    @pytest.mark.vcr
    def test_load_bad_team(self):
        with pytest.raises(ValueError):
            bad_team = Team.load("00000000-0000-0000-0000-000000000000")

    @pytest.mark.vcr
    def test_load_by_name(self):
        team = Team.load_by_name("Boston Flowers")
        assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load_by_name_bad_name(self):
        bad_name = Team.load_by_name("Ohio Astronauts")
        assert bad_name is None

    @pytest.mark.vcr
    def test_load_all(self):
        teams = Team.load_all()
        assert isinstance(teams, dict)
        assert len(teams) > 0
        for key, team in teams.items():
            assert isinstance(key, str)
            assert isinstance(team, Team)
            assert key == team.id

    @pytest.mark.vcr
    def test_load_at_time(self):
        team = Team.load_at_time("3f8bbb15-61c0-4e3f-8e4a-907a5fb1565e", time="2020-08-01T18:00:00Z")
        assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load_at_time_bad_team(self):
        bad_team = Team.load_at_time("00000000-0000-0000-0000-000000000000", time="2020-08-01T18:00:00Z")
        assert bad_team is None

    @pytest.mark.vcr
    def test_load_one_at_time_bad_time(self):
        bad_time = Team.load_at_time("3f8bbb15-61c0-4e3f-8e4a-907a5fb1565e", time="1980-01-01T00:00:00Z")
        assert bad_time is None
