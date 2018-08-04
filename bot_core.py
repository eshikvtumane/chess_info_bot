from filecmp import cmp

from api.chess_api_enum import ChessAPIEnum
from telegram_bot_response_wrapper import TelegramBotResponseWrapper


class Core:
    def __init__(self, dal):
        self._data_access_layer = dal

    def create_user(self, update):
        wrapper = TelegramBotResponseWrapper(update)
        self._data_access_layer.insert_user(wrapper.get_user_id())

    def get_info_by_nickname(self, nickname, chess_api):
        info = chess_api.get_user_by_username(nickname)
        return info

    def update_nickname_and_chess_api_id(self, user_id, nickname, chess_api, chess_api_user_id):

        method_name = 'update_%s_nickname' % chess_api.name
        update_method = getattr(self._data_access_layer, method_name, None)

        if update_method:
            update_method(user_id, nickname, chess_api_user_id)

    def get_nickname_from_command_args(self, args):
        if args is not None:
            return args[0]
        return None

    def get_all_users_id_from_chat_without_bot(self, chat_id):
        users = self._tg_api.get_participants(chat_id)
        # users = filter(lambda x: x.bot is False, users)

        return [user.id for user in users if user.bot is False]

    def get_all_lichess_ids_from_db(self):
        return self._data_access_layer.get_all_lichess_ids()

    def get_users_info_from_chess_api_by_nicknames(self, chess_api, ids=[]):
        return chess_api.get_users_by_ids(ids)

    def get_all_telegram_ids_db(self):
        return self._data_access_layer.get_all_telegram_ids()

    @staticmethod
    def sorting_user_by_game_type(game_type_name, users):
        return sorted(users,  key=lambda x: x.get_game_stats_by_name(game_type_name).rating, reverse=True)

    def rating_html(self, chess_api_name, type_game_name, users):
        '''

        :param game_type_name: string
        :param users: object UserInfo
        :return: html
        '''

        header = 'Top player %s %s \n\n' % (chess_api_name, type_game_name)
        lines = []
        for idx, user in enumerate(users):
            username = user.username
            rating = user.get_game_stats_by_name(type_game_name).rating
            lines.append('%s) %s %s' % (idx+1, username, rating))

        return header + '\n'.join(lines)
