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

# ---- Github Configuration ----
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

env_github_auth_url = os.environ.get("GITHUB_AUTH_URL")
if env_github_auth_url:
    GITHUB_AUTH_URL = env_github_auth_url
elif CONFIG.get("github_auth_url"):
    GITHUB_AUTH_URL = CONFIG["github_auth_url"]
else:
    raise Exception("Github authorisation URL is not configured")
# ---- END: Github Configuration ----

env_yaj_secret_key = os.environ.get("YAJ_SECRET_KEY")
if env_yaj_secret_key:
    YAJ_SECRET_KEY = env_yaj_secret_key
elif CONFIG.get("yaj_secret_key"):
    YAJ_SECRET_KEY = CONFIG.get("yaj_secret_key")
else:
    raise Exception("Please set the YAJ_SECRET_KEY environment variable, or provide it in config file.")


# ---- ORCID Configuration ----
env_orcid_client_id = os.environ.get("ORCID_CLIENT_ID")
if env_orcid_client_id:
    ORCID_CLIENT_ID = env_orcid_client_id
elif CONFIG.get("orcid_client_id"):
    ORCID_CLIENT_ID = CONFIG["orcid_client_id"]
else:
    raise Exception("ORCID client ID is not configured")

env_orcid_client_secret = os.environ.get("ORCID_CLIENT_SECRET")
if env_orcid_client_secret:
    ORCID_CLIENT_SECRET = env_orcid_client_secret
elif CONFIG.get("orcid_client_secret"):
    ORCID_CLIENT_SECRET = CONFIG["orcid_client_secret"]
else:
    raise Exception("ORCID client secret is not configured")

env_orcid_auth_url = os.environ.get("ORCID_AUTH_URL")
if env_orcid_auth_url:
    ORCID_AUTH_URL = env_orcid_auth_url
elif CONFIG.get("orcid_auth_url"):
    ORCID_AUTH_URL = CONFIG["orcid_auth_url"]
else:
    raise Exception("ORCID authorisation URL is not configured")

env_orcid_token_url = os.environ.get("ORCID_TOKEN_URL")
if env_orcid_token_url:
    ORCID_TOKEN_URL = env_orcid_token_url
elif CONFIG.get("orcid_token_url"):
    ORCID_TOKEN_URL = CONFIG["orcid_token_url"]
else:
    raise Exception("ORCID token URL is not configured")
# ---- END: ORCID Configuration ----


# ---- Elasticsearch Configuration ----
env_elasticsearch_host = os.environ.get("ELASTICSEARCH_HOST")
if env_elasticsearch_host:
    ELASTICSEARCH_HOST = env_elasticsearch_host
elif CONFIG.get("elasticsearch_host"):
    ELASTICSEARCH_HOST = CONFIG["elasticsearch_host"]
else:
    raise Exception("ELASTICSEARCH_HOST is not configured")

env_elasticsearch_port = os.environ.get("ELASTICSEARCH_PORT")
if env_elasticsearch_port:
    ELASTICSEARCH_PORT = env_elasticsearch_port
elif CONFIG.get("elasticsearch_port"):
    ELASTICSEARCH_PORT = CONFIG["elasticsearch_port"]
else:
    raise Exception("ELASTICSEARCH_PORT is not configured")
# ---- END: Elasticsearch Configuration ----
