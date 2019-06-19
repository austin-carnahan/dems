import tweepy as tw
from pymongo import MongoClient
import json
from .settings import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
from .geo import filter_geo


# Connect to our db
client = MongoClient("mongodb://my_db:27017")
db = client.tweetDB
tweets = db["Tweets"]

# Some lists and dictionaries of terms we're interested in
TERMS = ["#KamalaHarris", "#ElizabethWarren", "#JoeBiden", "#BernieSanders",]


class StreamListener(tweepy.StreamListener):
	"""tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API to collect tweets in real-time.
    """
    
    def on_connect(self):
        """Called when the connection is made"""
        print("You're connected to the streaming server.")

    def on_error(self, status_code):
        """This is called when an error occurs"""
        print('Error: ' + repr(status_code))
        return False

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        client = MongoClient("mongodb://my_db:27017")
        db = client.testDB

        # Decode JSON
        datajson = json.loads(data)

        # I'm only storing tweets in English. I stored the data for these tweets in a collection
        # called 'testDB_collection' of the 'testDB' database. If
        # 'testDB_collection' does not exist it will be created for you.
        if "lang" in datajson and datajson["lang"] == "en":
            db.testDB_collection.insert_one(datajson)

if __name__ == "__main__":
    # These are provided to you through the Twitter API after you create a account
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET

    auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth1.set_access_token(access_token, access_token_secret)

    # LOCATIONS are the longitude, latitude coordinate corners for a box that restricts the
    # geographic area from which you will stream tweets. The first two define the southwest
    # corner of the box and the second two define the northeast corner of the box.
    LOCATIONS = [-124.7771694, 24.520833, -66.947028, 49.384472,     # Contiguous US
                 -164.639405, 58.806859, -144.152365, 71.76871,      # Alaska
                 -160.161542, 18.776344, -154.641396, 22.878623]     # Hawaii

    stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    stream = tweepy.Stream(auth=auth1, listener=stream_listener)
    stream.filter(track=TERMS)
