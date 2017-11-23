from flask import send_from_directory, request, make_response, redirect, url_for, session
import sys
import traceback
import datetime
import logging

from yaj import app
from yaj.config import YAJ_WEB_ASSETS_DIR, YAJ_DIR, YAJ_SECRET_KEY

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
    return serve_template("error.mako",message=err_msg,stack=formatted_lines)

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
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
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
    es = Elasticsearch([{"host": "localhost", "port": 9200}])
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
    logout_user()
    return redirect("/")

@app.route("/github_auth", methods=["POST", "GET"])
def github_auth():
    from yaj.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
    import requests;
    code = request.args.get("code")
    return_to = request.args.get("return_to") or session["return-to"] or "/"
    session.pop("return-to", None)
    data = {
        "client_id": GITHUB_CLIENT_ID
        , "client_secret": GITHUB_CLIENT_SECRET
        , "code": code
        # , "redirect_uri": "The URL in your application where users are sent after authorization"
        # , "state": "The unguessable random string you provided in Step 1"
    }
    result = requests.post("https://github.com/login/oauth/access_token", json=data)
    result_dict = {arr[0]:arr[1] for arr in [tok.split("=") for tok in [token for token in result.text.split("&")]]}
    session["login-type"] = "github-oauth"
    login_user(UserManager.get(str(result_dict["access_token"]), "github-oauth"))
    return redirect(return_to)

@app.route("/orcid_auth", methods=["POST", "GET"])
def orcid_auth():
    from yaj.config import ORCID_CLIENT_ID, ORCID_CLIENT_SECRET, ORCID_TOKEN_URL
    import json
    import requests;
    code = request.args.get("code")
    error = request.args.get("error")
    if code:
        return_to = request.args.get("return_to") or session["return-to"] or "/"
        session.pop("return-to", None)
        data = {
            "client_id": ORCID_CLIENT_ID
            , "client_secret": ORCID_CLIENT_SECRET
            , "grant_type": "authorization_code"
            , "code": code
        }
        result = requests.post(ORCID_TOKEN_URL, data=data)
        result_dict = json.loads(result.text)
        session["login-type"] = "orcid-oauth"
        session["orcid-details"] = result_dict
        login_user(UserManager.get(str(result_dict["access_token"]), "orcid-oauth"))
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
        return serve_template(
            "register.mako"
            , menu={"Register": "active"}
            , errors = errors)
    elif request.method == "POST":
        input_state = validate_registration_details(request.form)
        if input_state["status"] == "ok":
            return register_user()
        else:
            errors = input_state["error_messages"]
            params = "&".join(["%s=%s" % (key, errors[key]) for key in errors])
            return redirect(url_for("register") + "?" + params)
    else:
        raise Exception("We really should never get here...")

def validate_registration_details(form):
    status_dict = {
        "status": "ok"
        , "error_messages": {}
    }

    if form["user-name"] == None or form["user-name"] == "":
        status_dict["status"] = "error"
        status_dict["error_messages"]["user-name"] = "The user's name MUST be provided"

    if form["user-email"] == None or form["user-email"] == "":
        status_dict["status"] = "error"
        status_dict["error_messages"]["user-email"] = "The user's email address MUST be provided"

    if form["password"] == None or form["password"] == "":
        status_dict["status"] = "error"
        status_dict["error_messages"]["password"] = "The password MUST be provided"

    if form["password"] != form["confirm-password"]:
        status_dict["status"] = "error"
        status_dict["error_messages"]["confirm-password"] = "The passwords MUST match"

    return status_dict

def register_user():
    raise Exception("Not Implemented!")
