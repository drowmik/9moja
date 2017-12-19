from django.utils.deprecation import MiddlewareMixin
from django_mobileesp import mdetect


class MobileDetectionMiddleware(MiddlewareMixin):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """
    
    def __init__(self, get_response=None):
        self.get_response = get_response
    
    def process_request(self, request):
        is_mobile = False
        browser = 'STANDARD'
        
        opera_mini_str = "opera mini"
        
        user_agent = request.META.get("HTTP_USER_AGENT", '')
        http_accept = request.META.get("HTTP_ACCEPT", '')
        
        if user_agent and http_accept:
            if opera_mini_str in user_agent.lower():
                browser = 'OPERA_MINI'
            
            agent = mdetect.UAgentInfo(userAgent=user_agent,
                                       httpAccept=http_accept)
            is_mobile = (agent.getIsIphone() or
                         agent.getIsTierTablet() or
                         agent.getIsTierIphone() or
                         agent.getIsTierRichCss() or
                         agent.getIsTierGenericMobile() or
                         agent.detectMobileQuick())
        
        request.is_mobile = is_mobile
        request.browser = browser
