from yaj.config import YAJ_DIR, YAJ_GIT
from misaka import Markdown, HtmlRenderer
import json
from urllib.parse import urlparse
from pygit2 import Repository

class Struct(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


def story_metadata(id):
    f = open(YAJ_DIR+"/doc/"+id+".jsonld")
    buf = f.read()
    f.close
    meta = json.loads(buf, object_hook=Struct)
    # print(meta)
    return meta

from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE, GIT_SORT_TIME

def story(content_uri):
    """Return the text referenced by content_uri. If uri can not be
    resolved it is returned as is. Current allowed scheme is 'git'. The
    netloc 'yaj-dir' resolves to the local source tree.

    """
    o = urlparse(content_uri)
    if o.scheme == 'git' and o.netloc == 'yaj-dir':
        fullpath = YAJ_DIR+'/'+o.path
        repo = Repository(YAJ_GIT)
        index = repo.index
        index.read()
        id = index['yaj'+o.path].id    # from path to object id
        print(id)
        # for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL|GIT_SORT_TIME):
        #     print(commit.commit_time, ' ', commit.message)
        f = open(fullpath)
        buf = f.read()
        f.close
    else:
        raise Exception("Can not parse URI "+content_uri)
    rndr = HtmlRenderer()
    md = Markdown(rndr)
    return md(buf)
