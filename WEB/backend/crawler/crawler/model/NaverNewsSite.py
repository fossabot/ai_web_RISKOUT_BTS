from crawler.model.Site import *
from crawler.model.ListPage import ListPage as listpage
from crawler.model.ContentsPage import ContentsPage as contentspage

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
    def get_eachday_urlbases(self):
        date = datetime.today()
        date_format = date.strftime("%Y%m%d")
        # 맨 뒤에 페이지 번호 숫자(1~9999등)을 붙여 페이지를 이동하기 위함.
        eachday_urlbases = [NAVER_BASE] * const.CRAWL_DATEAMOUNT

        for i in range(const.CRAWL_DATEAMOUNT):
            eachday_urlbases[i] += f"&date={date_format}&page="
            date -= timedelta(days=1)
            date_format = date.strftime("%Y%m%d")

        return eachday_urlbases

    # override
    def get_nowpage(self, soup):
        page_div = soup.find(self.paging_div, class_ = self.paging_div_class)

        nowpage = int(page_div.find(self.paging_tag).get_text())

        return nowpage

    def get_news_urls(self, soup):
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
    
    def get_request(self, url):
        """
        url에서 response 받아 리턴하는 간단한 함수
        """
        response = requests.get(url, headers = NAVER_CUSTOM_HEADER)

        return response

    async def get_contents(self, news_url, news_page, db):
        """
        news_url에서 contents 객체를 만들어 리턴하는 함수
        페이지 각각에서 스크래핑하는 기능을 담당하고 있다
        """
        print(f"Send request to {news_url}")

        # aiohttp 이용
        async with aiohttp.ClientSession() as sess:
            async with sess.get(news_url, headers = NAVER_CUSTOM_HEADER) as res:
                text = await res.text()
                content_soup = bs(text, 'html.parser')
                news_content = Content.contents_factory(news_url, content_soup, news_page)
                # news_content를 쿼리로 쏘는 코드
                db.put_content(news_content)

        print(f"Received request to {news_url}")

    async def crawl(self):
        db = database.DB()

        eachday_urlbases = self.listpage.get_eachday_urlbases()

        for urlbase in eachday_urlbases:
            prev_page = 0
            now_page = 1

            test_breaker = 0

            while prev_page != now_page and test_breaker < 1:
                response = self.get_request(urlbase + str(now_page))
                print('\nlisturl: ' + urlbase + str(now_page) + '\n')

                newslist_html = response.text
                newslist_soup = bs(newslist_html, 'html.parser')

                now_page = self.listpage.get_nowpage(newslist_soup)
                # 일단 마음에 안 들지만 이렇게 해 두었습니다.
                if(now_page == prev_page):
                    break

                news_urls= self.listpage.get_news_urls(newslist_soup)

                futures = [asyncio.ensure_future(self.get_contents(news_url, self.contentspage, db)) for news_url in news_urls]

                await asyncio.gather(*futures)

                print("nowpage: " + str(now_page) + '\n')
                time.sleep(crawler_const.CRAWLING_INTERVAL)

                test_breaker += 1

                prev_page = now_page
                now_page += 1

        db.select_all()
        db.close()