import tweepy
import os
from utils_scripts.paths import paths


def get_api():
    consumer_key, consumer_secret, access_token, access_token_secret = get_creds()
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def get_creds():
    with open(paths['scripts'] + 'twitter_scripts/creds.txt', 'r') as f:
        return [x.replace('\n', '') for x in f.readlines()]


def delete_temp_file(file_path):
    os.remove(file_path)