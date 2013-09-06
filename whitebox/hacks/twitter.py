from twython import Twython
from time import sleep

APP_KEY = 'FmhCchsssW7xswYsgxBEDw'
APP_SECRET = 'dADr1rlgVAISYWb6qBr3Pu364pqCA8b1LqLHWcJNxfE'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

print 'access token:', ACCESS_TOKEN

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)


max_id = None

while True:
	timeline_items = twitter.get_user_timeline(screen_name='mollerstrand', count=200, max_id=max_id)

	if not timeline_items:
		print 'done, I think.'
		break

	print 'got', len(timeline_items), 'tweets.'

	for item in timeline_items:
		print item['id'], item['created_at'], item['text']

	max_id = timeline_items[-1]['id'] - 1
	print 'max id:', max_id
	sleep(2)
