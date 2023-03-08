import tweepy
import openai
import os

# Twitter API credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Authenticate with Twitter API
auth = tweepy.OAuth2BearerHandler(access_token)
api = tweepy.API(auth)

# Define a listener class for DMs and mentions
class ClownBotListener(tweepy.Stream):

    def on_direct_message(self, status):
        print(f"Received DM from @{status.sender_screen_name}: {status.text}")
        response = generate_clown_response(status.text)
        send_dm(status.sender_screen_name, response)

    def on_status(self, status):
        if status.in_reply_to_screen_name == "HobbleStepN":
            print(f"Received mention from @{status.user.screen_name}: {status.text}")
            response = generate_clown_response(status.text)
            api.update_status(f"@{status.user.screen_name} {response}", status.id)

# Define a function to generate clown responses using OpenAI's GPT-3
def generate_clown_response(text):
    prompt = f"ClownBot: {text}\nClown:"
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100, n=1,stop=None,temperature=0.5)
    return response.choices[0].text.strip()

# Define a function to send DMs
def send_dm(screen_name, text):
    try:
        api.send_direct_message(screen_name=screen_name, text=text)
        print(f"Sent DM to @{screen_name}: {text}")
    except tweepy.TweepError as e:
        print(f"Failed to send DM to @{screen_name}: {e}")

# Start the listener
listener = ClownBotListener(consumer_key, consumer_secret, access_token, access_token_secret)
listener.filter(track=["@HobbleStepN"], threaded=True)

