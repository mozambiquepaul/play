import tweepy

# Replace the placeholders with your own values
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'
client_id = 'OAUTH2_CLIENT_ID'
client_secret = 'OAUTH2_CLIENT_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth.apply_auth()

# Add OAuth 2.0 client credentials to auth object
auth.set_client(client_id, client_secret)

api = tweepy.API(auth)

# Test authentication
try:
    user = api.verify_credentials()
    print('Authentication successful')
except tweepy.TweepError as e:
    print(f'Error: {e}')
