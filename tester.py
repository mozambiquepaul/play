import os
import tweepy
import openai
from tweepy.streaming import StreamListener
from tweepy import OAuth2BearerHandler

openai.api_key = os.environ['OPENAI_API_KEY']
auth = tweepy.OAuth2BearerHandler(access_token=os.environ['TWITTER_BEARER_TOKEN'])

# Authenticate to Twitter API
auth = tweepy.OAuth2BearerHandler(access_token=os.environ['TWITTER_BEARER_TOKEN'])

# Connect to Twitter API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class MyStreamListener(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret,
            tweet_mode='extended'
        )

    def on_status(self, status):
        # code to handle new tweet

    def on_error(self, status_code):
        # code to handle errors


class DMListener(StreamListener):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self)

    def on_direct_message(self, status):
        sender_id = status.direct_message.sender_id_str
        message = status.direct_message.text

        # code to respond to DM with clown-themed response


class MentionListener(StreamListener):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self)

    def on_status(self, status):
        if status.user.screen_name == 'HobbleStepN':
            message = status.text

            # code to respond to mention with clown-themed response


dm_listener = DMListener()
mention_listener = MentionListener()

dm_stream = tweepy.Stream(auth=auth, listener=dm_listener)
mention_stream = tweepy.Stream(auth=auth, listener=mention_listener)

dm_stream.userstream(_with='user')
mention_stream.filter(track=['@HobbleStepN']) 
