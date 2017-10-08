from flask import send_from_directory, request, make_response
import sys
import traceback
import datetime
import logging

from yaj import app
from yaj.config import YAJ_WEB_ASSETS_DIR, YAJ_DIR

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

@app.route("/")
def main_page(**kwargs):
    return serve_template("published.mako", menu = {"Home": "active"}, publish_id = "announce1", no_comments=True)

@app.route("/about.html")
def about():
    return serve_template("published.mako", menu = {"About": "active"}, publish_id = "about", no_comments=True)

@app.route("/issues/")
def issues():
    issues = [ { "tag": "issue 1", "url": "/issue/1" } ]
    return serve_template("list.mako", menu = {"Issues": "active"}, name = "Issue tracker", show_list = issues )

@app.route("/issue/<path:issue_num>")
def issue(issue_num):
    issues = [ "create_issue_tracker" ]
    return serve_template("issue.mako",
                          menu = {"Issues": "active"},
                          issue_id = "issues/" + issues[int(issue_num)-1])
