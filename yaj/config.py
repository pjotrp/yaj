import os
import sys
import yaj.kjson as kjson

YAJ_DIR     = os.path.dirname(os.path.realpath(__file__))
YAJ_CSS_DIR = YAJ_DIR+"/static/yaj/css"
YAJ_GIT     = os.path.dirname(YAJ_DIR)

print(YAJ_GIT)

import yaj.uri as uri

if len(sys.argv) == 2:
    configfn = sys.argv[1]
    CONFIG = kjson.loadf(configfn)
    YAJ_WEB_ASSETS_DIR = uri.resolve_to_path(CONFIG.web_assets_dir)

env_web_assets_dir = os.environ.get('WEB_ASSETS_DIR')
if env_web_assets_dir:
    YAJ_WEB_ASSETS_DIR = env_web_assets_dir

if YAJ_WEB_ASSETS_DIR == None or not os.path.isdir(YAJ_WEB_ASSETS_DIR):
    raise Exception("No path found for "+YAJ_WEB_ASSETS_DIR+" (set WEB_ASSETS_DIR)")

if not os.path.isdir(YAJ_CSS_DIR):
    raise "No path found for YAJ_CSS_DIR"+YAJ_CSS_DIR

env_github_client_id = os.environ.get("GITHUB_CLIENT_ID")
if env_github_client_id:
    GITHUB_CLIENT_ID = env_github_client_id
elif CONFIG.get("github_client_id"):
    GITHUB_CLIENT_ID = CONFIG["github_client_id"]
else:
    raise Exception("Github client ID is not configured")

env_github_client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
if env_github_client_secret:
    GITHUB_CLIENT_SECRET = env_github_client_secret
elif CONFIG.get("github_client_secret"):
    GITHUB_CLIENT_SECRET = CONFIG["github_client_secret"]
else:
    raise Exception("Github client secret is not configured")

env_yaj_secret_key = os.environ.get("YAJ_SECRET_KEY")
if env_yaj_secret_key:
    YAJ_SECRET_KEY = env_yaj_secret_key
elif CONFIG.get("yaj_secret_key"):
    YAJ_SECRET_KEY = CONFIG.get("yaj_secret_key")
else:
    raise Exception("Please set the YAJ_SECRET_KEY environment variable, or provide it in config file.")
