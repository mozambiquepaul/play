import os
import tweepy
import openai
import re
from tweepy import Stream
from tweepy.streaming import Stream
from tweepy import OAuth2BearerHandler

# Set up Twitter API authentication
bearer_token = os.environ['TWITTER_BEARER_TOKEN']
auth = OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

# Set up OpenAI API authentication
openai.api_key = os.environ['OPENAI_API_KEY']

# Define a listener for DMs
class DMListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=auth, async=True)

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'direct_message' in data:
            message = data['direct_message']['text']
            sender_id = data['direct_message']['sender_id']
            response = generate_response(message)
            send_direct_message(response, sender_id)

    def on_error(self, status_code):
        print(f"DMListener Error: {status_code}")
        return False

# Define a listener for mentions
class MentionListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=auth, async=True)

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'text' in data:
            message = data['text']
            sender_id = data['user']['id_str']
            response = generate_response(message)
            send_direct_message(response, sender_id)

    def on_error(self, status_code):
        print(f"MentionListener Error: {status_code}")
        return False

# Define function to generate a response using OpenAI
def generate_response(message):
    # Add your OpenAI API code here to generate a response based on the message
    response = "This is the response from OpenAI."
    return response

# Define function to send a direct message
def send_direct_message(message, recipient_id):
    api.send_direct_message(recipient_id, message)

# Start listening for DMs and mentions
dm_listener = DMListener()
dm_listener.filter(track=['@HobbleStepN'])

mention_listener = MentionListener()
mention_listener.filter(track=['@HobbleStepN'])
