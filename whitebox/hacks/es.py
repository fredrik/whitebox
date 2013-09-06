from pyelasticsearch import ElasticSearch


def go():
	es = ElasticSearch('http://localhost:9200/')
	es.index("tweets", "tweet", {
		"id": 1010,
		"text": "Oh my, a tweet."
	}, id=1)
	es.refresh("tweets")

	
if __name__ == '__main__':
	go()
