from django import template
from core.models import property, bookmark, Compare

register = template.Library()


@register.filter
def added_to_bookmark(user, id):
    try:
        if user.is_authenticated:
            qs = bookmark.objects.filter(user=user)[0]

            if qs.properties.filter(id=id).exists():
                return True
    except:
        return False


@register.filter
def added_to_compare(user, id):
    try:
        if user.is_authenticated:
            qs = Compare.objects.filter(user=user)
            if qs.properties.filter(id=id).exists():
                return True
    except:
        return False

