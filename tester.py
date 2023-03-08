import os
import tweepy
import openai
import re

# Twitter API credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
bearer_token = os.environ['TWITTER_BEARER_TOKEN']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# OpenAI API credentials
openai.api_key = os.environ['OPENAI_API_KEY']

# Set up Twitter authentication
auth = tweepy.OAuth2BearerToken(bearer_token)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Set up OpenAI GPT-3
model_engine = "text-davinci-002"
prompt = "I am a clown, and I will respond to you with a contextual and humorous message. What would you like to know?"

class DMListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self, tweet_mode='extended')
        
    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit exceeded")
            return False
        
    def on_direct_message(self, status):
        # Ignore messages from self
        if status.direct_message.sender_screen_name == "HobbleStepN":
            return
        
        # Get message text
        message_text = status.direct_message.text
        
        # Generate response from OpenAI GPT-3
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=60,
            n=1,
            stop=None,
            prompt_context={
                'additional_context': message_text,
            },
        )
        message = response.choices[0].text.strip()
        
        # Send response
        recipient_id = status.direct_message.sender_id
        api.send_direct_message(recipient_id, message)
        

class MentionListener(tweepy.Stream):
    def __init__(self):
        super().__init__(auth=api.auth, listener=self, tweet_mode='extended')
        
    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit exceeded")
            return False
        
    def on_status(self, status):
        # Ignore tweets from self
        if status.user.screen_name == "HobbleStepN":
            return
        
        # Check if tweet mentions self
        if re.search(r'\bHobbleStepN\b', status.text):
            # Get message text
            message_text = status.text
            
            # Generate response from OpenAI GPT-3
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=60,
                n=1,
                stop=None,
                prompt_context={
                    'additional_context': message_text,
                },
            )
            message = response.choices[0].text.strip()
            
            # Send response
            recipient_id = status.user.id
            api.update_status(status='@' + status.user.screen_name + ' ' + message, in_reply_to_status_id=status.id)
        

if __name__ == '__main__':
    dm_listener = DMListener()
    dm_listener.userstream(_with='user')
    
    mention_listener = MentionListener()
    mention_listener.filter(track=['@HobbleStepN'])
