import json
import requests
import base64
import tweepy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Twitter", timeout=10)

class TwitterAuth:

    def __init__(self, credentials="credentials_default.json"):
        """
        Create an authenticated channel with Twitter APIs
        """
        with open(credentials) as cred_data:
            info = json.load(cred_data)
            self.consumer_key = info['CONSUMER_KEY']
            self.consumer_secret = info['CONSUMER_SECRET']
            self.access_key = info['ACCESS_KEY']
            self.access_secret = info['ACCESS_SECRET']
            token_credential = self.consumer_key + ':' + self.consumer_secret
            encoded_token_credential = str(base64.b64encode(token_credential.encode())).replace("b'","").replace("'","")

        response = requests.post('https://api.twitter.com/oauth2/token', 
                                headers={'Authorization':'Basic ' + encoded_token_credential, 
                                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}, 
                                data={'grant_type':'client_credentials'})

        self.token = response.json()['access_token']

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    
    def get_tweets(self, geocode, last_id=None):
        url_rest = "https://api.twitter.com/1.1/search/tweets.json"
        
        q = '* -filter:retweets'

        params = {
            'q': q, 
            'count': 100, 
            'lang': 'en', 
            'geocode': geocode, 
            'result_type': 'recent'
        }

        if last_id:
            params['max_id'] = last_id

        return requests.get(
            url_rest, 
            params=params, 
            headers={'Authorization': 'Bearer ' + self.token}
        ).json()['statuses']


    def get_followers(self, user_name, state, country):

        for followers in tweepy.Cursor(self.api.followers_ids, screen_name=user_name).pages():
            qualified_followers = []

            for follower in followers:
                follower_object = self.api.get_user(str(follower))
                location = geolocator.geocode(follower_object.location, addressdetails=True).raw

                try:
                    if ((location['address']['country'] != country) or (location['address']['state'] != state)):
                        continue
                except AttributeError:
                    qualified_followers.append(follower_object)

        return follower_object