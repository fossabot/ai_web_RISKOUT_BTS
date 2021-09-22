# for scrapping
import requests
from bs4 import BeautifulSoup as bs

# for multiprocess
import asyncio
import aiohttp

# for checking elapesed time
import time

"""
일단 이 방법은 코드 복붙에 준하나, 지금 더 fancy한 방법을 연구하기엔 시간이 없으므로...
프로그램의 크기가 커지면 필연적으로 이곳을 수정할 것이고
그때는 무조건 해결해내야 한다.
"""
if __name__ == '__main__':
    # for unit test
    from config import jsonServer as js

    from model import Content as ct
    from model import NaverListPage as nlp
    from model import NaverNewsPage as nnp

    import const as const
    import db as database
else:
    # for run at main.py
    from crawler.config import jsonServer as js

    from crawler.model import Content as ct
    from crawler.model import NaverListPage as nlp
    from crawler.model import NaverNewsPage as nnp

    import crawler.const as const
    import crawler.db as database

def site_instance_selector(site):
    # return model.siteInstanceServer.get_instance_list[site]
    return None

async def crawl_manager(site):
    start_time = time.time()
    site_instance_selector(site).crawl()
    end_time = time.time()
    print(f'time taken crawling "{site}": {end_time - start_time}')

"""
현재 생각하는 flow
'Naver'같은 이름으로 site_instance_selector이용
get_instance_list에서 받아온 'Naver': NaverClass 와 같은 딕셔너리를 통해
직접 클래스 인스턴스(NaverClass) 에 crawl()명령을 내림

각각 사이트별 클래스에는
목록 사이트
컨텐츠 사이트
2가지가 있음

목록 사이트에 대한 접근은 url조작을 통해
컨텐츠 사이트에 대한 접근은
목록 사이트에서 태그/클래스 를 통한 스크래핑을 통해 접근

컨텐츠 사이트에서 내용을 읽어내는 것 역시
태그/클래스 식별을 통한 스크래핑이다.

새로운 사이트를 만든다면
1.
model 내부에 Naver.py 같은 파일을 만들고
그 안에 목록 사이트, 컨텐츠 사이트에 대한 것을 ListPage.py, NewsPage.py를 상속하여
구현 (이름은 뉴스에 국한되지 않을 것이므로 변경할 예정)

2.
config 내부에 generator.py에
태그/클래스를 기술하여 generator실행

3.
사이트 구조 및 url이 변경된다면 model을 수정
html 및 class 이름이 변경된다면 config.generator를 통해 수정
"""

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
            # news_content를 쿼리로 쏘는 코드
            db.put_content(news_content)

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

        test_breaker = 0
        while prev_page != now_page and test_breaker < 1:
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
            time.sleep(const.CRAWLING_INTERVAL)

            test_breaker += 1

            prev_page = now_page
            now_page += 1

    db.select_all()
    db.close()

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print(f'time taken: {end - start}')
