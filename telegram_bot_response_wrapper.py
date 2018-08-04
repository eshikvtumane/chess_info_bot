class TelegramBotResponseWrapper:
    def __init__(self, update):
        self._update = update

    def get_user_id(self):
        return self._update.effective_user.id

    def get_chat_id(self):
        return self._update.effective_chat.id

    def get_chat_name(self):
        return self._update.effective_chat.title

    def check_chat_name(self, name):
        chat_name = self.get_chat_name()
        if chat_name == name:
            return True
        return False

    def get_command_args(self):
        result = self._update.effective_message.text.split(' ')

        if len(result) >= 2:
            return result[1:]

        return None

    def check_reply_message(self):
        if self._update.effective_message.reply_to_message:
            return True
        return False

    def get_user_id_from_reply_message(self):
        if not self.check_reply_message:
            return None

        return self._update.effective_message.reply_to_message.from_user.id

    def get_telegram_username(self):
        return self._update.effective_user.username

    def get_telegram_fullname(self):
        user = self._update.effective_user
        return user.full_name
