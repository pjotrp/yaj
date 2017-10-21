from flask import Flask, jsonify, request
from datetime import datetime
import ipfsapi
import datetime

app = Flask(__name__)
api = ipfsapi.connect('127.0.0.1', 5001)

"""
Accepts an object name (for now a file on the local path) and store it on IPFS
Returns a dict with the object name and the IPFS hash
"""
@app.route("/store/put/<obj>", methods=['POST'])
def put(obj):
    if request.methd == 'POST':
        result = api.add(obj)
        return result

"""
Receives a name (either a local IPFS hash or a IPNS path) and resolve it to
an IPFS hash
"""
@app.route("/store/resolve/<name>",methods=['GET'])
def resolve(name):
    if request.method == 'GET':
        path = api.resolve(name)
        return path


"""
Takes an IPFS path of an object and publish it on IPNS.
Returns a dict with the IPNS hash and the IPFS path pointing to it
"""
@app.route("/store/publish/<obj_path>",methods=['POST'])
def publish(obj_path):
    if request.method == 'POST':
        result = api.name_publish(obj_path)
        return result



