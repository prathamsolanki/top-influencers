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
        while True:
            user = self.neo4j.get_user()
            followers = self.twitter.get_followers(user, self.state, self.country)
            self.neo4j.write_followership(user, followers)
            