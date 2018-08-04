import logging

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from api.chess_api_enum import ChessAPIEnum
from api.engines.lichess import LichessAPI
from api.game_type import GameType
from bot_core import Core
from config_settings import ConfigSettings
from data_access_layer import DataAccessLayer
from telegram_bot_response_wrapper import TelegramBotResponseWrapper

__all__ = ['main']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# data_access_layer = None
lichess = LichessAPI()

config = ConfigSettings()
dal = DataAccessLayer(database=config.db_name,
                      login=config.db_login,
                      password=config.db_password,
                      address=config.db_address,
                      port=config.db_port)

core = Core(dal)


def start(bot, update):
    core.create_user(update)
    update.message.reply_text('You added in bot database.')


def set_nickname_lichess(bot, update):
    wrapper = TelegramBotResponseWrapper(update)
    args = wrapper.get_command_args()
    nickname = core.get_nickname_from_command_args(args)

    if nickname:
        info = core.get_info_by_nickname(nickname, lichess)
        if isinstance(info, str):
            message = info
        else:
            if dal.get_user(wrapper.get_user_id()) is None:
                dal.insert_user(wrapper.get_user_id())

            core.update_nickname_and_chess_api_id(wrapper.get_user_id(), nickname, lichess, info.user_id)
            message = info.get_total_info()
    else:
        message = 'You not sent nickname'

    bot.send_message(chat_id=wrapper.get_chat_id(),
                     text=message,
                     parse_mode=telegram.ParseMode.HTML)


def elo(bot, update):
    wrapper = TelegramBotResponseWrapper(update)

    reply_message = wrapper.check_reply_message()

    if reply_message:
        user_id = wrapper.get_user_id_from_reply_message()
    else:
        user_id = wrapper.get_user_id()

    user = dal.get_user(user_id)

    if user and user.check_lichess_nickname():
        nickname = user.lichess_nickname
        info = core.get_info_by_nickname(nickname, lichess)
        message = info.get_total_info()
    else:
        message = 'User not register in bot'

    bot.send_message(chat_id=wrapper.get_chat_id(),
                     text=message,
                     parse_mode=telegram.ParseMode.HTML)


def top_chat_rating(bot, update, chess_api, type_game_name):
    wrapper = TelegramBotResponseWrapper(update)
    chess_api_users_ids = core.get_all_chess_api_ids_from_db(chess_api.name)

    if chess_api_users_ids is None:
        message = '%s not found' % chess_api.name
    else:
        users = core.get_users_info_from_chess_api_by_nicknames(chess_api, chess_api_users_ids)
        sorted_users = core.sorting_user_by_game_type(type_game_name, users)
        message = core.rating_html(lichess.name, type_game_name, sorted_users)

    bot.send_message(chat_id=wrapper.get_chat_id(),
                     text=message,
                     parse_mode=telegram.ParseMode.HTML)


def top_chat_lichess(bot, update):
    wrapper = TelegramBotResponseWrapper(update)
    type_game_name = 'blitz'
    # users_telegram_ids = core.get_all_telegram_ids_db()
    # users_ids = core.get_all_users_id_from_chat_without_bot(wrapper.get_chat_id())
    lichess_ids = core.get_all_lichess_ids_from_db()
    users = core.get_users_info_from_chess_api_by_nicknames(lichess, lichess_ids)
    sorted_users = core.sorting_user_by_game_type(type_game_name, users)
    message = core.rating_html(lichess.name, type_game_name, sorted_users)

    bot.send_message(chat_id=wrapper.get_chat_id(),
                     text=message,
                     parse_mode=telegram.ParseMode.HTML)

def button(bot, update):
    query = update.callback_query
    query_data = query.data

    result = core.convert_string_to_list(query_data)

    if isinstance(result, list):
        if result[0] == 'lichess':
            top_chat_rating(bot, update, lichess, result[1])
    else:
        t = ChessAPIEnum.LICHESS.value
        if query.data == ChessAPIEnum.LICHESS.value:
            keyboard = [
                [InlineKeyboardButton(game_type.name, callback_data="['lichess', '%s']" % game_type.value)]
                for game_type in GameType
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.edit_message_text(text="Choose game:".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, reply_markup=reply_markup)


def menu(bot, update):
    keyboard = [
        [InlineKeyboardButton("Lichess rating", callback_data='lichess')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def main():
    updater = Updater(config.telegram_bot_api_key)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('set_nickname_lichess', set_nickname_lichess))
    updater.dispatcher.add_handler(CommandHandler('elo', elo))
    updater.dispatcher.add_handler(CommandHandler('top_chat_lichess', top_chat_lichess))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()