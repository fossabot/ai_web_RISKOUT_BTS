from crawler.model.naver.NaverNewsSite import NaverNewsSite
from crawler.model.dcinside.DCSite import DCSite

def get_siteInstance_list():
    ret = {
        'naver_news': NaverNewsSite(),
        'dcinside': DCSite()
    }

    return ret

    