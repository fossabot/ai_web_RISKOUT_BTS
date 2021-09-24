from crawler.config import jsonServer as js_server

from crawler.model.NaverNewsSite import NaverNewsSite as naver
from crawler.model.DCSite import DCSite as dc

def get_siteInstance_list():
    ret = {
        'naver_news': naver(js_server.get_naverlist(), js_server.get_navernews()),
        'dcinside': dc(js_server.get_dclist(), js_server.get_dccontents())
    }

    return ret