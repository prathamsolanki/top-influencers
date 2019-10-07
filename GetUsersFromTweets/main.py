import sys
import requests
import bs4
import json
from bs4 import BeautifulSoup
import base64
import oauth2

with open('../credentials/twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']
    token_credential = consumer_key + ':' + consumer_secret
    encoded_token_credential = str(base64.b64encode(token_credential.encode())).replace("b'","").replace("'","")

response = requests.post('https://api.twitter.com/oauth2/token', 
                         headers={'Authorization':'Basic '+encoded_token_credential, 
                                  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}, 
                         data={'grant_type':'client_credentials'})

token = response.json()['access_token']

with open('../credentials/twitter_credentials_edo.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']
    token_credential = consumer_key + ':' + consumer_secret
    encoded_token_credential = str(base64.b64encode(token_credential.encode())).replace("b'","").replace("'","")
    
response = requests.post('https://api.twitter.com/oauth2/token', 
                         headers={'Authorization':'Basic '+encoded_token_credential, 
                                  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}, 
                         data={'grant_type':'client_credentials'})

token = response.json()['access_token']

url_rest = "https://api.twitter.com/1.1/search/tweets.json"

q = '* -filter:retweets'

last_id = sys.maxsize
initial_run = True

while True:
    if initial_run:
        intial_run = False
        params = {'q': q, 'count': 100, 'lang': 'en', 'geocode': '34.036654,-118.193582,150km', 'result_type': 'recent'}
    else:
        params = {'q': q, 'count': 100, 'lang': 'en', 'geocode': '34.036654,-118.193582,150km', 'result_type': 'recent', 'max_id': last_id}
    results = requests.get(url_rest, params=params, headers={'Authorization': 'Bearer ' + token})
    tweets = results.json()
    tweet_ids = [tweet['id'] for tweet in tweets['statuses']]
    for tweet_id in tweet_ids:
        if tweet_id < last_id: last_id = tweet_id
    user_ids = [tweet['user']['id_str']+'\n' for tweet in tweets['statuses']]
    with open('../data/users.txt', 'a') as myfile:
        myfile.writelines(user_ids)