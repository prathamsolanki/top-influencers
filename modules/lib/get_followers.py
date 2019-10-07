import json
import requests
import tweepy
import base64
import numpy as np
import oauth2
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Twitter", timeout=10)

with open('../credentials/twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']
    
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open('../credentials/twitter_credentials_edo.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']
    
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

with open('../data/users.txt', 'r') as f:
    unique_users = np.unique(f.readlines())
    
with open('../data/unique_users.txt', 'w') as f:
    f.write('userId:ID(User)\n')
    f.writelines(unique_users)

with open('../data/followers.txt', 'w') as myfile:
    myfile.write(':END_ID(User),:START_ID(User)\n')

with open('../data/unique_users.txt', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n','')
        if line.startswith('u'):
            continue
        user_name = api.get_user(line).screen_name
        for followers in tweepy.Cursor(api.followers_ids, screen_name=user_name).pages():
            for follower in followers:
                location = geolocator.geocode(api.get_user(str(follower)).location, addressdetails=True)
                try:
                    if ((location.raw['address']['country'] != 'United States of America') or
                       (location.raw['address']['state'] != 'California')):
                        continue
                except AttributeError:
                    pass
                with open('../data/followers.txt', 'a') as myfile:
                    myfile.write(str(line) + ',' + str(follower) + '\n')