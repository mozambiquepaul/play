import os
import tweepy
import openai
from tweepy import Stream, OAuth2BearerHandler
from tweepy.streaming import StreamListener

# Twitter API credentials
CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# OpenAI API credentials
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Authenticate with Twitter API
auth = tweepy.OAuth2BearerHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

# Authenticate with OpenAI API
openai.api_key = OPENAI_API_KEY

# Define a listener to handle incoming DMs and mentions
class ClownStreamListener(StreamListener):
    
    def on_direct_message(self, status):
        # Generate a response to the DM using OpenAI
        response = openai.Completion.create(
            engine="davinci",
            prompt=status.message_create["message_data"]["text"],
            temperature=0.5,
            max_tokens=100,
            n=1,
            stop=None,
            )
        
        # Send the generated response back to the user
        user_id = status.message_create["sender_id"]
        api.send_direct_message(user_id, text=response.choices[0].text)
        
    def on_status(self, status):
        # Check if the tweet mentions our username
        if api.get_user(status.user.id_str).screen_name == "HobbleStepN":
            # Generate a response to the tweet using OpenAI
            response = openai.Completion.create(
                engine="davinci",
                prompt=status.text,
                temperature=0.5,
                max_tokens=100,
                n=1,
                stop=None,
                )
            
            # Send the generated response back to the user
            api.update_status(
                status="@" + status.user.screen_name + " " + response.choices[0].text,
                in_reply_to_status_id=status.id_str,
            )

# Create a stream to listen for incoming DMs and mentions
stream_listener = ClownStreamListener()
stream = Stream(auth, stream_listener)
stream.filter(track=["@HobbleStepN"], is_async=True)
