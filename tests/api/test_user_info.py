import pytest

from api.engines.lichess import LichessAPI
from api.engines.user_info import UserInfo
from bot_core import Core


class TestLichess:
    def setup_class(self):
        self._lichess = LichessAPI()

    def get_users_nicknames(self):
        return ['eshikvtumane', 'Rooost']

    def get_users_ids(self):
        nicknames = self.get_users_nicknames()
        return [self._lichess.get_user_by_username(nickname).user_id for nickname in nicknames]

    def test_get_user_by_username(self):
        nicknames = self.get_users_nicknames()
        nickname = nicknames[0]
        lichess_user = self._lichess.get_user_by_username(nickname)
        assert isinstance(lichess_user, UserInfo) == True
        assert lichess_user.username == nickname

    def test_get_users_by_ids(self):
        users = self._lichess.get_users_by_ids(self.get_users_ids())

        assert len(self.get_users_nicknames()) == len(users)

    def test_get_game_stats(self):
        type_game_name = 'blitz'
        nicknames = self.get_users_nicknames()
        nickname = nicknames[0]
        lichess_user = self._lichess.get_user_by_username(nickname)
        stats = lichess_user.get_game_stats_by_name(type_game_name)
        assert stats.name == type_game_name

        stats = lichess_user.get_game_stats_by_name('wrong_game_name')
        assert stats == None


    def test_sorting_user_by_game_type(self):
        type_game_name = 'blitz'
        users = self._lichess.get_users_by_ids(self.get_users_ids())
        sorted_users = Core.sorting_user_by_game_type(type_game_name, users)
        raitings = [user.get_game_stats_by_name(type_game_name).rating for user in sorted_users]

        for index in range(0, len(raitings)-1):
            assert raitings[index] > raitings[index+1]
