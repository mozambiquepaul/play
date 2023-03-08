import tweepy
import os
import openai

# set up Twitter API credentials
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# set up Tweepy API client
auth = tweepy.OAuth2BearerHandler(access_token)
api = tweepy.API(auth)

# set up listener for incoming DMs and mentions
class ClownListener(tweepy.Stream):
    def __init__(self, auth, api, access_token, access_token_secret):
        super().__init__(auth, api)
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def on_status(self, status):
        # check if mention includes @HobbleStepN
        if "@HobbleStepN" in status.text:
            # generate clown-themed response using OpenAI API
            response = openai.Completion.create(
              engine="davinci",
              prompt=status.text,
              temperature=0.7,
              max_tokens=60,
              n=1,
              stop=None,
              timeout=10,
            )
            # post response as a tweet
            api.update_status(f"@{status.user.screen_name} {response.choices[0].text}", status.id)
        # check if DM received
        elif status.direct_message:
            # generate clown-themed response using OpenAI API
            response = openai.Completion.create(
              engine="davinci",
              prompt=status.text,
              temperature=0.7,
              max_tokens=60,
              n=1,
              stop=None,
              timeout=10,
            )
            # post response as a DM
            api.send_direct_message(status.user.id, f"{response.choices[0].text}")

# set up Tweepy API client
auth = tweepy.OAuth2BearerHandler(access_token)
api = tweepy.API(auth)

# start Tweepy stream
stream = ClownListener(auth, api)
stream.filter(track=["@HobbleStepN"], is_async=True)
