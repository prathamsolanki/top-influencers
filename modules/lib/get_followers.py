import json
import requests
import tweepy
import base64
import numpy as np
import oauth2

from ..twitter.interface import TwitterAuth
from ..neo4j.interface import Neo4j

class GetFollowers:

    def __init__(self, state="California", country="United States of America"):
        self.twitter = TwitterAuth()
        self.neo4j = Neo4j()
        self.state = state
        self.country = country


    def run(self):
        # get users from Neo4j whose isProcessed status is false
        users = []
        for user in users:
            followers = self.twitter.get_followers(user, self.state, self.country)
            # set isProcessed status of user to true
            