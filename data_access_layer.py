from pymongo import MongoClient


class DataAccessLayer:
    def __init__(self, database, login=None, password=None, address='127.0.0.1', port='27017'):
        self._connect(login, password, address, port)
        self._set_db(database)
        self._set_collections()

    def _connect(self, login, password, address, port):
        self._conn = MongoClient(address, port)

    def _set_db(self, db_name):
        self._db = self._conn.get_database(db_name)

    def _set_collections(self):
        self._users = self._db.get_collection('users_test')

    def insert_user(self, telegram_user_id, telegram_fullname, telegram_username):
        self._users.insert({"telegram_id": telegram_user_id,
                            "telegram_fullname": telegram_fullname,
                            "telegram_username": telegram_username})

    def update_lichess_nickname(self, telegram_user_id, nickname, chess_api_id):
        self._users.update({"telegram_id": telegram_user_id},
                           {"$set": {"lichess_nickname": nickname, "lichess_id": chess_api_id}})

    def get_user(self, telegram_user_id):
        user = self._users.find_one({"telegram_id": telegram_user_id})

        if user:
            return User(user.get('telegram_id', None), user.get('lichess_nickname', None))
        return None

    def get_all_lichess_ids(self):
        cursor = self._users.find({'lichess_id': {'$exists': True}}, {'lichess_id'})
        return [c.get('lichess_id') for c in cursor]

    def get_all_telegram_ids(self):
        return self._users.find({}, {'telegram_id'})

    def close(self):
        self._conn.close()

    def __destroy__(self):
        self.close()


class User:
    def __init__(self, telegram_user_id, lichess_nickname):
        self.telegram_user_id = telegram_user_id
        self.lichess_nickname = lichess_nickname

    def check_lichess_nickname(self):
        if self.lichess_nickname:
            return True
        return False
