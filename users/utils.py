from django.contrib.auth.decorators import user_passes_test


def moderator_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_moderator,
    )
    return decorated_view_func(view_func)
