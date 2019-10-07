import sys
import requests
import bs4
import json
from bs4 import BeautifulSoup
import base64
import oauth2
import numpy as np

from ..twitter.interface import TwitterAuth
from ..neo4j.interface import Neo4j


class GetUser:

    def __init__(self, users_file, geocode="34.036654,-118.193582,150km"):
        self.twitter = TwitterAuth()
        self.neo4j = Neo4j()
        self.geocode = geocode
        self.users_file = users_file


    def run(self, initial_run=False):

        while True:
            if initial_run:
                initial_run = False
                tweets = self.twitter.get_tweets(self.geocode)

                # Write some initial stats
                self.neo4j.init_execution()

            else:
                # Get the current state of execution
                last_id = self.neo4j.get_lastId()
                try:
                    tweets = self.twitter.get_tweets(self.geocode, last_id=last_id)
                except AssertionError as e:
                    print(e)
                    return False

            last_id = self.get_max_id(tweets)

            # Persist the state of the last ID
            self.neo4j.write_lastId(last_id)

            #Save the extracted users
            user_ids = [tweet['user']['id_str']+'\n' for tweet in tweets['statuses']]
            with open(self.users_file, 'a') as myfile:
                myfile.writelines(user_ids)

        
    
    def get_max_id(self, tweets):
        tweet_ids = np.array([tweet['id'] for tweet in tweets['statuses']])
        return tweet_ids.max()

