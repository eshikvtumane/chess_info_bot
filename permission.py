class Permission:
    def __init__(self, bot):
        self._bot = bot

    def _get_chat_administrators(self, chat_id):
        return self._bot.get_chat_administrators(chat_id)

    def check_user_in_administrators(self, user_id, chat_id):

        administrators = self._get_chat_administrators(chat_id)
        quantity = len(list(filter(lambda x: x.user.id == user_id, administrators)))
        if quantity > 0:
            return True
        return False
