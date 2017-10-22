IPFS Backend
============


Experimental backend with [IPFS](https://ipfs.io) using the official [IPFS Python API](https://github.com/ipfs/py-ipfs-api)

First you need to install IPFS: https://dist.ipfs.io/#go-ipfs

Then start the IPFS deamon:

```
ipfs daemon
```


To test
-------

```
pip install -r requirements.txt
python yaj_ipfs.py & 
```

Then you can create a simple test file:

```
echo "Ready for Interplanetary filesystem!" > test.txt
curl -X PUT http://127.0.0.1:5000/store/put/test.txt
```

You can then test other actions using the IPFS hash returned by the put

```
curl -X GET http://127.0.0.1:5000/store/list/$HASH
curl -X GET http://127.0.0.1:5000/store/get/$HASH
```

