import tweepy
import openai
import os
import re

# Authenticate to Twitter
bearer_token = os.environ['TWITTER_BEARER_TOKEN']
auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

# Authenticate to OpenAI
openai.api_key = os.environ['OPENAI_API_KEY']

# Define function to generate clown-themed response using OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Define function to handle DMs
class DMListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self)

    def on_connect(self):
        print("Connected to Twitter API for DMs.")

    def on_direct_message(self, status):
        if status.direct_message.sender_id != api.me().id:
            # Only respond to DMs sent by others
            user = api.get_user(status.direct_message.sender_id)
            screen_name = user.screen_name
            text = status.direct_message.text
            prompt = f"I'm a clown, {screen_name}. {text}"
            response = generate_response(prompt)
            api.send_direct_message(recipient_id=user.id, text=response)

# Define function to handle mentions
class MentionListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self)

    def on_connect(self):
        print("Connected to Twitter API for mentions.")

    def on_status(self, status):
        if status.in_reply_to_user_id == api.me().id:
            # Only respond to mentions of my username
            user = api.get_user(status.user.id)
            screen_name = user.screen_name
            text = status.text
            prompt = f"I'm a clown, {screen_name}. {text}"
            response = generate_response(prompt)
            api.update_status(
                status=response,
                in_reply_to_status_id=status.id,
                auto_populate_reply_metadata=True,
            )

# Start listening for DMs and mentions
dm_listener = DMListener()
mention_listener = MentionListener()
dm_listener.filter(track=["direct_message"])
mention_listener.filter(track=["@HobbleStepN"])

print("Listening for DMs and mentions...")

