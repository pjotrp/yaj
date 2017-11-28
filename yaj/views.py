from flask import send_from_directory, request, make_response, redirect, url_for, session
import sys
import traceback
import datetime
import logging

from yaj import app
from yaj.config import YAJ_WEB_ASSETS_DIR, YAJ_DIR, YAJ_SECRET_KEY, ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

from elasticsearch import Elasticsearch, TransportError

from flask_login import LoginManager, login_user, logout_user

from yaj.users import UserManager, User

logger = logging.getLogger('publish')

# ---- LoginManager ----
manager = LoginManager();
manager.init_app(app)

@manager.user_loader
def load_user(user_id):
    return UserManager.get(user_id, session.get("login-type"))

# ---- MAKO templating

from mako.template import Template
from mako.lookup import TemplateLookup

if app.secret_key == None:
    app.secret_key = YAJ_SECRET_KEY
mylookup = TemplateLookup(directories=['yaj/templates'], module_directory='/tmp/mako_modules')

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)

# ---- Error handling

@app.errorhandler(Exception)
def handle_bad_request(e):
    err_msg = str(e)
    logger.error(err_msg)
    logger.error(request.url)
    # get the stack trace and send it to the logger
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logger.error(traceback.format_exc())
    now = datetime.datetime.utcnow()
    time_str = now.strftime('%l:%M%p UTC %b %d, %Y')
    formatted_lines = [request.url + " ("+time_str+")"]+traceback.format_exc().splitlines()
    # resp = make_response(render_template("error.html",message=err_msg,stack=formatted_lines,error_image=animation,version=GN_VERSION))
    return serve_template("error.mako",message=err_msg,stack=formatted_lines,menu={"Error":"active"})

# ---- Issues from filesystem
def get_issues():
    from os import listdir
    from os.path import isfile, join
    issues_dir = YAJ_DIR + "/doc/issues/"
    files = [f for f in listdir(issues_dir) if isfile(join(issues_dir, f)) and f.endswith(".jsonld")]
    return map(get_issues_tags_and_urls, files)

def get_issues_tags_and_urls(filename):
    name = filename[:-7]
    tag = " ".join(str(x) for  x in map(lambda s: s.strip().title(), name.split("_")))
    return { "tag": tag, "url": "/issue/"+name }

# ---- Comments from and to Elasticsearch
def get_issue_comments(issue):
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST
        , "port": ELASTICSEARCH_PORT}])
    comments = []
    try:
        response = es.search(
            index = "comments",
            doc_type = issue,
            body = { "query": { "match_all": {} }
                     , "sort": { "posted_on": { "order": "asc" }}
                     , "size": 10000
            })
        comments = sorted(
            list(map(lambda c: convertCommentDate(c["_source"]), response["hits"]["hits"])),
            key = lambda x: x["posted_on"])
    except TransportError as te:
        comments = []
    return comments

def convertCommentDate(comment):
    new_comment = comment
    timestamp = comment["posted_on"];
    new_comment["posted_on"] = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return new_comment

def get_author():
    return {
        "@type": "Person",
        "@context": "http://json-ld.org/contexts/person.jsonld",
        "@id": "http://example.com/",
        "name": "Not Set",
        "jobTitle": "A Job Title",
        "nationality": "East Timor",
        "url": "http://domain.tld/",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Guatemala",
            "email": "roxannemiles@plasto.com"
        }
    }

def save_comment(index, doc_type, comment, comment_id):
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST,
        "port": ELASTICSEARCH_PORT
    }])
    es.create(index=index, doc_type=doc_type, body=comment, id=comment_id);

def convertMarkdownToHTML(comment):
    from markdown import markdown
    new_comment = comment
    new_comment["comment_text"] = markdown(comment["comment_text"])
    return new_comment

# ---- Routing

@app.route("/jquery/<path:filename>") # bootstrap CSS and JS
def jquery(filename):
    return send_from_directory(YAJ_WEB_ASSETS_DIR+"/jquery", filename)

@app.route("/bootstrap/<path:filename>") # bootstrap CSS and JS
def bootstrap(filename):
    return send_from_directory(YAJ_WEB_ASSETS_DIR+"/bootstrap", filename)

@app.route("/bootstrap-native/<path:filename>")
def bootstrap_native(filename):
    return send_from_directory(YAJ_WEB_ASSETS_DIR+"/bootstrap-native", filename)

@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(YAJ_DIR+"/static/yaj/css", filename)

@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory(YAJ_DIR+"/static/yaj/images", filename)

@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(YAJ_DIR+"/static/yaj/js", filename)

@app.route("/")
def main_page(**kwargs):
    return serve_template("published.mako", menu = {"Home": "active"}, publish_id = "announce1", no_comments=True)

@app.route("/about.html")
def about():
    return serve_template("published.mako", menu = {"About": "active"}, publish_id = "about", no_comments=True)

@app.route("/issues/")
def issues():
    issues = get_issues()
    return serve_template("list.mako", menu = {"Issues": "active"}, name = "Issue tracker", show_list = issues )

@app.route("/issue/<path:issue>")
def issue(issue):
    import flask
    import flask_login
    comments = list(map(convertMarkdownToHTML, get_issue_comments(issue)))
    return serve_template(
        "issue.mako"
        , menu = {"Issues": "active"}
        , issue_id = issue
        , comments = comments
        , return_to = request.base_url)

@app.route("/add_comment/<path:issue>", methods=["POST"])
def add_comment(issue):
    from time import time, sleep
    from uuid import uuid4
    comment_text = request.form["comment"]
    if not (comment_text is None or comment_text == ""):
        comment_id = str(uuid4())
        comment = {
            "issue_id": issue,
            "comment_id": comment_id,
            "comment_text": comment_text,
            "posted_on": time(),
            "author": get_author()
        }
        save_comment("comments", issue, comment, comment_id)
        sleep(1) # wait a second to allow document to be indexed
    return redirect(url_for("issue", issue=issue))

@app.route("/login", methods = ["GET"])
def login():
    from yaj.config import GITHUB_CLIENT_ID, GITHUB_AUTH_URL, ORCID_CLIENT_ID, ORCID_AUTH_URL
    return_to = request.args.get("return_to")
    session["return-to"] = return_to
    return serve_template(
        "login.mako"
        , menu = {"Login": "active"}
        , client_id = {"github": GITHUB_CLIENT_ID, "orcid": ORCID_CLIENT_ID}
        , auth_url = {"github": GITHUB_AUTH_URL, "orcid": ORCID_AUTH_URL}
        , return_to = return_to
        , base_url = request.url_root)

@app.route("/logout")
def logout():
    session.pop("login-type", None)
    session.pop("orcid-details", None)
    session.pop("local-user-details", None)
    logout_user()
    return redirect("/")

@app.route("/github_auth", methods=["POST", "GET"])
def github_auth():
    from yaj.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
    import requests;
    code = request.args.get("code")
    return_to = request.args.get("return_to") or session.pop("return-to", None) or "/"
    data = {
        "client_id": GITHUB_CLIENT_ID
        , "client_secret": GITHUB_CLIENT_SECRET
        , "code": code
    }
    result = requests.post("https://github.com/login/oauth/access_token", json=data)
    result_dict = {arr[0]:arr[1] for arr in [tok.split("=") for tok in [token for token in result.text.split("&")]]}
    
    github_user = get_github_user_details(result_dict["access_token"])
    user_details = get_user_by_unique_column(
        "github_id"
        , github_user["id"])
    if user_details == None:
        # Create new user
        from uuid import uuid4
        user_details = {
            "user_id": str(uuid4())
            , "name": github_user["name"]
            , "github_id": github_user["id"]
            , "github_url": github_user["html_url"]
        }
        save_user(user_details, user_details["user_id"])
    session["user_id"] = user_details["user_id"]
    login_user(UserManager.get(str(user_details["user_id"])))
    return redirect(return_to)

def get_github_user_details(access_token):
        import requests, flask
        url = "https://api.github.com/user"
        parameters = { "access_token": access_token}
        result = requests.get(url, params=parameters)
        result_json = result.json()
        return result_json

@app.route("/orcid_auth", methods=["POST", "GET"])
def orcid_auth():
    from yaj.config import ORCID_CLIENT_ID, ORCID_CLIENT_SECRET, ORCID_TOKEN_URL
    import json
    import requests;
    code = request.args.get("code")
    error = request.args.get("error")
    if code:
        return_to = request.args.get("return_to") or session.pop("return-to", None) or "/"
        session.pop("return-to", None)
        data = {
            "client_id": ORCID_CLIENT_ID
            , "client_secret": ORCID_CLIENT_SECRET
            , "grant_type": "authorization_code"
            , "code": code
        }
        result = requests.post(ORCID_TOKEN_URL, data=data)
        result_dict = json.loads(result.text)
        user_details = get_user_by_unique_column(
            "orcid"
            , result_dict["orcid"])
        if user_details == None:
            from uuid import uuid4
            from yaj.config import ORCID_AUTH_URL
            user_details = {
                "user_id": str(uuid4())
                , "name": result_dict["name"]
                , "orcid": result_dict["orcid"]
                , "orcid_url": "%s/%s" % (
                    "/".join(ORCID_AUTH_URL.split("/")[:-2]),
                    result_dict["orcid"])
            }
            save_user(user_details, user_details["user_id"])
        session["user_id"] = user_details["user_id"]
        login_user(UserManager.get(str(user_details["user_id"])))
    elif error:
        return_to = url_for("oauth_access_denied", service="ORCID")
    return redirect(return_to)

@app.route("/oauth_access_denied/<path:service>")
def oauth_access_denied(service):
    return serve_template(
        "access_denied.mako"
        , menu = {"Login": "active"}
        , service = service)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        errors = {key:request.args.get(key) for key in request.args}
        entered_data = session.pop("entered_data", None)

        return serve_template(
            "register.mako"
            , menu={"Register": "active"}
            , errors = errors
            , entered_data = entered_data)
    elif request.method == "POST":
        input_state = validate_registration_details(request.form)
        if input_state["status"] == "ok":
            return register_user(request.form)
        else:
            session["entered_data"] = {
                "user-name": request.form["user-name"]
                , "user-email": request.form["user-email"]
            }
            errors = input_state["error_messages"]
            params = "&".join(["%s=%s" % (key, errors[key]) for key in errors])
            return redirect(url_for("register") + "?" + params)
    else:
        raise Exception("We really should never get here...")

def validate_user_name(form, status):
    if form["user-name"] == None or form["user-name"] == "":
        status["status"] = "error"
        status["error_messages"]["user-name"] = "The user's name MUST be provided"
    return status

def validate_user_email(form, status):
    if form["user-email"] == None or form["user-email"] == "":
        status["status"] = "error"
        status["error_messages"]["user-email"] = "The user's email address MUST be provided"
    return status

def validate_user_password(form, status):
    if form["password"] == None or form["password"] == "":
        status["status"] = "error"
        status["error_messages"]["password"] = "The password MUST be provided"
    return status

def confirm_user_passwork(form, status):
    if form["password"] != form["confirm-password"]:
        status["status"] = "error"
        status["error_messages"]["confirm-password"] = "The passwords MUST match"
    return status
    

def validate_registration_details(form):
    status_dict = {
        "status": "ok"
        , "error_messages": {}
    }
    status_dict = validate_user_name(form, status_dict)
    status_dict = validate_user_email(form, status_dict)
    status_dict = validate_user_password(form, status_dict)
    status_dict = confirm_user_password(form, status_dict)
    return status_dict

def register_user(form):
    if user_exists(form["user-email"]):
        return redirect(url_for("register") + "?email=User already exists")
    else:
        from uuid import uuid4
        import bcrypt
        import json
        uid = str(uuid4())
        salt = bcrypt.gensalt()
        user = json.dumps({
            "user_id": uid
            , "name": form["user-name"]
            , "email": form["user-email"]
            , "password": bcrypt.hashpw(
                form["password"].encode("utf-8")
                , salt).decode("utf-8")
            , "salt": salt.decode("utf-8")
        })
        return save_user(user, uid)

def user_exists(email):
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST
        , "port": ELASTICSEARCH_PORT
    }])
    user = None
    try:
        response = es.search(
            index = "users",
            doc_type = "local",
            body = {
                "query": { "match": { "email": email } }
            })
        user = response["hits"]["hits"]
    except TransportError as te:
        pass
    return user

def save_user(user, user_id, index="users", doc_type="local"):
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST
        , "port": ELASTICSEARCH_PORT
    }])
    es.create(index, doc_type, body=user, id=user_id)
    return redirect(url_for("login"))

@app.route("/login_local", methods=["POST"])
def login_local():
    if request.method == "POST":
        login_status = validate_login_details(request.form)
        if login_status["status"] == "ok":
            return_to = request.args.get("return_to") or session.pop("return-to", None) or "/"
            user = get_user_by_email_and_password(
                request.form["user-email"]
                , request.form["password"])
            if user == None:
                return redirect(url_for("login"))
            else:
                session["local-user-details"] = user
                session["login-type"] = "local-auth"
                login_user(UserManager.get(
                    uid = str(user["user_id"])
                    , login_type = "local-auth"))
                return redirect(return_to)
        else:
            return redirect(return_to)
    else:
        raise Exception("Login: Should never get here!")

def validate_login_details(form):
    status_dict = {
        "status": "ok"
        , "error_messages": {}
    }
    status_dict = validate_user_email(form, status_dict)
    status_dict = validate_user_password(form, status_dict)
    return status_dict

def get_user_by_email_and_password(email, password):
    import bcrypt
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST
        , "port": ELASTICSEARCH_PORT
    }])
    try:
        response = es.search(
            index = "users"
            , doc_type = "local"
            , body = {
                "query": { "match": { "email": email } }
            })
        user_details = response["hits"]["hits"][0]["_source"]
        if bcrypt.checkpw(
                password.encode("utf-8")
                , user_details["password"].encode("utf-8")):
            return user_details
    except TransportError as te:
        pass
    return None

def get_user_by_unique_column(column_name, column_value):
    es = Elasticsearch([{
        "host": ELASTICSEARCH_HOST
        , "port": ELASTICSEARCH_PORT
    }])
    user_details = None
    try:
        response = es.search(
            index = "users"
            , doc_type = "local"
            , body = {
                "query": { "match": { column_name: column_value } }
            })
        if len(response["hits"]["hits"]) > 0:
            user_details = response["hits"]["hits"][0]["_source"]
    except TransportError as te:
        pass
    return user_details
