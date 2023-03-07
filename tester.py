import os
import tweepy
import openai

# Authenticate with Twitter API
auth = tweepy.OAuth2BearerHandler(os.environ['BEARER_TOKEN'])
api = tweepy.API(auth)

# Authenticate with OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

# Generate clown response
def generate_clown_response(message):
    prompt = f"Clown-themed response to: {message}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=50,
        n=1,
        stop=None,
        timeout=10,
    )
    return response.choices[0].text.strip()

# Stream listener to respond to DMs and mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.author.id == api.me().id:
            return
        if status.in_reply_to_status_id is not None or 'media' in status.entities:
            return
        if status.in_reply_to_screen_name == api.me().screen_name:
            response = generate_clown_response(status.text)
            api.update_status(
                status=response,
                in_reply_to_status_id=status.id,
                auto_populate_reply_metadata=True
            )
        elif hasattr(status, 'direct_message'):
            message = status.direct_message['text']
            response = generate_clown_response(message)
            api.send_direct_message(
                user_id=status.direct_message['sender_id'],
                text=response
            )

# Start streaming
stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=[api.me().screen_name])
