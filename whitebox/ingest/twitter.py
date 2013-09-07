import os
import sys
import logging
from datetime import datetime

from twython import Twython
from pyelasticsearch import ElasticSearch



# twitter auths
APP_KEY = os.getenv("APP_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

ES = 'http://localhost:9200/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
logger.addHandler(handler)



class TweetEater(object):
	"""
	Process and index tweets.
	"""
	# TODO: make robust, catch ES exceptions, etc
	def __init__(self, screen_name):
		self.screen_name = screen_name
		self.index = 'feed'
		self.type = 'tweet'
		self.es = ElasticSearch(ES)
		self.ingestion_count = 0
	def ingest(self, tweet):
		processed_tweet = self.process(tweet)
		logger.debug(u"indexing %d => %s", processed_tweet['id'], self.index)
		self.es.index(self.index, self.type, processed_tweet, processed_tweet['id'])
		self.ingestion_count += 1
	def process(self, tweet):
		"""Take a raw tweet dict and turn it into an indexable entity."""
		processed_tweet = {
			'id': tweet['id'],
			'raw': tweet,
			'processed_at': datetime.utcnow(),
		}
		return processed_tweet


def fetch_all_tweets(screen_name):
	"""Generator of all tweets from screen_name's timeline."""
	if not APP_KEY or not ACCESS_TOKEN:
		raise Exception("please set the APP_KEY and ACCESS_TOKEN environment variables.")
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
	max_id = None
	while True:
		timeline_items = twitter.get_user_timeline(screen_name=screen_name, count=200, max_id=max_id)
		if not timeline_items:
			break
		logger.debug("fetched %d tweets from %s's timeline.", len(timeline_items), screen_name)
		for item in timeline_items:
			yield item
		# set max_id to ask for the next set of tweets.
		max_id = timeline_items[-1]['id'] - 1



def process_user_timeline(screen_name):
	eater = TweetEater(screen_name)
	logger.info(u'about to process tweets for %s', screen_name)
	for tweet in fetch_all_tweets(screen_name):
		logger.debug('processing %d', tweet['id'])
		eater.ingest(tweet)
	logger.info("ingested %d tweets.", eater.ingestion_count)


if __name__ == '__main__':
	process_user_timeline('mollerstrand')
