from twitter_api import twitter as tt
from datetime import datetime
import os


POST_COUNT = 16


def get_query():
    with open('twitter_api/tweet_search_params.txt') as f:
        return ' OR '.join([x.replace('\n', '') for x in f.readlines()])


def get_timestamp_str():
    return datetime.now().strftime('%H-%M')


def unfollow(api, timestamp):
    file_path = f'twiiter_api/follow_lists/{timestamp}.txt'
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            user_ids = [int(x.replace('\n', '')) for x in f.readlines()]

        for id in user_ids:
            api.destroy_friendship(user_id=id)


def follow(api, timestamp, user_ids):
    for id in user_ids:
        api.create_friendship(user_id=id, follow=True)

    with open(f'twiiter_api/follow_lists/{timestamp}.txt', 'w') as f:
        f.write('\n'.join([str(x) for x in user_ids]))


if __name__ == '__main__':
    api = tt.get_api()
    results = api.search_tweets(
        q=get_query(),
        result_type='recent',
        count=POST_COUNT
    )
 
    timestamp = get_timestamp_str()

    unfollow(api, timestamp)

    new_user_ids = [x.user.id for x in results]
    follow(api, timestamp, new_user_ids)