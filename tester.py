import os
import tweepy
import openai

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    os.environ["TWITTER_API_KEY"],
    os.environ["TWITTER_API_SECRET_KEY"],
    os.environ["TWITTER_ACCESS_TOKEN"],
    os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
)

# Authenticate to OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Define function to respond to mentions
def respond_to_mention(tweet):
    # Get tweet text and author
    text = tweet.text
    author = tweet.author.screen_name
    
    # Ignore retweets and own tweets
    if "RT @" in text or author == "HobbleStepN":
        return
    
    # Get AI response
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Post response as a tweet
    api.update_status(
        status="@" + author + " " + response.choices[0].text,
        in_reply_to_status_id=tweet.id
    )

# Define function to respond to DMs
def respond_to_dm(dm):
    # Get DM text and sender
    text = dm.message_create["message_data"]["text"]
    sender_id = dm.message_create["sender_id"]
    
    # Get AI response
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Post response as a DM
    api.send_direct_message(
        recipient_id=sender_id,
        text=response.choices[0].text
    )

# Set up stream listener to respond to mentions and DMs
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.in_reply_to_status_id is not None or status.text.startswith('@'):
            respond_to_mention(status)
    
    def on_direct_message(self, dm):
        respond_to_dm(dm)

# Start stream listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=["@HobbleStepN"])
