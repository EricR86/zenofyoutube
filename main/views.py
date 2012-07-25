from random import choice

import gdata

from django.template import RequestContext
from django.shortcuts import render_to_response

import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()


def test(request):
    context_dict = {}

    feed = get_most_popular_youtube_feed()
    comment_info = get_random_youtube_video_info_from_feed(feed)

    # Add comment into to our context dictionary
    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text()

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def get_random_comment_context_text():
    strings = (
        "'s discussion on",
        "'s insight on",
        " discussing",
        " on being inspired by",
        " after carefully analyzing"
    )

    return choice(strings)


def get_random_youtube_video_info_from_feed(feed):
    random_video_entry = choice(feed.entry)

    id = get_youtube_feed_entry_id(random_video_entry)

    comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=id)
    random_comment_entry = choice(comment_feed.entry)

    comment_info = {}
    comment_info["video_title"] = get_youtube_feed_entry_title(random_video_entry)
    comment_info["video_url"] = get_youtube_feed_entry_url(random_video_entry)
    comment_info["comment_author"] = get_comment_author_text_from_feed_entry(random_comment_entry)
    comment_info["comment_text"] = get_comment_text_from_feed_entry(random_comment_entry)

    return comment_info


def get_most_popular_youtube_feed():
    #yt_service.GetMostViewedVideoFeed() there isn't one for most popular afaik
    uri = "https://gdata.youtube.com/feeds/api/standardfeeds/most_popular"
    feed = yt_service.GetYouTubeVideoFeed(uri)
    return feed


def get_youtube_feed_entry_title(entry):
    return entry.media.title.text


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


#def get_comment_author_url_from_feed_entry(comment_entry):
#    
#    author = get_comment_author_text_from_feed_entry(comment_entry)
#    user_entry = yt_service.GetYouTubeUserEntry(username=author)
#
#    return user_entry.link[0].href # crashes sometimes
