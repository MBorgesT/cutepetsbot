from twitter_api import twitter as tt
import tweepy
import os

if __name__ == '__main__':
    os.chdir("~/cutepetsbot/")
    
    api = tt.get_api()
    for status in tweepy.Cursor(api.user_timeline).items():
       try:
           api.destroy_status(status.id)
       except:
           pass
