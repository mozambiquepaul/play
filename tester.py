import os
import tweepy
import openai
from tweepy import OAuth2BearerHandler
from openai import api_key

# Twitter API keys and secrets
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Authenticate with Twitter API
auth = tweepy.OAuth2BearerHandler(os.environ['TWITTER_BEARER_TOKEN'])
api = tweepy.API(auth)

# Define listener for stream
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # If tweet is a mention, respond with a clown-themed response
        if status.in_reply_to_screen_name == 'HobbleStepN':
            user_id = status.user.id_str
            screen_name = status.user.screen_name
            tweet_id = status.id_str
            tweet_text = status.text.lower()
            response = generate_response(tweet_text)
            api.update_status(
                status=f'@{screen_name} {response}',
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            print(f'Responded to mention from @{screen_name}: {tweet_text}')
            
        # If tweet is a direct message, respond with a clown-themed response
        elif hasattr(status, 'direct_message'):
            user_id = status.direct_message.sender_id_str
            screen_name = status.direct_message.sender_screen_name
            message_id = status.direct_message.id_str
            message_text = status.direct_message.text.lower()
            response = generate_response(message_text)
            api.send_direct_message(
                recipient_id=user_id,
                text=response
            )
            print(f'Responded to DM from @{screen_name}: {message_text}')
        
    def on_error(self, status_code):
        if status_code == 420:
            return False
        
# Generate response using OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()

# Stream tweets
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=auth, listener=myStreamListener)
myStream.filter(track=['@HobbleStepN'], is_async=True)
