class User:
    users = {}

    def __init__(self, tg_id):
        self.tg_id = tg_id
        self.allowed = True

    @classmethod
    def get(cls, tg_id):
        return cls.users.get(tg_id)

    @classmethod
    def create(cls, tg_id):
        user = User(tg_id)
        cls.users[tg_id] = user
        return user

    @classmethod
    def get_or_create(cls, tg_id):
        user = cls.get(tg_id)
        if user is None:
            user = cls.create(tg_id)
        return user

    def block(self):
        self.allowed = False

    def allow(self):
        self.allowed = True
