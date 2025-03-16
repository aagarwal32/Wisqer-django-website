from django import template

register = template.Library()

@register.filter
def is_following(current_user, target_user):
    '''
    Returns True if current_user follows target_user
    '''
    if not target_user.is_authenticated: return False
    return target_user.followers.filter(user_id=current_user).exists()

@register.filter
def is_following_by(follower, target_user):
    '''
    Returns True if 'follower' is following 'target'.
    '''
    if not target_user.is_authenticated: return False
    return follower.following.filter(following_user_id=target_user).exists()