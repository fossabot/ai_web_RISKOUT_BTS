from crawler.model.Site import *

# BASEURL 하드코딩
NAVY = "navy"
DC_BASE = f"https://gall.dcinside.com/board/lists/?id={NAVY}"

DC_CUSTOM_HEADER = {
    'referer' : "https://gall.dcinside.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

class DCListPage(listpage):
    def __init__(self, jsonfile):
        listpage.__init__(self, jsonfile)

    # override
    def get_each_urlbases(self):
        # + "&page="
        return [DC_BASE + "&page="]

    # override
    def get_nowpage(self, soup):
        page_div = soup.find(self.paging_div, class_ = self.paging_div_class)

        nowpage = int(page_div.find(self.paging_tag).get_text())
        
        return nowpage

    #override
    def get_contents_urls(self, soup):
        ret = []

        list_div = soup.find(self.list_div)

        for tr in list_div.find_all("tr", class_ = "ub-content us-post"):
            if(tr.find("td", class_="gall_num").get_text() != "공지"):
                href = tr.find('a')['href']
                ret.append('https://gall.dcinside.com' + href)

        return ret



class DCContentsPage(contentspage):
    def __init__(self, jsonfile):
        contentspage.__init__(self, jsonfile)

class DCSite(Site):
    def __init__(self, listjson, contentjson):
        self.listpage = DCListPage(listjson)
        self.contentspage = DCContentsPage(contentjson)

    async def crawl(self):
        await Site.crawl(self, DC_CUSTOM_HEADER)