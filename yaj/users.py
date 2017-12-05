from flask import session

class User():

    def __init__(self, user_id, authenticated = True, active = True, anonymous = False):
        self.user_id = user_id
        self.authenticated = authenticated
        self.active = active
        self.anonymous = anonymous


    def get_id(self):
        return str(self.user_id)

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return self.anonymous

class UserManager():
    def get(uid):
        from yaj.views import get_user_by_unique_column
        user = None
        user_details = get_user_by_unique_column("user_id", uid)
        if user_details != None:
            user = User(user_id = uid)
            user.data = {}
            for key in user_details:
                user.data[key] = user_details[key]
        return user
