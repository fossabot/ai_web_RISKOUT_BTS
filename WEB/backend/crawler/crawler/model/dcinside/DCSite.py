from crawler.model.Site import *
from crawler.model.dcinside.const import *

# BASEURL 하드코딩
NAVY = "navy"
DC_BASE = f"https://gall.dcinside.com/board/lists/?id={NAVY}"

DC_CUSTOM_HEADER = {
    'referer' : "https://gall.dcinside.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

class DCListPage(listpage):
    def __init__(self):
        listpage.__init__(self, '/dcinside')

    # override
    def get_each_urlbases(self):
        # + "&page="
        return [DC_BASE + "&page="]

    #override
    def get_contents_urls(self, soup):
        """
        컨텐츠 페이지의 url들을 리스트에 담아 리턴하는 함수,
        실패할 경우 -1을 리턴한다.
        """
        ret = []
        
        list_div = soup.find(self.list_div)
        if(list_div is None):
            if(DEBUG):
                print("can't find list div")
            return -1

        for tr in list_div.find_all("tr", class_ = "ub-content us-post"):
            if(tr.find("td", class_="gall_num").get_text() != "공지"):
                href = tr.find('a')['href']
                ret.append('https://gall.dcinside.com' + href)

        if ret:
            if(DEBUG):
                print("can't find list div")
            return -1

        return ret

class DCContentsPage(contentspage):
    def __init__(self):
        contentspage.__init__(self, '/dcinside')

class DCSite(Site):
    def __init__(self):
        self.name = 'dcinside'
        self.listpage = DCListPage()
        self.contentspage = DCContentsPage()

    async def crawl(self):
        await Site.crawl(self, DC_CUSTOM_HEADER)