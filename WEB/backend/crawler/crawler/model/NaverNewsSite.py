from crawler.model.Site import *

#네이버 뉴스 하드코딩
POLITICS = 100
NORTH_KOREA = 268

NAVER_BASE = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={NORTH_KOREA}&sid1={POLITICS}"

NAVER_CUSTOM_HEADER = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

class NaverNewsListPage(listpage):
    def __init__(self, jsonfile):
        listpage.__init__(self, jsonfile)

    # override
    def get_each_urlbases(self):
        date = datetime.today()
        date_format = date.strftime("%Y%m%d")
        # 맨 뒤에 페이지 번호 숫자(1~9999등)을 붙여 페이지를 이동하기 위함.
        each_urlbases = [NAVER_BASE] * const.CRAWL_DATEAMOUNT

        for i in range(const.CRAWL_DATEAMOUNT):
            each_urlbases[i] += f"&date={date_format}&page="
            date -= timedelta(days=1)
            date_format = date.strftime("%Y%m%d")

        return each_urlbases

    # override
    def get_nowpage(self, soup):
        page_div = soup.find(self.paging_div, class_ = self.paging_div_class)

        nowpage = int(page_div.find(self.paging_tag).get_text())

        return nowpage

    def get_contents_urls(self, soup):
        """
        page 안에서 뉴스들의 url을 찾아 리스트 형태로 리턴하는 함수
        """
        ret = []
        div = soup.find(self.list_div, class_ = self.list_div_class)

        """
        일단은 사진에 붙어있는 링크를 이용하는 방법.
        즉, 사진이 없으면 링크가 없음.
        근데 사진이 없는 경우에 대한 예외처리가 있음 ㅋㅋ
        사진 없으면 작동을 안한다는건데, 모르겠다 아직
        """
        for dt in div.find_all("dt", class_="photo"):
            href = dt.find('a')['href']
            ret.append(href)

        return ret


class NaverNewsContentsPage(contentspage):
    def __init__(self, jsonfile):
        contentspage.__init__(self, jsonfile)


class NaverNewsSite(Site):
    def __init__(self, listjson, contentsjson):
        self.listpage = NaverNewsListPage(listjson)
        self.contentspage = NaverNewsContentsPage(contentsjson)

    async def crawl(self):
        await Site.crawl(self, NAVER_CUSTOM_HEADER)