from random import choice

import gdata

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

import gdata.youtube
import gdata.youtube.service

#dev_key="AI39si4YAGMVZ7p1xugBwj8ScWBiO7syiCU5HpTPZzo8jNYc2Ww78QA6uVkwNJt2LrbXYmwuCjv9fHXhuoVxs-0DFU5atM2TMw"
# See http://gdata.youtube.com/demo/index.html
# This Python Youtube API uses version 1 (instead of 2)
video_feed_get_parameters = "max-results=50"
video_feed_filter_parameters = "fields=entry(id,title,gd:comments)"
comment_feed_get_parameters = "max-results=50"
comment_feed_filter_parameters = "fields=entry(id,content,author)"

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


def custom_404(request):
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
    # Choose a random video
    random_video_entry = choice(feed.entry)

    # Get the comment feed for the video
    #comment_uri = get_video_feed_entry_comment_feed_uri(random_video_entry)
    #comment_uri = comment_uri + "?" + \
    #    comment_feed_filter_parameters + "&" + \
    #    comment_feed_get_parameters

    ## This crashes sometimes
    #comment_feed = yt_service.GetYouTubeVideoCommentFeed(uri=comment_uri)
    comment_feed = yt_service.GetYouTubeVideoCommentFeed(
        video_id=get_video_feed_entry_id(random_video_entry)
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
    comment_info["video_title"] = get_video_feed_entry_title(video_entry)
    comment_info["video_url"] = get_video_feed_entry_url(video_entry)
    comment_info["video_id"] = get_video_feed_entry_id(video_entry)
    comment_info["comment_author"] = get_comment_feed_entry_author(comment_entry)
    comment_info["comment_text"] = get_comment_feed_entry_content(comment_entry)
    comment_info["comment_id"] = get_comment_feed_entry_id(comment_entry)

    return comment_info


def get_most_popular_youtube_feed():
    #yt_service.GetMostViewedVideoFeed() there isn't one for most popular afaik
    uri = "https://gdata.youtube.com/feeds/api/standardfeeds/most_popular"
    uri = uri + "?" + video_feed_filter_parameters + "&" + video_feed_get_parameters
    feed = yt_service.GetYouTubeVideoFeed(uri)
    return feed


# Video Info Retrieval 
def get_video_feed_entry_title(entry):
    return entry.title.text


def get_video_feed_entry_url(entry):
    base_url = "https://www.youtube.com/watch?v="
    return base_url + get_video_feed_entry_id(entry)


def get_video_feed_entry_id(entry):
    # Get the url
    url = entry.id.text
    # Strip out everything before /v/
    temp_array = url.split("/") # Splits the url between '/'s into an array
    #Take the last element which should contain the ID
    id = temp_array[-1] 
    return id


def get_video_feed_entry_comment_feed_uri(entry):
    return entry.comments.feed_link[0].href


# Comment Info Retrieval 
def get_comment_feed_entry_content(comment_entry):
    return comment_entry.content.text


def get_comment_feed_entry_author(comment_entry):
    return comment_entry.author[0].name.text


def get_comment_feed_entry_id(comment_entry):
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
#    author = get_comment_feed_entry_author(comment_entry)
#    user_entry = yt_service.GetYouTubeUserEntry(username=author)
#
#    return user_entry.link[0].href # crashes sometimes
