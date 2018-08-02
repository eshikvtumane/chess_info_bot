import lichess.api
from lichess.api import ApiHttpError

from api.chess_api_enum import ChessAPIEnum
from .user_info import UserInfo


class LichessAPI:
    name = ChessAPIEnum.LICHESS.value

    def __init__(self):
        self.api = self._connect()

    def _connect(self):
        return lichess.api

    def get_user_by_username(self, username):
        try:
            user = self.api.user(username)
            return UserInfo(user)
        except ApiHttpError:
            return None

    def get_users_by_ids(self, ids=[]):
        users = self.api.users_by_ids(ids)
        return [UserInfo(user) for user in users]

    # def get_info(self):
    #     user


