# for multiprocess
import asyncio
import aiohttp

# for crawl
import requests
from bs4 import BeautifulSoup as bs

# for checking elapsed time
import time

# import class
from crawler.model.ListPage import ListPage as listpage
from crawler.model.ContentsPage import ContentsPage as contentspage
from crawler.model import Content
from crawler.model import const as const

# database
import crawler.db as database

# import setting values
from crawler.setting import DEBUG, TIME_CHECK

# for matching site name to site class instance
from crawler.model.siteInstanceServer import get_siteInstance_list

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

def site_instance_selector(site):
    return get_siteInstance_list()[site]

async def crawl_manager(site):
    start_time = time.time()
    await asyncio.gather(crawl(site_instance_selector(site)))
    end_time = time.time()
    if(TIME_CHECK):
        print(f'time taken crawling "{site}": {end_time - start_time}')

def get_request(url, header):
    """
    url에서 response 받아 리턴하는 간단한 함수
    """
    response = requests.get(url, headers = header)

    return response

async def get_contents(site, contents_url, urlinfo, db):
    """
    news_url에서 contents 객체를 만들어 리턴하는 함수
    페이지 각각에서 스크래핑하는 기능을 담당하고 있다
    """
    if(DEBUG):
        print(f"Send request to {contents_url}")

    # aiohttp 이용
    async with aiohttp.ClientSession() as sess:
        async with sess.get(contents_url, headers = site.header) as res:
            text = await res.text()
            content_soup = bs(text, 'html.parser')
            news_content = Content.contents_factory(site, contents_url, urlinfo, content_soup)
            # news_content를 쿼리로 쏘는 코드
            db.put_content(news_content)
            time.sleep(const.CRAWLING_PAGE_INTERVAL)

    if(DEBUG):
        print(f"Received request to {contents_url}")

# 나중에는 site뿐만 아니라 subject 역시 매개변수에 넣어서 전달,
# 이후 각 Site 페이지에서 받은 subject 매개변수를 토대로 baseurl을 제작하면 됨
async def crawl(site):
    db = database.DB()

    each_urlbases, urlinfo = site.listpage.get_each_urlbases()

    for urlbase in each_urlbases:
        prev_page = 0
        now_page = 1

        test_breaker = 0

        while prev_page != now_page and test_breaker < 1:
            if(DEBUG):
                print('\nlisturl: ' + urlbase + str(now_page) + '\n')
            response = get_request(urlbase + str(now_page), site.header)

            list_html = response.text
            list_soup = bs(list_html, 'html.parser')

            now_page = site.listpage.get_nowpage(list_soup)
            # 일단 마음에 안 들지만 이렇게 해 두었습니다.
            if(now_page == prev_page):
                break

            contents_urls= site.listpage.get_contents_urls(list_soup)

            futures = [asyncio.ensure_future(get_contents(site, contents_url, urlinfo, db)) for contents_url in contents_urls]

            await asyncio.gather(*futures)

            if(DEBUG):
                print("nowpage: " + str(now_page) + '\n')

            time.sleep(const.CRAWLING_LIST_INTERVAL)

            test_breaker += 1

            prev_page = now_page
            now_page += 1

    db.select_all()
    db.close()