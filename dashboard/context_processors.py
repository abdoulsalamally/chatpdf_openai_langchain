from .models import TokenTracker
from allauth.socialaccount.models import SocialAccount
from dashboard.models import Notification

def token_context(request):
    has_notifications = False
    try:
        nofts = Notification.objects.filter(user=request.user)
        has_notifications = False
        if len(nofts) > 0:
            has_notifications = True
    except:
        nofts = None
    try:
        social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
        profile_image_url = None
        if social_account:
            profile_image_url = social_account.extra_data.get('picture')
    except:
        profile_image_url = None

    try:
        tokens = int(TokenTracker.objects.get_or_create(user=request.user)[0].token_count)

    except:
        tokens = 0

    return {'tokens': tokens, 'profile_image_url':profile_image_url,'nofts':nofts, 'has_notifications':has_notifications,}
