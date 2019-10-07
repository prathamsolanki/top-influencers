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
