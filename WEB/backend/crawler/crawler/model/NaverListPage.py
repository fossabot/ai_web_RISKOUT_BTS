from . import ListPage as lp
from . import const as const

from datetime import datetime, timedelta

class NaverListPage(lp.ListPage):
    def __init__(self, jsonfile):
        lp.ListPage.__init__(self, jsonfile)

    # override
    def get_eachday_urlbases(self):
        date = datetime.today()
        date_format = date.strftime("%Y%m%d")
        # 맨 뒤에 페이지 번호 숫자(1~9999등)을 붙여 페이지를 이동하기 위함.
        eachday_urlbases = [const.NAVER_BASE] * const.CRAWL_DATEAMOUNT

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


if __name__ == '__main__':
    pass