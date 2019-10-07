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

    def __init__(self, geocode="34.036654,-118.193582,150km"):
        self.twitter = TwitterAuth()
        self.neo4j = Neo4j()
        self.geocode = geocode


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
                except:
                    return

            last_id = self.get_max_id(tweets)

            # Persist the state of the last ID
            self.neo4j.write_lastId(last_id)

            #Save the extracted users
            users = [tweet['user'] for tweet in tweets]
            self.neo4j.write_users(users)

        
    
    def get_max_id(self, tweets):
        tweet_ids = np.array([tweet['id'] for tweet in tweets['statuses']])
        return tweet_ids.max()

