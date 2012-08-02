from random import choice

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect

import youtube

COMMENT_CONTEXT_STRINGS = (
    "'s discussion on",
    "'s insight on",
    " discussing",
    " on being inspired by",
    " after carefully analyzing"
)

REPLY_CONTEXT_STRINGS = (
    "'s response to %s on",
    "'s witty rebuttal to %s on",
    " providing additional insight to %s on",
    " after careful thought about %s's comment on",
    "'s careful analysis of %s's comment on",
)

def default(request):
    context_dict = {}

    # Sometimes the video gets removed and there's no valid information for it
    # Or comments have been disabled, etc.
    #try:
    #    comment_info = youtube.get_random_video_info_from_most_popular()
    #except:
    #    # If there's no info for this video, redirect to itself and try again
    #    return HttpResponseRedirect("/")
    comment_info = youtube.get_random_video_info_from_most_popular()

    # Add comment into to our context dictionary
    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text(comment_info["comment_original_author"])

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


#def search(request, search_term):
#    context_dict = {}
#
#    feed = get_youtube_video_search_feed(search_term)
#
#    # Sometimes the video gets removed and there's no valid information for it
#    try:
#        comment_info = get_random_youtube_video_info_from_feed(feed)
#    except:
#        # If there's no info for this video, redirect to itself
#        return HttpResponseRedirect("/search/"+search_term)
#
#    context_dict.update(comment_info)
#    context_dict["comment_context"] = get_random_comment_context_text(comment_info["comment_original_author"])
#
#    return render_to_response('main.html',
#                              context_dict,
#                              context_instance=RequestContext(request))


def permalink(request, video_id, comment_id):
    context_dict = {}

    try:
        comment_info = youtube.get_video_info_from_ids(video_id, comment_id)
    except:
        raise Http404

    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text(comment_info["comment_original_author"])

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def custom_404(request):
    context_dict = {}

    comment_info = {}
    comment_info["video_title"] = "Why can't I find this page?"
    comment_info["video_url"] = "notreallyaurl"
    comment_info["video_id"] = "404"
    comment_info["comment_author"] = "404"
    comment_info["comment_text"] = "This page doesn't exist. The video may have been removed."
    comment_info["comment_id"] = "404"

    context_dict.update(comment_info)
    context_dict["comment_context"] = get_random_comment_context_text()

    return render_to_response('main.html',
                              context_dict,
                              context_instance=RequestContext(request))


def get_random_comment_context_text(original_author=""):
    if(original_author == ""):
        return choice(COMMENT_CONTEXT_STRINGS)
    else:
        response = choice(REPLY_CONTEXT_STRINGS)
        return response % (original_author)
