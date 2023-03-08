import os
import tweepy
import openai
from dotenv import load_dotenv

load_dotenv()

# Authenticate to Twitter API
auth = tweepy.OAuth2BearerHandler(os.environ['TWITTER_BEARER_TOKEN'])
api = tweepy.API(auth)

# Authenticate to OpenAI API
openai.api_key = os.environ['OPENAI_API_SECRET_KEY']


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.user.id != api.me().id: # Ignore tweets from self
            tweet_id = status.id
            username = status.user.screen_name
            context = status.text

            # Check if tweet is a mention
            if f"@{api.me().screen_name}" in context:
                response = generate_response(context)
                api.update_status(
                    status=response,
                    in_reply_to_status_id=tweet_id,
                    auto_populate_reply_metadata=True
                )

            # Check if tweet is a DM
            elif status.in_reply_to_screen_name is None:
                response = generate_response(context)
                api.send_direct_message(
                    recipient_id=status.user.id,
                    text=response
                )

    def on_error(self, status_code):
        if status_code == 420:
            return False


def generate_response(context):
    # Get AI-generated response
    prompt = f"Clown responds to {context}\nClown:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


if __name__ == "__main__":
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
    my_stream.filter(track=[f"@{api.me().screen_name}"], is_async=True)

