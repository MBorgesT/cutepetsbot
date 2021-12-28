from twitter_scripts import twitter as tt
import tweepy

if __name__ == '__main__':
    api = tt.get_api()
    for status in tweepy.Cursor(api.user_timeline).items():
       try:
           api.destroy_status(status.id)
       except:
           pass
