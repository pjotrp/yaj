from yaj.config import YAJ_DIR
from misaka import Markdown, HtmlRenderer
import json

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

def story(id):
    rndr = HtmlRenderer()
    f = open(YAJ_DIR+"/doc/"+id+".md")
    buf = f.read()
    f.close
    md = Markdown(rndr)
    return md(buf)
