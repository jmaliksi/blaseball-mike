"""
Unit Tests for Team Model
"""

import pytest
import vcr
from blaseball_mike.models import Team, Player, Modification, Stadium
from blaseball_mike.tables import Tarot
from .helpers import TestBase, CASSETTE_DIR


class TestTeam(TestBase):
    def test_base_compliance(self, team):
        self.base_test(team)

    @pytest.mark.vcr
    def test_lineup(self, team):
        """Test players on the lineup are valid and also alive"""
        assert isinstance(team.lineup, list)
        for player in team.lineup:
            assert isinstance(player, Player)
            assert player.deceased is False

    @pytest.mark.vcr
    def test_rotation(self, team):
        """Test players on the rotation are valid and also alive"""
        assert isinstance(team.rotation, list)
        for player in team.rotation:
            assert isinstance(player, Player)
            assert player.deceased is False

    @pytest.mark.vcr
    def test_bullpen(self, team):
        """Test players on the bullpen are valid and also alive"""
        assert isinstance(team.bullpen, list)
        for player in team.bullpen:
            assert isinstance(player, Player)
            assert player.deceased is False

    @pytest.mark.vcr
    def test_bench(self, team):
        """Test players on the bench are valid and also alive"""
        assert isinstance(team.bench, list)
        for player in team.bench:
            assert isinstance(player, Player)
            assert player.deceased is False

    @pytest.mark.vcr
    def test_shadows(self, team):
        """Test players in the shadows are valid and also alive"""
        assert isinstance(team.shadows, list)
        for player in team.shadows:
            assert isinstance(player, Player)
            assert player.deceased is False

    @pytest.mark.vcr
    def test_perm_mods(self, team):
        assert isinstance(team.perm_attr, list)
        for mod in team.perm_attr:
            assert isinstance(mod, Modification)
            assert mod.id != "????"

    @pytest.mark.vcr
    def test_seas_mods(self, team):
        assert isinstance(team.seas_attr, list)
        for mod in team.seas_attr:
            assert isinstance(mod, Modification)
            assert mod.id != "????"

    @pytest.mark.vcr
    def test_week_mods(self, team):
        assert isinstance(team.week_attr, list)
        for mod in team.week_attr:
            assert isinstance(mod, Modification)
            assert mod.id != "????"

    @pytest.mark.vcr
    def test_game_mods(self, team):
        assert isinstance(team.game_attr, list)
        for mod in team.game_attr:
            assert isinstance(mod, Modification)
            assert mod.id != "????"

    def test_tarot(self, team):
        assert isinstance(team.card, (Tarot, type(None)))

    @pytest.mark.vcr
    def test_stadium(self, team):
        assert isinstance(team.stadium, (Stadium, type(None)))

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
        if getattr(team, "team_spirit", None) is not None:
            assert isinstance(team.team_spirit, int)
        if getattr(team, "rotation_slot", None) is not None:
            assert isinstance(team.rotation_slot, int)
        if getattr(team, "tournament_wins", None) is not None:
            assert isinstance(team.tournament_wins, int)
        if getattr(team, "e_density", None) is not None:
            assert isinstance(team.e_density, (int, float))
        if getattr(team, "state", None) is not None:
            assert isinstance(team.state, dict)
        if getattr(team, "evolution", None) is not None:
            assert isinstance(team.evolution, int)
        if getattr(team, "win_streak", None) is not None:
            assert isinstance(team.win_streak, int)
        if getattr(team, "level", None) is not None:
            assert isinstance(team.level, int)

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

    @pytest.mark.vcr
    def test_load_history(self):
        team = Team.load_history("d9f89a8a-c563-493e-9d64-78e4f9a55d4a", count=200)
        assert isinstance(team, list)
        assert len(team) > 0
        for t in team:
            assert isinstance(t, Team)

    @pytest.mark.vcr
    def test_load_history_bad_id(self):
        bad_team = Team.load_history("00000000-0000-0000-0000-000000000000", count=200)
        assert isinstance(bad_team, list)
        assert len(bad_team) == 0

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.team_crabs.yaml')
    def team_crabs(self):
        """common case"""
        return Team.load("8d87c468-699a-47a8-b40d-cfb73a5660ad")

    @pytest.fixture(scope="module")
    def team_ohio_astronauts(self):
        """invalid ID, multi-codepoint emoji, modifications, empty player lists, invalid Tarot"""
        return Team({
            "id": "00000000-0000-0000-0000-000000000000",
            "fullName": "Ohio Astronauts",
            "location": "Ohio",
            "nickname": "Astronauts",
            "shorthand": "OHIO",
            "slogan": "Always has been...",
            "lineup": [],
            "rotation": [],
            "bullpen": [],
            "bench": ["555b0a07-a3e0-41bc-b3db-ca8f520857bc"],
            "seasAttr": ["SHELLED"],
            "permAttr": ["PARTY_TIME"],
            "weekAttr": ["HEATING_UP"],
            "gameAttr": ["GRAVITY"],
            "mainColor": "#333",
            "secondaryColor": "#999",
            "emoji": "🧑🏾‍🚀",
            "shameRuns": 0,
            "totalShames": 69,
            "totalShamings": 420,
            "seasonShames": 0,
            "seasonShamings": 0,
            "championships": 0,
            "rotationSlot": 3,
            "teamSpirit": 0,
            "card": 17,
            "tournamentWins": 0
        })

    @pytest.fixture(scope="module")
    def team_pies_chronicler(self):
        """chronicler historical data, S2"""
        return Team({
            "timestamp": "2020-07-30T02:13:38.328Z",
            "_id": "23e4cbc1-e9cd-47fa-a35b-bfa06f726cb7",
            "bench": [
                "20395b48-279d-44ff-b5bf-7cf2624a2d30",
                "d8bc482e-9309-4230-abcb-2c5a6412446d",
                "cd5494b4-05d0-4b2e-8578-357f0923ff4c"
            ],
            "emoji": "0x1F967",
            "lineup": [
                "1ba715f2-caa3-44c0-9118-b045ea702a34",
                "26cfccf2-850e-43eb-b085-ff73ad0749b8",
                "13a05157-6172-4431-947b-a058217b4aa5",
                "80dff591-2393-448a-8d88-122bd424fa4c",
                "6fc3689f-bb7d-4382-98a2-cf6ddc76909d",
                "15ae64cd-f698-4b00-9d61-c9fffd037ae2",
                "083d09d4-7ed3-4100-b021-8fbe30dd43e8",
                "06ced607-7f96-41e7-a8cd-b501d11d1a7e",
                "66cebbbf-9933-4329-924a-72bd3718f321"
            ],
            "slogan": "Pie or Die.",
            "bullpen": [
                "0672a4be-7e00-402c-b8d6-0b813f58ba96",
                "62111c49-1521-4ca7-8678-cd45dacf0858",
                "7f379b72-f4f0-4d8f-b88b-63211cf50ba6",
                "906a5728-5454-44a0-adfe-fd8be15b8d9b",
                "90cc0211-cd04-4cac-bdac-646c792773fc",
                "a7b0bef3-ee3c-42d4-9e6d-683cd9f5ed84",
                "b85161da-7f4c-42a8-b7f6-19789cf6861d",
                "d2a1e734-60d9-4989-b7d9-6eacda70486b"
            ],
            "fullName": "Philly Pies",
            "location": "Philly",
            "nickname": "Pies",
            "rotation": [
                "1732e623-ffc2-40f0-87ba-fdcf97131f1f",
                "9786b2c9-1205-4718-b0f7-fc000ce91106",
                "b082ca6e-eb11-4eab-8d6a-30f8be522ec4",
                "60026a9d-fc9a-4f5a-94fd-2225398fa3da",
                "814bae61-071a-449b-981e-e7afc839d6d6"
            ],
            "mainColor": "#399d8f",
            "shameRuns": 0,
            "shorthand": "PHIL",
            "totalShames": 3,
            "seasonShames": 3,
            "championships": 1,
            "totalShamings": 0,
            "seasonShamings": 0,
            "secondaryColor": "#ffffff",
            "seasonAttributes": [],
            "permanentAttributes": []
        })

    @pytest.fixture(scope="module", params=['team_crabs', 'team_pies_chronicler', 'team_ohio_astronauts'])
    def team(self, request):
        """Parameterized fixture of various teams"""
        return request.getfixturevalue(request.param)
