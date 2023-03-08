import os
import tweepy
import openai
from dotenv import load_dotenv

load_dotenv()

# Authenticate to Twitter
auth = tweepy.OAuth2BearerHandler(os.environ['TWITTER_BEARER_TOKEN'])
api = tweepy.API(auth)

# Authenticate to OpenAI
openai.api_key = os.environ['OPENAI_API_SECRET_KEY']

# Define the stream listener
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        print(status.text)

# Start the stream listener
myStreamListener = MyStreamListener(api_key, api_secret, access_token, access_token_secret)
myStreamListener.filter(track=['@HobbleStepN'])

# Define a function to generate a response
def generate_response(tweet_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=tweet_text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text

# Define a function to send a reply tweet
def send_reply_tweet(tweet, response_text):
    api.update_status(
        status=response_text,
        in_reply_to_status_id=tweet.id,
        auto_populate_reply_metadata=True,
    )

# Define the stream listener
class MyStreamListener(tweepy.Stream):
    def on_status(self, status):
        if status.in_reply_to_screen_name == 'HobbleStepN':
            response_text = generate_response(status.text)
            send_reply_tweet(status, response_text)

# Start the stream listener
myStreamListener = MyStreamListener(api_key, api_secret, access_token, access_token_secret)
myStreamListener.filter(track=['@HobbleStepN'])
