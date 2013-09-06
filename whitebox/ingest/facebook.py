import json
import requests
from pyelasticsearch import ElasticSearch


access_token = 'CAAGTx1WBwzUBADXYe5YeMYXzyGg5P6P88tSi6kZCYZCx1I7F1auU54hZBSBBlZBiz9IQJrOFxJdAMvVhbQGdisbDdNcNc4U62hBCojSEWPS3NphAaeqv9cI7zHtiHkZCD1dcBQqLNhjEZC5pspM8fjIfqoNkiajfiAEMQs2pPxk20TpdiVx9ZAT'

ES = 'http://localhost:9200/'
index_name = 'facebook_christos'



# hacks ahoy!
if __name__ == '__main__':
	es = ElasticSearch(ES)

	print 'hello facebook'
	response = requests.get("https://graph.facebook.com/me/feed?access_token={}&limit=1000000".format(access_token))
	response.raise_for_status()  # or bust
	print 'reply!'

	data = json.loads(response.text)
	stream = data['data']
	assert len(stream) > 0

	for post in stream:
		es.index(index_name, 'facebook', post)

	print 'indexing: done.'
	print 'thanks for playing.'
