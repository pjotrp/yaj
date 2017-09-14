from yaj.config import YAJ_DIR
from misaka import Markdown, HtmlRenderer
import json
from urllib.parse import urlparse

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



def story(content_uri):
    """Return the text referenced by content_uri. If uri can not be
    resolved it is returned as is. Current allowed scheme is 'git'. The
    netloc 'yaj-dir' resolves to the local source tree.

    """
    o = urlparse(content_uri)
    if o.scheme == 'git' and o.netloc == 'yaj-dir':
        f = open(YAJ_DIR+'/'+o.path)
        buf = f.read()
        f.close
    else:
        raise Exception("Can not parse URI "+content_uri)
    rndr = HtmlRenderer()
    md = Markdown(rndr)
    return md(buf)
