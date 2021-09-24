from crawler.model.ListPage import ListPage as listpage
from crawler.model.ContentsPage import ContentsPage as contentspage
from crawler.model import Content
from crawler.model import const as const

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

    async def get_contents(self, contents_url, contentspage, db, header):
        """
        news_url에서 contents 객체를 만들어 리턴하는 함수
        페이지 각각에서 스크래핑하는 기능을 담당하고 있다
        """
        print(f"Send request to {contents_url}")

        # aiohttp 이용
        async with aiohttp.ClientSession() as sess:
            async with sess.get(contents_url, headers = header) as res:
                text = await res.text()
                content_soup = bs(text, 'html.parser')
                news_content = Content.contents_factory(contents_url, content_soup, contentspage)
                # news_content를 쿼리로 쏘는 코드
                db.put_content(news_content)

        print(f"Received request to {contents_url}")

    async def crawl(self, header):
        db = database.DB()

        each_urlbases = self.listpage.get_each_urlbases()

        for urlbase in each_urlbases:
            prev_page = 0
            now_page = 1

            test_breaker = 0

            while prev_page != now_page and test_breaker < 1:
                print('\nlisturl: ' + urlbase + str(now_page) + '\n')
                response = self.get_request(urlbase + str(now_page), header)
                
                list_html = response.text
                list_soup = bs(list_html, 'html.parser')

                now_page = self.listpage.get_nowpage(list_soup)
                # 일단 마음에 안 들지만 이렇게 해 두었습니다.
                if(now_page == prev_page):
                    break

                contents_urls= self.listpage.get_contents_urls(list_soup)

                futures = [asyncio.ensure_future(self.get_contents(contents_url, self.contentspage, db, header)) for contents_url in contents_urls]

                await asyncio.gather(*futures)

                print("nowpage: " + str(now_page) + '\n')
                time.sleep(const.CRAWLING_INTERVAL)

                test_breaker += 1

                prev_page = now_page
                now_page += 1

        # db.select_all()
        db.close()