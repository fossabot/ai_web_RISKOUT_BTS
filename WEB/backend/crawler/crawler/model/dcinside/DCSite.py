from crawler.model.Site import *
from crawler.model.dcinside.const import *

class DCListPage(listpage):
    def __init__(self):
        listpage.__init__(self, '/dcinside')

    # override
    def get_each_urlbases(self):
        # + "&page="
        urlinfo = URLInfo(DOMAIN, NAVY, None)
        return [DC_BASE + "&page="], urlinfo

    #override
    def get_contents_urls(self, soup):
        """
        컨텐츠 페이지의 url들을 리스트에 담아 리턴하는 함수,
        실패할 경우 -1을 리턴한다.
        """
        ret = []
        
        list_div = soup.find(self.list_div, class_=self.list_div_class)
        # print(list_div.prettify())
        if(list_div is None):
            if(DEBUG):
                print("in DCSite.py/DCSitePage/get_contents_urls: can't find list div")
            return -1

        for li in list_div.find_all("div", class_="gall-detail-lnktb"):
            href = li.find('a', class_='lt')['href']
            ret.append(href)

        if not ret:
            if(DEBUG):
                print("in DCSite.py/DCSitePage/get_contents_urls: can't find contents on list div")
            return -1

        return ret

class DCContentsPage(contentspage):
    def __init__(self):
        contentspage.__init__(self, '/dcinside')

class DCSite(Site):
    def __init__(self):
        self.name = 'dcinside'
        self.category = 'social'
        self.listpage = DCListPage()
        self.contentspage = DCContentsPage()
        self.header = DC_CUSTOM_HEADER

    def get_articleID(self, contents_url):
        return "1"





