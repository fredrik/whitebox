import sys
import json
import hashlib

import requests
from pyelasticsearch import ElasticSearch


ES = 'http://localhost:9200/'
index_name = 'feed'



# hacks ahoy!
if __name__ == '__main__':

	if not len(sys.argv) == 2:
		print 'usage: {} <access_token>'.format(sys.argv[0])
		sys.exit(1)

	access_token = sys.argv[1]
	md5_of_token = hashlib.md5(access_token).hexdigest()
	print 'access_token:', access_token

	es = ElasticSearch(ES)

	print 'hello facebook'
	response = requests.get("https://graph.facebook.com/me/feed?access_token={}&limit=1000000".format(access_token))
	response.raise_for_status()  # or bust
	print 'reply!'

	data = json.loads(response.text)
	stream = data['data']
	assert len(stream) > 0

	for post in stream:
		post['fb'] = md5_of_token
		es.index(index_name, 'facebook', post)

	print 'indexing: done.'
	print 'thanks for playing.'
