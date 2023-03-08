import tweepy
import openai
import os
import re

# Authenticate to Twitter
auth = tweepy.OAuth2BearerHandler(access_token=os.environ['TWITTER_ACCESS_TOKEN'])

# Create API object
api = tweepy.API(auth)

# Authenticate to OpenAI
openai.api_key = os.environ['OPENAI_API_KEY']

# Define function to generate clown-themed responses using OpenAI's GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
    )
    return response.choices[0].text.strip()

# Define function to handle incoming DMs and @mentions
class MyStreamListener(tweepy.Stream):
    def __init__(self, api):
        super().__init__(auth=api.auth, listener=self)

    def on_direct_message(self, status):
        sender_id = status.direct_message.sender_id_str
        message_text = status.direct_message.text
        response_text = generate_response(message_text)
        api.send_direct_message(sender_id, response_text)

    def on_status(self, status):
        if re.search(r'@HobbleStepN', status.text):
            message_text = status.text
            response_text = generate_response(message_text)
            api.update_status(f"@{status.user.screen_name} {response_text}", status.id_str)

# Set up the stream listener
myStreamListener = MyStreamListener(api)
myStreamListener.filter(track=['@HobbleStepN'], is_async=True)


