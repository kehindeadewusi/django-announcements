from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from announcements.models import Announcement, current_announcements_for_request



def announcement_list(request):
    """
    A basic view that wraps ``django.views.list_detail.object_list`` and
    uses ``current_announcements_for_request`` to get the current
    announcements.
    """
    queryset = current_announcements_for_request(request)
    return ListView.as_view(request, **{
        "queryset": queryset,
        "allow_empty": True,
    })


def announcement_hide(request, object_id):
    """
    Mark this announcement hidden in the session for the user.
    """
    announcement = get_object_or_404(Announcement, pk=object_id)
    # TODO: perform some basic security checks here to ensure next is not bad
    redirect_to = request.GET.get("next")
    excluded_announcements = request.session.get("excluded_announcements", list())
    excluded_announcements.append(announcement.pk)
    request.session["excluded_announcements"] = excluded_announcements
    return HttpResponseRedirect(redirect_to)
