import re

from django import template

register = template.Library()


@register.filter
def highlighter(value, search):
    redata = re.compile(r"({0})(?![^<]*>|[^<>]*</)".format(search), re.IGNORECASE)
    newval = redata.sub("<span class=\"highlight\">{}</span>".format(search), value)
    return newval
