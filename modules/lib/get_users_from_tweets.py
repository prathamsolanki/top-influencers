import sys
import requests
import bs4
import json
from bs4 import BeautifulSoup
import base64
import oauth2

from ..twitter.interface import TwitterAuth


class GetUser:

    def __init__(self, ):
        self.twitter = TwitterAuth()



# url_rest = "https://api.twitter.com/1.1/search/tweets.json"

# q = '* -filter:retweets'

# last_id = sys.maxsize
# initial_run = True

# while True:
#     if initial_run:
#         intial_run = False
#         params = {'q': q, 'count': 100, 'lang': 'en', 'geocode': '34.036654,-118.193582,150km', 'result_type': 'recent'}
#     else:
#         params = {'q': q, 'count': 100, 'lang': 'en', 'geocode': '34.036654,-118.193582,150km', 'result_type': 'recent', 'max_id': last_id}
#     results = requests.get(url_rest, params=params, headers={'Authorization': 'Bearer ' + twitter.token})
#     tweets = results.json()
#     tweet_ids = [tweet['id'] for tweet in tweets['statuses']]
#     for tweet_id in tweet_ids:
#         if tweet_id < last_id: last_id = tweet_id
#     user_ids = [tweet['user']['id_str']+'\n' for tweet in tweets['statuses']]
#     with open('../data/users.txt', 'a') as myfile:
#         myfile.writelines(user_ids)