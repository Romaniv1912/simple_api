class Users:
    ADMIN = 'admin'
    ADMIN_ID = 1

    MANAGER = 'manager'
    MANAGER_ID = 2

    USER1 = 'user1'
    USER1_ID = 3

    USER2 = 'user2'
    USER2_ID = 4

    @staticmethod
    def all():
        return [Users.ADMIN, Users.MANAGER, Users.USER1, Users.USER2]


class Records:
    ADMIN = 1
    MANAGER = 2
    USER1 = 3
    USER2 = 4
