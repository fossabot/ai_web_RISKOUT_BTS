# for scrapping
import requests
from bs4 import BeautifulSoup as bs

# for multiprocess
import asyncio
import aiohttp

# for checking elapesed time
import time

from config import jsonServer as js

from model import Content as ct
from model import NaverListPage as nlp
from model import NaverNewsPage as nnp
import const as const
import db as database

def get_request(url):
    """
    url에서 response 받아 리턴하는 간단한 함수
    """
    response = requests.get(url, headers = const.NAVER_CUSTOM_HEADER)

    return response

async def get_contents(news_url, news_page, db):
    """
    news_url에서 contents 객체를 만들어 리턴하는 함수
    페이지 각각에서 스크래핑하는 기능을 담당하고 있다
    """
    print(f"Send request to {news_url}")

    # aiohttp 이용
    async with aiohttp.ClientSession() as sess:
        async with sess.get(news_url, headers = const.NAVER_CUSTOM_HEADER) as res:
            text = await res.text()
            content_soup = bs(text, 'html.parser')
            news_content = ct.contents_factory(news_url, content_soup, news_page)
            # TODO news_content를 쿼리로 쏘는 코드 작성
            # db.put_content(news_content)

    print(f"Received request to {news_url}")

async def main():
    db = database.DB()

    # NaverListPage 객체 생성 및 기본 URL 얻기
    naver_list_page = nlp.NaverListPage(js.get_naverlist())
    eachday_urlbases = naver_list_page.get_eachday_urlbases()

    # NaverNewsPage 객체 생성
    naver_news_page = nnp.NaverNewsPage(js.get_navernews())
    
    for urlbase in eachday_urlbases:
        print("urlbase: " + urlbase)

        prev_page = 0
        now_page = 1
        # for i in range(1, MAX_LISTPAGE_CRAWL):
        # 아직 now_page를 읽어오는 함수가 검증되지 않았으므로, 테스트를 끝내기 위한 조건 추가
        test_breaker = 0
        while prev_page != now_page or test_breaker < 5:
            response = get_request(urlbase + str(now_page))
            print('\nlisturl: ' + urlbase + str(now_page) + '\n')

            newslist_html = response.text
            newslist_soup = bs(newslist_html, 'html.parser')

            now_page = naver_list_page.get_nowpage(newslist_soup)
            # 일단 마음에 안 들지만 이렇게 해 두었습니다.
            if(now_page == prev_page):
                break

            news_urls= naver_list_page.get_news_urls(newslist_soup)

            futures = [asyncio.ensure_future(get_contents(news_url, naver_news_page, db)) for news_url in news_urls]

            await asyncio.gather(*futures)

            print("nowpage: " + str(now_page) + '\n')
            time.sleep(2)

            test_breaker += 1

            prev_page = now_page
            now_page += 1


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print(f'time taken: {end - start}')
