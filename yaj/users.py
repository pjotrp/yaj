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
    def get(uid, login_type = None):
        user = None
        if login_type == "github-oauth":
            user_details = UserManager.login_github_user(uid)
            user = User(user_id = uid)
            user.name = user_details["name"]
            user.github_id = user_details["id"]
        elif login_type == "orcid-oauth":
            user_details = session["orcid-details"]
            user = User(user_id = uid)
            user.name = user_details["name"]
            user.orcid = user_details["orcid"]
        return user

    def login_github_user(access_token):
        import requests, flask
        url = "https://api.github.com/user"
        parameters = { "access_token": access_token}
        result = requests.get(url, params=parameters)
        result_json = result.json()
        return result_json
