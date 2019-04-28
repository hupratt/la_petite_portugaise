from . import mdetect
from django.conf import settings
import re

"""
class DetectAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_request(request)
        # self.process_view(request)
        return response

    def process_request(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT")
        http_accept = request.META.get("HTTP_ACCEPT")
        if user_agent and http_accept:
            agent = mdetect.UAgentInfo(
                userAgent=user_agent, httpAccept=http_accept)
            # in case we want more information about the device
            request.mobile_esp_agent = agent
            if agent.detectMobileQuick():
                request.device_type = 'mobile'
            elif agent.detectTierTablet():
                request.device_type = 'tablet'
            else:
                request.device_type = 'desktop'
            # print(request)
        else:
            request.mobile_esp_agent = None
            request.device_type = 'desktop'   # default

        client_os = ['_UAgentInfo__isIphone', '_UAgentInfo__isAndroidPhone']
        # print("request.mobile_esp_agent", dir(request.mobile_esp_agent))
        try:
            request.session['_UAgentInfo__isIphone'] = request.mobile_esp_agent.__dict__[
                '_UAgentInfo__isIphone']
            request.session['_UAgentInfo__isAndroidPhone'] = request.mobile_esp_agent.__dict__[
                '_UAgentInfo__isAndroidPhone']
        except KeyError:
            request.session['_UAgentInfo__isIphone'] = 'None'
            request.session['_UAgentInfo__isAndroidPhone'] = 'None'
        if request.device_type == 'desktop':
            request.session['_UAgentInfo__isDesktop'] = 'True'
        else:
            request.session['_UAgentInfo__isDesktop'] = 'False'

"""

# answers the question whether the client is on mobile: True False


class MobileDetectionMiddleware(object):

    user_agents_test_match = (
        "w3c ", "acs-", "alav", "alca", "amoi", "audi",
        "avan", "benq", "bird", "blac", "blaz", "brew",
        "cell", "cldc", "cmd-", "dang", "doco", "eric",
        "hipt", "inno", "ipaq", "java", "jigs", "kddi",
        "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
        "maui", "maxo", "midp", "mits", "mmef", "mobi",
        "mot-", "moto", "mwbp", "nec-", "newt", "noki",
        "xda",  "palm", "pana", "pant", "phil", "play",
        "port", "prox", "qwap", "sage", "sams", "sany",
        "sch-", "sec-", "send", "seri", "sgh-", "shar",
        "sie-", "siem", "smal", "smar", "sony", "sph-",
        "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
        "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
        "wapi", "wapp", "wapr", "webc", "winw", "xda-",)
    user_agents_test_search = u"(?:%s)" % u'|'.join((
        'up.browser', 'up.link', 'mmp', 'symbian', 'smartphone', 'midp',
        'wap', 'phone', 'windows ce', 'pda', 'mobile', 'mini', 'palm',
        'netfront', 'opera mobi',
    ))
    user_agents_exception_search = u"(?:%s)" % u'|'.join((
        'ipad',
    ))
    http_accept_regex = re.compile(
        "application/vnd\.wap\.xhtml\+xml", re.IGNORECASE)

    def __init__(self, get_response):
        self.get_response = get_response
        user_agents_test_match = r'^(?:%s)' % '|'.join(
            self.user_agents_test_match)
        self.user_agents_test_match_regex = re.compile(
            user_agents_test_match, re.IGNORECASE)
        self.user_agents_test_search_regex = re.compile(
            self.user_agents_test_search, re.IGNORECASE)
        self.user_agents_exception_search_regex = re.compile(
            self.user_agents_exception_search, re.IGNORECASE)

    def __call__(self, request):
        response = self.get_response(request)
        self.process_request(request)
        return response

    def process_request(self, request):
        is_mobile = False

        if 'HTTP_USER_AGENT' in request.META:
            print('yessss')
            user_agent = request.META['HTTP_USER_AGENT']

            # Test common mobile values.
            if self.user_agents_test_search_regex.search(user_agent) and \
                    not self.user_agents_exception_search_regex.search(user_agent):
                is_mobile = True
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if 'HTTP_ACCEPT' in request.META:
                    http_accept = request.META['HTTP_ACCEPT']
                    if self.http_accept_regex.search(http_accept):
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                if self.user_agents_test_match_regex.match(user_agent):
                    is_mobile = True

        if is_mobile:
            request.session['is_mobile'] = 'True'
        else:
            request.session['is_mobile'] = 'False'
