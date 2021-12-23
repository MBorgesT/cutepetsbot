from twitter_api import twitter as tt
import tweepy

if __name__ == '__main__':
    api = tt.get_api()
    for id in api.get_friend_ids():
       try:
           api.destroy_friendship(user_id=id)
       except Exception as e:
           print(e)