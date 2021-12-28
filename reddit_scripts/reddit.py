from praw import Reddit
import urllib.request
import random
from utils_scripts.paths import paths


class Post:

    def __init__(self, title, content, content_type):
        self.title = title
        self.content_path = content
        self.content_type = content_type


def get_post():
    subreddits = get_subreddits()
    posted_ids = get_posted_ids()
    reddit = get_praw()

    for sr in subreddits:
        subreddit = reddit.subreddit(sr)
        for post in subreddit.hot(limit=20):
            content_type = get_content_type(post.url)
            if (content_type == 'jpg' or content_type == 'gif') and post.id not in posted_ids:
                save_posted_ids(posted_ids, post.id)
                return Post(post.title, save_image_from_url(post.url, content_type), content_type)
    
    return None


def get_praw():
    id, secret = get_creds()
    reddit = Reddit(
        client_id=id,
        client_secret=secret,
        user_agent='Pets Bot',
    )
    reddit.read_only = True
    return reddit


def get_subreddits():
    with open(paths['scripts'] + 'reddit_scripts/subreddits.txt', 'r') as f:
        subreddits = [x.replace('\n', '') for x in f.readlines()]
    random.shuffle(subreddits)
    return subreddits


def get_creds():
    with open(paths['scripts'] + 'reddit_scripts/creds.txt', 'r') as f:
        return [x.replace('\n', '') for x in f.readlines()]


def get_posted_ids():
    with open(paths['scripts'] + 'reddit_scripts/posted_ids.txt', 'r') as f:
        return [x.replace('\n', '') for x in f.readlines()]


def save_posted_ids(posted_ids, new_id):
    if len(posted_ids) >= 200:
        del posted_ids[:-1]
    posted_ids.insert(0, new_id)

    with open(paths['scripts'] + 'reddit_scripts/posted_ids.txt', 'w') as f:
        f.write('\n'.join(posted_ids))


def save_image_from_url(url, content_type):
    file_path = 'temp.' + content_type
    urllib.request.urlretrieve(url, file_path)
    return file_path


def get_content_type(url):
    if url[-4:] == '.jpg':
        return 'jpg'
    if url[-4:] == '.gif':
        return 'gif'
    if 'v.redd.it' in url:
        return 'video'
    return 'idk'
    

if __name__ == '__main__':
    post = get_post()
    if post is None:
        raise Exception('No post found')
    print(post.title)
    post.content.show()
