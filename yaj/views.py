from flask import send_from_directory, request, make_response, redirect, url_for
import sys
import traceback
import datetime
import logging

from yaj import app
from yaj.config import YAJ_WEB_ASSETS_DIR, YAJ_DIR

from elasticsearch import Elasticsearch, TransportError

logger = logging.getLogger('publish')

# ---- MAKO templating

from mako.template import Template
from mako.lookup import TemplateLookup

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
    comments = list(map(convertMarkdownToHTML, get_issue_comments(issue)))
    user = flask.g.get("user") # Doesn't work. Use sessions
    return serve_template(
        "issue.mako"
        , menu = {"Issues": "active"}
        , issue_id = issue
        , comments = comments
        , user = user
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
    from yaj.config import GITHUB_CLIENT_ID
    return_to = request.args.get("return_to")
    return serve_template(
        "login.mako"
        , menu = {"Login": "active"}
        , client_id = GITHUB_CLIENT_ID
        , return_to = return_to
        , base_url = request.url_root)

@app.route("/github_auth", methods=["POST", "GET"])
def github_auth():
    from yaj.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
    import requests;
    code = request.args.get("code")
    return_to = request.args.get("return_to")
    data = {
        "client_id": GITHUB_CLIENT_ID
        , "client_secret": GITHUB_CLIENT_SECRET
        , "code": code
        # , "redirect_uri": "The URL in your application where users are sent after authorization"
        # , "state": "The unguessable random string you provided in Step 1"
    }
    result = requests.post("https://github.com/login/oauth/access_token", json=data)
    result_dict = {arr[0]:arr[1] for arr in [tok.split("=") for tok in [token for token in result.text.split("&")]]}
    return redirect(
        url_for("login_github_user", access_token=result_dict["access_token"])
        + "?return_to=" + return_to)

@app.route("/login_github_user/<access_token>", methods = ["GET"])
def login_github_user(access_token):
    import requests, flask
    url = "https://api.github.com/user"
    parameters = { "access_token": access_token}
    result = requests.get(url, params=parameters)
    result_json = result.json()
    flask.g.user = { # Doesn't work. Use sessions
        "login-type": "github-oauth"
        , "user-data": result_json
        , "access_token": access_token
    }
    return_to = request.args.get("return_to")
    return redirect(return_to)
