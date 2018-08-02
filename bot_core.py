import telegram

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

    def update_nickname(self, user_id, nickname, chess_api_name):

        method_name = 'update_%s_nickname' % chess_api_name
        update_method = getattr(self._data_access_layer, method_name, None)

        if update_method:
            update_method(user_id, nickname)

    def get_nickname_from_command_args(self, args):
        if args is not None:
            return args[0]
        return None



    # def get_info_html(self, user):
