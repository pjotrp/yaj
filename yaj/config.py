import os

YAJ_WEB_PATH = os.environ.get('YAJ_WEB_PATH')

print(YAJ_WEB_PATH)

if YAJ_WEB_PATH == None or not os.path.isdir(YAJ_WEB_PATH):
    raise "No path found for "+YAJ_WEB_PATH+" (set YAJ_WEB_PATH)"
