def user_info(request):
    if request.user.is_authenticated:
        return {
            'user_name': request.user.get_full_name() or request.user.username,
            'user_avatar': request.user.avatar.url if request.user.avatar else '/static/images/user-icon.svg',
        }
    return {}
