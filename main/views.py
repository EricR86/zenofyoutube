from random import choice

import gdata

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

import gdata.youtube
import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()


def default(request):
    context_dict = {}

    feed = get_most_popular_youtube_feed()
    comment_info = get_random_youtube_video_info_from_feed(feed)

    # Add comment into to our context dictionary
    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text()

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def permalink(request, video_id, comment_id):
    context_dict = {}

    try:
        comment_info = get_youtube_video_info_from_ids(video_id, comment_id)
    except:
        raise Http404

    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text()

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def page_not_found():
    context_dict = {}

    comment_info = {}
    comment_info["video_title"] = "Why can't I find this page?"
    comment_info["video_url"] = "notreallyaurl"
    comment_info["video_id"] = "404"
    comment_info["comment_author"] = "404 Magic Man"
    comment_info["comment_text"] = "This page doesn't exist. Seriously, this is a broken link."
    comment_info["comment_id"] = "404"

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
    comment_feed = yt_service.GetYouTubeVideoCommentFeed(
        video_id=get_youtube_feed_entry_id(random_video_entry)
    )
    random_comment_entry = choice(comment_feed.entry)

    return get_youtube_video_info_from_entries(random_video_entry, random_comment_entry)


def get_youtube_video_info_from_ids(video_id, comment_id):

    #Get comment from URI provided in permalink
    comment_uri = get_comment_uri_from_ids(video_id, comment_id)
    try:
        comment_entry = yt_service.GetYouTubeVideoCommentEntry(comment_uri)
        video_entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
    except:
        raise Http404

    return get_youtube_video_info_from_entries(video_entry, comment_entry)


def get_youtube_video_info_from_entries(video_entry, comment_entry):

    comment_info = {}
    comment_info["video_title"] = get_youtube_feed_entry_title(video_entry)
    comment_info["video_url"] = get_youtube_feed_entry_url(video_entry)
    comment_info["video_id"] = get_youtube_feed_entry_id(video_entry)
    comment_info["comment_author"] = get_comment_author_text_from_feed_entry(comment_entry)
    comment_info["comment_text"] = get_comment_text_from_feed_entry(comment_entry)
    comment_info["comment_id"] = get_comment_entry_id(comment_entry)

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


def get_comment_entry_id(comment_entry):
    url = comment_entry.id.text
    # Take last part of the URL for the id
    id = url.split("/")[-1]
    return id

def get_comment_uri_from_ids(video_id, comment_id):
    return "http://gdata.youtube.com/feeds/api/videos/" + \
            video_id + \
            "/comments/" + \
            comment_id


#def get_comment_author_url_from_feed_entry(comment_entry):
#    
#    author = get_comment_author_text_from_feed_entry(comment_entry)
#    user_entry = yt_service.GetYouTubeUserEntry(username=author)
#
#    return user_entry.link[0].href # crashes sometimes
