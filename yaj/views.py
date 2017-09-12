from yaj import app
# from flask import render_template

# ---- MAKO templating

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['yaj/templates'], module_directory='/tmp/mako_modules')

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)

# ---- Routing

@app.route("/test")
def test_page():
    return "Yet another journal! Well, early days!"

@app.route("/")
def main_page(**kwargs):
    return serve_template("index.mako", name = "Pjotr")
