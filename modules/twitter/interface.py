import json
import requests
import base64

class TwitterAuth:

    def __init__(self, credentials="credentials_default.json"):
        """
        Create an authenticated channel with Twitter APIs
        """
        credentials = "./" + credentials

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
        ).json()


