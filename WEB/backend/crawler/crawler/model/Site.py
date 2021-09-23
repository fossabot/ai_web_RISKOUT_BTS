from crawler.model.ListPage import ListPage as listpage
from crawler.model.ContentsPage import ContentsPage as contentspage
from crawler.model import Content
from crawler.model import const as const
import crawler.const as crawler_const

import crawler.db as database

from datetime import datetime, timedelta

# for multiprocess
import asyncio
import aiohttp

# for crawl
import requests
from bs4 import BeautifulSoup as bs

# for checking elapesed time
import time

class Site:
    def __init__(self, listjson, contentjson):
        self.listpage = listpage(listjson)
        self.contentspage = contentspage(contentjson)

    def get_request(self, url, header):
        """
        url에서 response 받아 리턴하는 간단한 함수
        """
        response = requests.get(url, headers = header)

        return response

    async def get_contents(self, news_url, news_page, db, header):
        """
        news_url에서 contents 객체를 만들어 리턴하는 함수
        페이지 각각에서 스크래핑하는 기능을 담당하고 있다
        """
        print(f"Send request to {news_url}")

        # aiohttp 이용
        async with aiohttp.ClientSession() as sess:
            async with sess.get(news_url, headers = header) as res:
                text = await res.text()
                content_soup = bs(text, 'html.parser')
                news_content = Content.contents_factory(news_url, content_soup, news_page)
                # news_content를 쿼리로 쏘는 코드
                db.put_content(news_content)

        print(f"Received request to {news_url}")

    async def crawl(self, header):
        db = database.DB()

        eachday_urlbases = self.listpage.get_eachday_urlbases()

        for urlbase in eachday_urlbases:
            prev_page = 0
            now_page = 1

            test_breaker = 0

            while prev_page != now_page and test_breaker < 1:
                response = self.get_request(urlbase + str(now_page), header)
                print('\nlisturl: ' + urlbase + str(now_page) + '\n')

                newslist_html = response.text
                newslist_soup = bs(newslist_html, 'html.parser')

                now_page = self.listpage.get_nowpage(newslist_soup)
                # 일단 마음에 안 들지만 이렇게 해 두었습니다.
                if(now_page == prev_page):
                    break

                news_urls= self.listpage.get_news_urls(newslist_soup)

                futures = [asyncio.ensure_future(self.get_contents(news_url, self.contentspage, db, header)) for news_url in news_urls]

                await asyncio.gather(*futures)

                print("nowpage: " + str(now_page) + '\n')
                time.sleep(crawler_const.CRAWLING_INTERVAL)

                test_breaker += 1

                prev_page = now_page
                now_page += 1

        db.select_all()
        db.close()