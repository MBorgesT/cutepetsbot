from twitter_api import twitter as tt
from reddit_api import reddit
import os


if __name__ == '__main__':
    os.chdir("~/cutepetsbot/")
    
    api = tt.get_api()
    post = reddit.get_post()

    media = api.media_upload(post.content_path)
    api.update_status(
        status=post.title,
        media_ids=[media.media_id]
    )
        
    tt.delete_temp_file(post.content_path)