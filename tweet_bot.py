import tweepy
from config import api_key, secret_key, access_token, token_secret
import pandas as pd
from random import randint
import time

auth = tweepy.OAuthHandler(api_key, secret_key)
auth.set_access_token(access_token, token_secret)

api = tweepy.API(auth)

movies = pd.read_csv('movies.csv')


def send_tweet():
    rnd = randint(1, 4615)
    msg = (movies.loc[rnd][0] + " " + movies.loc[rnd][1] + " - " + movies.loc[rnd][2])
    if len(msg) <= 280:
        api.update_status(msg)
        print("Bot tweeted: " + msg)

    else:
        send_tweet()

while True:
    send_tweet()
    time.sleep(3600)
