from crawler.config import jsonServer as js_server

from crawler.model.NaverNewsSite import NaverNewsSite as naver

def get_siteInstance_list():
    ret = {
        'naver_news': naver(js_server.get_naverlist(), js_server.get_navernews())
    }

    return ret