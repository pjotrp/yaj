import json

class JSONAcces(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

def loadf(filen):
    f = open(filen)
    buf = f.read()
    f.close
    return json.loads(buf, object_hook=JSONAcces)
