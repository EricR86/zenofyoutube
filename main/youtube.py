#from random import randint
from random import choice

import gdata

import gdata.youtube
import gdata.youtube.service

#dev_key="AI39si4YAGMVZ7p1xugBwj8ScWBiO7syiCU5HpTPZzo8jNYc2Ww78QA6uVkwNJt2LrbXYmwuCjv9fHXhuoVxs-0DFU5atM2TMw"
# See http://gdata.youtube.com/demo/index.html
# This Python Youtube API uses version 1 (instead of 2)
FEED_NUMBER_OF_RESULTS_FILTER_PARAMETERS = "max-results=0&fields=openSearch:totalResults"

MAX_VIDEO_RESULTS = 50
VIDEO_FEED_GET_PARAMETERS = "max-results=%d" % (MAX_VIDEO_RESULTS)
VIDEO_FEED_FILTER_PARAMETERS = "fields=openSearch:totalResults,entry(id,title,gd:comments)"

MAX_COMMENT_RESULTS = 50
COMMENT_FEED_GET_PARAMETERS = "max-results=%d" % (MAX_COMMENT_RESULTS)
COMMENT_FEED_FILTER_PARAMETERS = "fields=openSearch:totalResults,entry(id,link,content,author)"
COMMENT_IN_REPLY_TO_LINK = "http://gdata.youtube.com/schemas/2007#in-reply-to"


MOST_POPULAR_YOUTUBE_FEED_URI = "https://gdata.youtube.com/feeds/api/standardfeeds/most_popular"

yt_service = gdata.youtube.service.YouTubeService()


def get_random_video_info_from_most_popular():
    # Get a random video from the most popular video feed
    random_video_entry = get_random_video_entry_from_feed(MOST_POPULAR_YOUTUBE_FEED_URI)

    # Get a random comment from the selected video entry
    random_comment_entry = get_random_comment_entry_from_video_entry(random_video_entry)

    return get_youtube_video_info_from_entries(random_video_entry, random_comment_entry)


def get_random_video_info_from_search(search_terms):
    # Get a random video from the most popular video feed
    random_video_entry = get_random_video_entry_from_search(search_terms)

    # Get a random comment from the selected video entry
    random_comment_entry = get_random_comment_entry_from_video_entry(random_video_entry)

    return get_youtube_video_info_from_entries(random_video_entry, random_comment_entry)


def get_video_info_from_ids(video_id, comment_id):

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

    comment_info["comment_is_response"] = False
    comment_info["comment_original_author"] = ""
    comment_info["comment_original_link"] = ""
    
    #import pdb
    #pdb.set_trace()

    comment_in_reply_to_uri = get_comment_feed_entry_in_reply_to_uri(comment_entry)
    # If there's a reponse
    if(comment_in_reply_to_uri != ""):
        # Fill in the repsonse info
        comment_info["comment_is_response"] = True
        original_comment_entry = yt_service.GetYouTubeVideoCommentEntry(uri=comment_in_reply_to_uri)
        comment_info["comment_original_author"] = get_comment_feed_entry_author(original_comment_entry)
        comment_info["comment_original_link"] = "/permalink/" + \
            comment_info["video_id"] + "/" + \
            comment_in_reply_to_uri.split("/")[-1]

    return comment_info


def get_random_video_entry_from_search(search_terms):
    query = "http://gdata.youtube.com/feeds/api/videos"
    query += "?" + VIDEO_FEED_FILTER_PARAMETERS
    query += "&" + VIDEO_FEED_GET_PARAMETERS
    query += "&q=" + search_terms

    feed = yt_service.GetYouTubeVideoFeed(query)

    total_results = int(feed.total_results.text)

    if total_results < 1:
        raise gdata.youtube.service.YouTubeError("No video entries found from search")
    
    return choice(feed.entry)


# Video Entry Retrieval
def get_random_video_entry_from_feed(uri):
    # Query the number of videos from this feed
    #total_results = get_number_of_results_from_video_feed(uri)
    
    query = uri + "?" + VIDEO_FEED_FILTER_PARAMETERS
    query += "&" + VIDEO_FEED_GET_PARAMETERS
    #query += "&" + get_random_start_index_get_parameter(total_results)

    feed = yt_service.GetYouTubeVideoFeed(query)
    total_results = int(feed.total_results.text)

    if total_results < 1:
        raise gdata.youtube.service.YouTubeError("No video entries found from feed")
    
    return choice(feed.entry)


def get_number_of_results_from_video_feed(uri):
    query = uri + "?" + FEED_NUMBER_OF_RESULTS_FILTER_PARAMETERS
    feed = yt_service.GetYouTubeVideoFeed(query)
    return int(feed.total_results.text)


def get_random_start_index_get_parameter(max_results):
    # There's a limit on the index we can query at
    if max_results > 1000:
        max_results = 1000

    return "start-index=%d" % (randint(1, max_results))


# Comment Entry Retrieval
def get_random_comment_entry_from_video_entry(video_entry):
    # Get the comment feed uri
    comment_uri = get_comment_feed_uri_from_video_entry(video_entry)

    # Query the number of comments from this feed
    #total_results = get_number_of_results_from_comment_feed(comment_uri)

    comment_uri = comment_uri + "?" + \
        COMMENT_FEED_FILTER_PARAMETERS + "&" + \
        COMMENT_FEED_GET_PARAMETERS + "&"#+ \
        #get_random_start_index_get_parameter(total_results)

    comment_feed = yt_service.GetYouTubeVideoCommentFeed(uri=comment_uri)

    total_results = int(comment_feed.total_results.text)
    if total_results < 1:
        raise gdata.youtube.service.YouTubeError("No comment entries found from video")
    #comment_feed = yt_service.GetYouTubeVideoCommentFeed(
    #    video_id=get_video_feed_entry_id(random_video_entry)
    #)

    # There will only be one entry since max-results was set to 1
    #return comment_feed.entry[0]

    #random_comment_entry = choice(comment_feed.entry)
    return choice(comment_feed.entry)


def get_number_of_results_from_comment_feed(uri):
    query = uri + "?" + FEED_NUMBER_OF_RESULTS_FILTER_PARAMETERS
    feed = yt_service.GetYouTubeVideoCommentFeed(query)
    return int(feed.total_results.text)


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


def get_comment_feed_uri_from_video_entry(entry):
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


def get_comment_feed_entry_in_reply_to_uri(comment_entry):
    uri = ""
    for link in comment_entry.link:
        if(link.rel == COMMENT_IN_REPLY_TO_LINK):
            uri = link.href
            break

    return uri


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
