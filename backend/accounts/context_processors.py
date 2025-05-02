import os
from django.conf import settings

def user_avatar(request):
    """
    يُعيد رابط صورة المستخدم إذا كانت موجودة فعليًا،
    وإذا لم تكن موجودة يُعيد رابط صورة افتراضية من static.
    """
    default_avatar = '/static/images/default_avatar.svg'

    if request.user.is_authenticated:
        avatar = getattr(request.user, 'avatar', None)
        if avatar:
            avatar_path = os.path.join(settings.MEDIA_ROOT, avatar.name)
            if os.path.exists(avatar_path):
                return {'user_avatar': avatar.url}

    return {'user_avatar': default_avatar}
