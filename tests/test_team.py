"""
Unit Tests for Team Model
"""

import pytest
import vcr
from blaseball_mike.models import Team, Player, Modification
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

    @pytest.fixture(scope="module")
    def team_xpresso(self):
        """Tournament team test"""
        return Team({
            "id": "d8f82163-2e74-496b-8e4b-2ab35b2d3ff1",
            "lineup": [
                "678170e4-0688-436d-a02d-c0467f9af8c0",
                "cbd19e6f-3d08-4734-b23f-585330028665",
                "a7d8196a-ca6b-4dab-a9d7-c27f3e86cc21",
                "03b80a57-77ea-4913-9be4-7a85c3594745",
                "766dfd1e-11c3-42b6-a167-9b2d568b5dc0",
                "32c9bce6-6e52-40fa-9f64-3629b3d026a8",
                "04931546-1b4a-469f-b391-7ed67afe824c",
                "817dee99-9ccf-4f41-84e3-dc9773237bc8",
                "2f3d7bc7-6ffb-40c3-a94f-5e626be413c9"
            ],
            "rotation": [
                "ae4acebd-edb5-4d20-bf69-f2d5151312ff",
                "dddb6485-0527-4523-9bec-324a5b66bf37",
                "5eac7fd9-0d19-4bf4-a013-994acc0c40c0",
                "03f920cc-411f-44ef-ae66-98a44e883291",
                "73265ee3-bb35-40d1-b696-1f241a6f5966"
            ],
            "bullpen": [
                "57290370-6723-4d33-929e-b4fc190e6a9a",
                "c9e4a49e-e35a-4034-a4c7-293896b40c58",
                "6b8d128f-ed51-496d-a965-6614476f8256",
                "8b53ce82-4b1a-48f0-999d-1774b3719202",
                "138fccc3-e66f-4b07-8327-d4b6f372f654"
            ],
            "bench": [
                "9ba361a1-16d5-4f30-b590-fc4fc2fb53d2",
                "60026a9d-fc9a-4f5a-94fd-2225398fa3da",
                "cd417f8a-ce01-4ab2-921d-42e2e445bbe2",
                "a647388d-fc59-4c1b-90d3-8c1826e07775"
            ],
            "seasAttr": [],
            "permAttr": [],
            "fullName": "Inter Xpresso",
            "location": "Xpresso",
            "mainColor": "#8a2444",
            "nickname": "Xpresso",
            "secondaryColor": "#e6608b",
            "shorthand": "IE",
            "emoji": "0x274C",
            "slogan": "We've got a Shot!",
            "shameRuns": 0,
            "totalShames": 0,
            "totalShamings": 1,
            "seasonShames": 0,
            "seasonShamings": 1,
            "championships": 0,
            "weekAttr": [],
            "gameAttr": [],
            "rotationSlot": 15,
            "teamSpirit": 0,
            "card": -1,
            "tournamentWins": 1
        })

    @pytest.fixture(scope="module", params=['team_crabs', 'team_pies_chronicler', 'team_ohio_astronauts',
                                            'team_xpresso'])
    def team(self, request):
        """Parameterized fixture of various teams"""
        return request.getfixturevalue(request.param)
