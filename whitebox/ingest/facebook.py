import sys
import json
import hashlib

import requests
import pyelasticsearch
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

	es = ElasticSearch(ES)

	try:
		print 'purging old posts for this user.'
		feed_for_this_token = es.search('fb:{}'.format(md5_of_token), index=index_name, size=10000)['hits']['hits']
		for doc in feed_for_this_token:
			es.delete(index_name, 'facebook', doc['_id'])
	except pyelasticsearch.exceptions.ElasticHttpNotFoundError:
		pass

	print 'hello facebook'
	response = requests.get("https://graph.facebook.com/me/feed?access_token={}&limit=1000000".format(access_token))
	response.raise_for_status()  # or bust
	print 'reply!'

	data = json.loads(response.text)
	stream = data['data']
	assert len(stream) > 0

	print 'fetched', len(stream), 'posts.'

	for post in stream:
		post['fb'] = md5_of_token
		es.index(index_name, 'facebook', post)

	print 'indexing: done.'
	print 'thanks for playing.'
