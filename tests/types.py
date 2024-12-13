

class Users:
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER1 = 'user1'
    USER2 = 'user2'

    @staticmethod
    def all():
        return [Users.ADMIN, Users.MANAGER, Users.USER1, Users.USER2]

