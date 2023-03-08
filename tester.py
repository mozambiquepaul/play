import os
import tweepy
import openai

# Authenticate Tweepy API client using API keys and access tokens
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

# Set up OpenAI API key
openai.api_key = "your_openai_api_key_here"

# Define function to generate clown-themed responses
def generate_clown_response(input_text):
    prompt = "Clown-themed response to: " + input_text
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=60, n=1, stop=None, temperature=0.5)
    return response.choices[0].text.strip()

# Define function to handle DMs and mentions
class ClownBot(tweepy.StreamListener):
    def on_direct_message(self, status):
        text = status.direct_message.text
        response_text = generate_clown_response(text)
        api.send_direct_message(status.direct_message.sender_id, response_text)
    def on_status(self, status):
        text = status.text
        response_text = generate_clown_response(text)
        api.update_status(f"@{status.user.screen_name} {response_text}", in_reply_to_status_id=status.id)

# Create an instance of the ClownBot class and start the Tweepy stream
bot = ClownBot()
stream = tweepy.Stream(auth=api.auth, listener=bot)
stream.filter(track=['@HobbleStepN'])

