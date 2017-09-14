import os
import sys
import yaj.kjson as kjson
import yaj.uri as uri

if len(sys.argv) == 2:
    configfn = sys.argv[1]
    CONFIG = kjson.loadf(configfn)
    YAJ_WEB_ASSETS_DIR = uri.resolve_to_path(CONFIG.web_assets_dir)

env_web_assets_dir = os.environ.get('YAJ_WEB_ASSETS_DIR')
if env_web_assets_dir:
    YAJ_WEB_ASSETS_DIR = env_web_assets_dir

if YAJ_WEB_ASSETS_DIR == None or not os.path.isdir(YAJ_WEB_ASSETS_DIR):
    raise Exception("No path found for "+YAJ_WEB_ASSETS_DIR+" (set YAJ_WEB_ASSETS_DIR)")

YAJ_DIR     = os.path.dirname(os.path.realpath(__file__))
YAJ_CSS_DIR = YAJ_DIR+"/static/yaj/css"
YAJ_GIT     = os.path.dirname(YAJ_DIR)

print(YAJ_CSS_DIR)

if not os.path.isdir(YAJ_CSS_DIR):
    raise "No path found for YAJ+CSS_DIR"+YAJ_CSS_DIR
