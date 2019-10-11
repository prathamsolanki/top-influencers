import sys
import requests
import bs4
import json
from bs4 import BeautifulSoup
import base64
import oauth2
import numpy as np
import time

from ..twitter.interface import TwitterAuth
from ..neo4j.interface import Neo4j


class GetUsers:

    def __init__(self, credentials=None, geocode="34.036654,-118.193582,150km"):
        self.twitter = TwitterAuth(credentials=credentials) if credentials else TwitterAuth()
        self.neo4j = Neo4j(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="neo4j",
        )
        self.geocode = geocode

    
    def close(self, ):
        self.neo4j.close()


    def _run(self, initial_run=False):

        while True:
            if initial_run:
                initial_run = False
                tweets = self.twitter.get_tweets(self.geocode)

                # Write some initial stats
                self.neo4j.init_execution()

            else:
                # Get the current state of execution
                last_id = int(self.neo4j.get_lastId())
                try:
                    tweets = self.twitter.get_tweets(self.geocode, last_id=last_id)
                except:
                    return

            #Save the extracted users
            users = [tweet['user'] for tweet in tweets]
            self.neo4j.write_users(users)

            last_id = self.get_min_id(tweets)

            # Persist the state of the last ID
            self.neo4j.write_lastId(str(last_id))
  
    def get_min_id(self, tweets):
        tweet_ids = np.array([tweet['id'] for tweet in tweets])
        return tweet_ids.min()

    
    @staticmethod
    def run(credentials, initial_run=False):
        # Initial run
        # get_users = GetUsers(credentials=credentials[0])
        # get_users.run(initial_run=True)
        # get_users.close()

        while True:
            for c in credentials:
                get_users = GetUsers(credentials=c)
                get_users._run(initial_run=initial_run)
                get_users.close()

            # sleep for 10 seconds
            print("Sleeping...")
            time.sleep(10)  

