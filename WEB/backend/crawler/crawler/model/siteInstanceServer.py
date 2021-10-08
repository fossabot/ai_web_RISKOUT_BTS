from crawler.model.naver.NaverNewsSite import NaverNewsSite
from crawler.model.dcinside.DCSite import DCSite
from crawler.model.twitter.Twitter import Twitter

def get_siteInstance_list():
    ret = {
        'naver_news': NaverNewsSite(),
        'dcinside': DCSite(),
        'twitter': Twitter()
    }

    return ret

    