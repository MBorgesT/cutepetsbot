from twitter_scripts import twitter as tt
from reddit_scripts import reddit


if __name__ == '__main__':
    api = tt.get_api()
    post = reddit.get_post()

    media = api.media_upload(post.content_path)
    api.update_status(
        status=post.title,
        media_ids=[media.media_id]
    )
        
    tt.delete_temp_file(post.content_path)