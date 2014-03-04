from django import template
from django.template import Library, Node, TemplateSyntaxError 
from InstaSell.sellposts.models import SellPost 
from mezzanine.conf import settings
from settings import SELLPOST_EXTENSION, MEDIA_URL
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


register = template.Library()

@register.filter(name='apply_modulo')
def apply_modulo(value, arg):
    return value % arg

#gets all tags for a dormpic, according to its id
@register.filter(name='get_tags')
def get_tags(sellpost):
    tags = SellPost.tags.filter(sellpost = sellpost)
    tags_in_proper_form = []
    #return with commas
    for i in range(len(tags)):
        if i is not (len(tags) - 1):
            tags_in_proper_form.append(str(tags[i].name) + ', ')
        else:
            tags_in_proper_form.append(str(tags[i].name))
    return " ".join(tags_in_proper_form)


@register.filter(name = 'get_url_for_thumbnail')
def get_url_for_thumbnail(image_path):
    length_to_cut = len(MEDIA_URL + SELLPOST_EXTENSION)
    thumbnail_path = MEDIA_URL + SELLPOST_EXTENSION + settings.THUMBNAILS_DIR_NAME + image_path[length_to_cut-1:]
    return thumbnail_path

@register.filter(name = 'get_username_from_user_id')
def get_username_from_user_id(user_profile):
    try:
        user = User.objects.get(pk = user_profile.user_id)
        user = user.username
    except:
        ObjectDoesNotExist
        user = None
    return user

