import os
import tweepy
import requests
from requests.structures import CaseInsensitiveDict


# Authenticate to Twitter
auth = tweepy.OAuth2BearerHandler(os.environ['TWITTER_BEARER_TOKEN'])
api = tweepy.API(auth)

# Set up ChatGPT API credentials
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {os.environ['OPENAI_API_SECRET_KEY']}"

def generate_response(prompt):
    data = """
    {
        """
    data += f'"prompt": "{prompt}",'
    data += """
        "temperature": 0.7,
        "max_tokens": 60,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    """

    resp = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, data=data)

    if resp.status_code != 200:
        raise ValueError("Failed to generate response from ChatGPT API")

    response_text = resp.json()["choices"][0]["text"].strip()
    return response_text

# Create a stream listener
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Check if the tweet is a mention and not a retweet
        if status.in_reply_to_screen_name == 'HobbleStepN' and not status.retweeted:
            # Extract the text of the tweet
            text = status.text.lower()
            
            # Generate a clown-themed response using ChatGPT API
            prompt = f"clown response to {text}"
            response = generate_response(prompt)
            reply_text = f"@{status.author.screen_name} {response}"
            
            # Post the response as a reply to the original tweet
            api.update_status(status=reply_text, in_reply_to_status_id=status.id)
            
        # Check if the tweet is a direct message
        elif status.in_reply_to_screen_name is None:
            # Extract the text of the direct message
            text = status.text.lower()
            
            # Generate a clown-themed response using ChatGPT API
            prompt = f"clown response to {text}"
            response = generate_response(prompt)
            
            # Send the response as a direct message
            api.send_direct_message(status.author.id, text=response)

    def on_error(self, status_code):
        print(f"Error: {status_code}")

# Create a stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Start the stream
myStream.filter(track=['HobbleStepN'])

