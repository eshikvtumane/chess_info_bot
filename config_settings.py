from enum import Enum

try:
    import settings
except:
    raise ModuleNotFoundError('Create settings.py file in root project.')


class AttributeEnum(Enum):
    DATABASE_NAME = 'DATABASE_NAME'
    DATABASE_ADDRESS = 'DATABASE_ADDRESS'
    DATABASE_ENGINE = 'DATABASE_ENGINE'
    DATABASE_PORT = 'DATABASE_PORT'
    DATABASE_LOGIN = 'DATABASE_LOGIN'
    DATABASE_PASSWORD = 'DATABASE_PASSWORD'

    API_ID = 'API_ID'
    API_HASH = 'API_HASH'
    BOT_SECRET_KEY = 'BOT_SECRET_KEY'

    CHAT_NAME = 'CHAT_NAME'


class ConfigSettings:
    def __init__(self):
        self._get_config()

    def _get_config(self):
        self._settings = settings

    def get_settings_property(self, attr_name):
        return getattr(self._settings, attr_name.value, None)

    @property
    def db_name(self):
        return self.get_settings_property(AttributeEnum.DATABASE_NAME)

    @property
    def db_address(self):
        return self.get_settings_property(AttributeEnum.DATABASE_ADDRESS)

    @property
    def db_port(self):
        return self.get_settings_property(AttributeEnum.DATABASE_PORT)

    @property
    def db_login(self):
        return self.get_settings_property(AttributeEnum.DATABASE_LOGIN)

    @property
    def db_password(self):
        return self.get_settings_property(AttributeEnum.DATABASE_PASSWORD)

    @property
    def telegram_bot_api_key(self):
        return self.get_settings_property(AttributeEnum.BOT_SECRET_KEY)

    @property
    def telegram_api_key(self):
        return self.get_settings_property(AttributeEnum.API_ID)

    @property
    def telegram_api_hash(self):
        return self.get_settings_property(AttributeEnum.API_HASH)

    @property
    def chat_name(self):
        return self.get_settings_property(AttributeEnum.CHAT_NAME)
