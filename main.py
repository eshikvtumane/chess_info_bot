import logging

import telegram
from telegram.ext import Updater, CommandHandler

from api.engines.lichess import LichessAPI
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

            core.update_nickname(wrapper.get_user_id(), nickname, lichess.name)
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


def top_lichess(bot, update):
    member = bot.getChat(update.effective_chat.id)
    member = bot.getChatMembersCount(update.effective_chat.id)
    update.message.reply_text("")


def main():
    updater = Updater(config.telegram_bot_api_key)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('set_nickname_lichess', set_nickname_lichess))
    updater.dispatcher.add_handler(CommandHandler('elo', elo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()