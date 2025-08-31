"""
takes request, returns a dict of data as a context

category dropdown-menu is in nav bar whih is included in every template
"""
from .models import Category


def menu_links(request):

    return {
        'links': Category.objects.all(),
    }