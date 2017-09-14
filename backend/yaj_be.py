from flask import Flask, jsonify, request
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

#from fask_restful import Resource, Api
import datetime

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class Author:
	def __init__(self, name, familyName, email):
		self.name = name
		self.familyName = familyName
		self.email = email

	def to_json(self):
		return({
		'@context':'http://schema.org',
		'@type':'Person',
		'familyName': self.familyName,
		'givenName': self.name,
		'url':'',
		'email': self.email
		})

class Post:
	def __init__(self, headline, articleBody, about, author, contributor):
		self.headline = headline
		self.articleBody = articleBody
		self.author = author
		self.about = about
		self.contributor = contributor
		self.date = datetime.datetime.now()

	def to_json(self):
		return({
		'@context': 'http://schema.org',
		'@type': 'BlogPosting',
        'headline': self.headline,
        'articleBody': self.articleBody,
        'about': self.about,
        'contributor': self.contributor,
        'author': self.author,
        'dateCreated': self.date
        })

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/author", methods=['POST'])
def newauthor():
	print(request.method)
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			author = Author(data['givenName'], data['familyName'], data['email'])
			es.index(index='dev-yaj', doc_type='author', body=author.to_json())
			return(jsonify(":ok"))
	return(jsonify(":error"))

@app.route("/post", methods=['POST'])
def newpost():
	if request.method == 'POST':
		if request.is_json:
			data = request.get_json()
			search = Search(using=es, index='dev-yaj', doc_type='author')
			response = search.query("match", email=data['email']).execute()
			if response.hits.total==1:
				post = Post(data['headline'], data['articleBody'], data['about'], response.hits[0].meta.id,data['contributor'])
				es.index(index='dev-yaj', doc_type='post', body=post.to_json())
				return(jsonify(":ok"))
			elif response.hits.total>1:
				return(jsonify([":error",":multiusers"]))
			else:
				return(jsonify([":error",":unkown_user"]))
		else:
			return(jsonify([":error",":not_json_request"]))


@app.route("/author/<email>", methods=["GET"])
def author(email):
	if request.method == 'GET':
		search = Search(using=es, index='dev-yaj', doc_type='author')
		response = search.query("match", email=email).execute()
		if response.hits.total == 1:
			return(jsonify(response.hits[0].to_dict()))
	return(jsonify(":error"))

@app.route("/authors", methods=["GET"])
def authors():
	search = Search(using=es, index='dev-yaj', doc_type='author')
	response=search.query("match_all").execute()
	response_json = response.to_dict()['hits']['hits']
	return(jsonify(response_json))


@app.route("/posts", methods=["GET"])
def posts():
	search = Search(using=es, index='dev-yaj', doc_type='post')
	response=search.query("match_all").execute()
	response_json = response.to_dict()['hits']['hits']
	return(jsonify(response_json))

if __name__ == "__main__":
    app.run()
