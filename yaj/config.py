import os

YAJ_WEB_DIR = os.environ.get('YAJ_WEB_DIR')

if YAJ_WEB_DIR == None or not os.path.isdir(YAJ_WEB_DIR):
    raise "No path found for "+YAJ_WEB_DIR+" (set YAJ_WEB_DIR)"

YAJ_DIR     = os.path.dirname(os.path.realpath(__file__))
YAJ_CSS_DIR = YAJ_DIR+"/static/yaj/css"
YAJ_GIT     = os.path.dirname(YAJ_DIR)

print(YAJ_CSS_DIR)

if not os.path.isdir(YAJ_CSS_DIR):
    raise "No path found for YAJ+CSS_DIR"+YAJ_CSS_DIR
