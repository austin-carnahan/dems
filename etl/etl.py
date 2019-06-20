import tweepy as tw
from pymongo import MongoClient
import json
import logging
from settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from geo import filter_geo

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('This is a log message.')


#~ # Connect to our db
#~ client = MongoClient("mongodb://my_db:27017")
#~ db = client.tweetDB
#~ tweets = db["Tweets"]

# Some lists and dictionaries of terms we're interested in
TERMS = ["#KamalaHarris", "#ElizabethWarren", "#JoeBiden", "#BernieSanders",]


class StreamListener(tw.StreamListener):
	"""tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API to collect tweets in real-time.
    """
    
	def on_connect(self):
		"""Called when the connection is made"""
		logging.info("You're connected to the streaming server.")

	def on_error(self, status_code):
		"""This is called when an error occurs"""
		logging.error('Error: ' + repr(status_code))
		return False

	def on_data(self, data):
		logging.info("data recieved...")
		"""This will be called each time we receive stream data"""
		client = MongoClient("mongodb://my_db:27017")
		db = client.testDB

		# Decode JSON
		datajson = json.loads(data)

		# I'm only storing tweets in English. I stored the data for these tweets in a collection
		# called 'testDB_collection' of the 'testDB' database. If
		# 'testDB_collection' does not exist it will be created for you.
		if "lang" in datajson and datajson["lang"] == "en":
			logging.info("saving data...")
			db.testDB_collection.insert_one(datajson)

if __name__ == "__main__":
	# These are provided to you through the Twitter API after you create a account
	consumer_key = CONSUMER_KEY
	consumer_secret = CONSUMER_SECRET
	access_token = ACCESS_TOKEN
	access_token_secret = ACCESS_TOKEN_SECRET

	auth1 = tw.OAuthHandler(consumer_key, consumer_secret)
	auth1.set_access_token(access_token, access_token_secret)

	stream_listener = StreamListener(api=tw.API(wait_on_rate_limit=True))
	stream = tw.Stream(auth=auth1, listener=stream_listener)
	stream.filter(track=TERMS)
