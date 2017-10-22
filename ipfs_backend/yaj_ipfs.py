from flask import Flask, request
import ipfsapi

app = Flask(__name__)
api = ipfsapi.connect('127.0.0.1', 5001)

"""
Accepts an object name (for now a file on the local path) and store it on IPFS
Returns a dict with the object name and the IPFS hash
"""
@app.route("/store/put/<obj>", methods=['PUT'])
def put(obj):
    if request.method == 'PUT':
        result = api.add(obj)
        print(result)
        return "Put request processed: {0}".format(result)


"""
Lists hashes linked to an object hash, returns a dict
"""
@app.route("/store/list/<obj_hash>",methods=['GET'])
def list(obj_hash):
    if request.method == 'GET':
        result = api.ls(obj_hash)
        print(result)
        return "Get request processed: {0}".format(result)


"""
Accepts an object IPFS hash and download a local copy of that object
"""
@app.route("/store/get/<obj_hash>",methods=['GET'])
def get(obj_hash):
    if request.method == 'GET':
        result = api.get(obj_hash)
        return "Get request processed: {0}".format(result)

"""
Receives a name (either a local IPFS hash or a IPNS path) and resolve it to
an IPFS hash
"""
@app.route("/store/resolve/<name>",methods=['GET'])
def resolve(name):
    if request.method == 'GET':
        path = api.resolve("/ipfs/{0}".format(name))
        return "Resolve request processed: {0}".format(path)

"""
Takes an IPFS path of an object and publish it on IPNS.
Returns a dict with the IPNS hash and the IPFS path pointing to it
"""
@app.route("/store/publish/<obj_path>",methods=['POST'])
def publish(obj_path):
    if request.method == 'POST':
        print(obj_path)
        result = api.name_publish(obj_path)
        return "Publish request processed: {0}".format(result)



if __name__ == "__main__":
    app.run()
