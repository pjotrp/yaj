from yaj.config import YAJ_DIR
from misaka import Markdown, HtmlRenderer

def story(id):
    rndr = HtmlRenderer()
    f = open(YAJ_DIR+"/doc/"+id+".md")
    buf = f.read()
    f.close
    md = Markdown(rndr)
    return md(buf)
