import tweepy
import openai
import os

# Twitter OAuth 2.0 authentication
auth = tweepy.OAuth2BearerHandler(os.environ.get("TWITTER_BEARER_TOKEN"))
api = tweepy.API(auth)

# OpenAI API authentication
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to generate clown-themed responses
def generate_response(text):
    prompt = "You say: " + text + "\nClown response:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Tweepy Stream object to listen for direct messages and mentions
class MyStreamListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self)

    def on_direct_message(self, status):
        text = status.message_create["message_data"]["text"]
        sender_id = status.message_create["sender_id"]
        response_text = generate_response(text)
        api.send_direct_message(sender_id, text=response_text)

    def on_status(self, status):
        text = status.text
        username = status.user.screen_name
        if f"@{username}" in text:
            response_text = generate_response(text)
            api.update_status(
                status=response_text,
                in_reply_to_status_id=status.id,
                auto_populate_reply_metadata=True,
            )

# Start the Tweepy Stream
stream_listener = MyStreamListener()
stream_listener.filter(track=[f"@{api.me().screen_name}"], is_async=True)

