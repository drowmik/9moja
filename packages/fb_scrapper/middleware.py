from core import settings as settings
from .models import SocialAuth


class SocialAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        all_auths = SocialAuth.objects.all()
        # print(all_auths)
        if all_auths:
            for auth in all_auths:
                if (auth.name).lower() == "facebook":
                    settings.SOCIAL_AUTH_FACEBOOK_KEY = auth.app_id
                    settings.SOCIAL_AUTH_FACEBOOK_SECRET = auth.secret_id
                if (auth.name).lower() == "twitter":
                    settings.SOCIAL_AUTH_TWITTER_KEY = auth.app_id
                    settings.SOCIAL_AUTH_TWITTER_SECRET = auth.secret_id
        
        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        
        
        return response
