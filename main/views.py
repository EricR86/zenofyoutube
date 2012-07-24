from random import choice

import gdata

from django.http import HttpResponse

import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()


def test(request):
    data = get_video_comment_user_and_URL()

    str = '\n'.join(data)
    return HttpResponse(str)

def get_video_comment_user_and_URL():
    feed = get_most_popular_youtube_feed()
    random_video_entry = choice(feed.entry)

    id = get_youtube_feed_entry_id(random_video_entry)

    comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=id)
    random_comment_entry = choice(comment_feed.entry)

    return (get_comment_text_from_feed_entry(random_comment_entry),
            get_comment_author_text_from_feed_entry(random_comment_entry),
            get_youtube_feed_entry_url(random_video_entry),
    )


def get_most_popular_youtube_feed():
    #yt_service.GetMostViewedVideoFeed() there isn't one for most popular afaik
    uri = "https://gdata.youtube.com/feeds/api/standardfeeds/most_popular"
    feed = yt_service.GetYouTubeVideoFeed(uri)
    return feed

def get_youtube_feed_entry_url(entry):
    base_url = "https://www.youtube.com/watch?v="
    return base_url + get_youtube_feed_entry_id(entry)

def get_youtube_feed_entry_id(entry):
    # Get the url
    url = entry.GetSwfUrl()
    # Strip out everything before /v/
    temp_array = url.split("/") # Splits the url between '/'s into an array

    #Take the last element which should contain the ID and the query string
    temp_query_string = temp_array[-1] 

    # Strip out everything after ? (the queries)
    # Take the first part of a split between the "?" url parameter
    id = temp_query_string.split("?")[0]

    return id

def get_comment_text_from_feed_entry(comment_entry):
    return comment_entry.content.text

def get_comment_author_text_from_feed_entry(comment_entry):
    return comment_entry.author[0].name.text

def get_link_from_comment_entry(comment_entry):
    return
