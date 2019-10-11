import json
import requests
import tweepy
import base64
import numpy as np
import oauth2

from ..twitter.interface import TwitterAuth, Followers
from ..neo4j.interface import Neo4j

class GetFollowers:

    def __init__(self, credentials=None, state="California", country="United States of America"):
        self.twitter = TwitterAuth(credentials=credentials) if credentials else TwitterAuth()
        self.neo4j = Neo4j(
             uri="bolt://localhost:7687",
            user="neo4j",
            password="neo4j",
        )
        self.state = state
        self.country = country


    @staticmethod
    def run(credentials):
        get_followers = GetFollowers(credentials=credentials)
        while True:
            user = get_followers.neo4j.get_user()
            
            follower_class = Followers(user, get_followers.state, get_followers.country, get_followers.twitter.api)
            followers = follower_class.next_page()
            while followers is not None:
                get_followers.neo4j.write_followership(user, followers)
                followers = follower_class.next_page()
            
            get_followers.neo4j.user_processed(user)