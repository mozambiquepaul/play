import tweepy

# Fill in your own keys and secrets
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate with Tweepy
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret)

# Test authentication by retrieving your user timeline
api = tweepy.API(auth)
timeline = api.user_timeline(count=10)

# Print out the tweet text from your user timeline
for tweet in timeline:
    print(tweet.text)
