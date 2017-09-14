import os
from urllib.parse import urlparse

from yaj.config import YAJ_DIR, YAJ_GIT

def resolve_to_path(uri):
    """Turn a URI into a file name, if possible. On failure return uri as is
    """
    o = urlparse(uri)
    print(o)
    path = o.path
    if o.scheme == 'git' and o.netloc == 'yaj-dir':
        path = YAJ_DIR+'/'+o.path
    if o.netloc == '{{HOME}}':
        path = os.environ.get('HOME')+path
    if not os.path.exists(path):
        return uri
    return path
