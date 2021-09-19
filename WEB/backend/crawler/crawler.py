# for scrapping
import requests
from bs4 import BeautifulSoup as bs

# for multiprocess
import asyncio
import aiohttp

# for checking elapesed time
import time

# for build-up naver news url
from datetime import datetime, timedelta

from model import *
from const import *


def get_news_urls(soup):
    """
    page 안에서 세부 뉴스들의 url을 찾아 리스트 형태로 리턴하는 함수
    """
    ret = []
    div = soup.find("div", class_ = 'list_body newsflash_body')

    for dt in div.find_all("dt", class_="photo"):
        href = dt.find('a')['href']
        ret.append(href)

    return ret

def get_listamount(soup):
    """
    first page안에서 페이지 목록 개수를 리턴하는 함수
    """
    div = soup.find("div", class_="paging")
    hrefs = div.find_all('a')
    return len(hrefs)

def get_request(url):
    """
    url에서 response 받아 리턴하는 간단한 함수
    """
    response = requests.get(url, headers = CUSTOM_HEADER)

    return response

async def get_contents(news_url):
    """
    news_url에서 contents 객체를 만들어 리턴하는 함수
    페이지 각각에서 스크래핑하는 기능을 담당하고 있다
    """
    print(f"Send request to {news_url}")

    # aiohttp 이용
    async with aiohttp.ClientSession() as sess:
        async with sess.get(news_url, headers = CUSTOM_HEADER) as res:
            text = await res.text()
            content_soup = bs(text, 'html.parser')
            news_content = contents_factory(news_url, content_soup)
            # TODO news_content를 쿼리로 쏘는 코드 작성

    print(f"Received request to {news_url}")

async def main():
    date = datetime.today()
    date_format = date.strftime("%Y%m%d")
    # 맨 뒤에 페이지 번호 숫자(1~9999등)을 붙여 페이지를 이동하기 위함.
    eachday_urlbases = [NAVER_BASE] * CRAWL_DATEAMOUNT
    
    for i in range(CRAWL_DATEAMOUNT):
        eachday_urlbases[i] += f"&date={date_format}&page="
        date -= timedelta(days=1)
        date_format = date.strftime("%Y%m%d")
    
    for urlbase in eachday_urlbases:
        print("urlbase: " + urlbase)

        for i in range(1, MAX_LISTPAGE_CRAWL): # TODO 페이지의 끝까지 다다랐을 때 탈출할 수 있도록 조정해야 함
            response = get_request(urlbase + str(i))

            newslist_html = response.text
            newslist_soup = bs(newslist_html, 'html.parser')

            news_urls= get_news_urls(newslist_soup)

            futures = [asyncio.ensure_future(get_contents(news_url)) for news_url in news_urls]

            await asyncio.gather(*futures)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print(f'time taken: {end - start}')
