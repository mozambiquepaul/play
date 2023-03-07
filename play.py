import tweepy
import openai
import os
import random

# Retrieve API keys and access tokens from environment variables
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Set up Tweepy API client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set up OpenAI API client
openai.api_key = openai_api_key

# Define function to generate silly response
def generate_response(text):
    prompt = f"Clown themed response to: {text}\nResponse: "
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=60,
        n = 1,
        stop = None,
        timeout = 5,
    )
    return response.choices[0].text.strip()

# Define function to handle mentions
def handle_mention(tweet):
    text = tweet.text.lower()
    username = tweet.user.screen_name
    response_text = generate_response(text)
    api.update_status(f"@{username} {response_text}", tweet.id)

# Set up stream listener to listen for mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.in_reply_to_status_id is not None or status.user.id == api.me().id:
            return
        elif "clown" in status.text.lower():
            api.update_status(
                status="@%s That's right, I'm a clown! 🤡🎉" % status.user.screen_name,
                in_reply_to_status_id=status.id,
            )
        else:
            handle_mention(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False

# Set up stream listener and start listening for mentions
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@YOUR_USERNAME'])
