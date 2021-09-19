# for scrapping
import requests
from bs4 import BeautifulSoup as bs

# for multiprocess
import asyncio
import aiohttp
from functools import partial

# for checking elapesed time
import time

# 앞으로는 date와 page를 for 문으로 돌면서 검색하는 함수 만들면 될듯
TARGET_URL = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=100&sid2=268"
CUSTOM_HEADER = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

class Content:
    """
    페이지의 내용에 대한 모델
    url, 제목, 내용, 대표 이미지가 있다.
    """
    def __init__(self, url, title, body, img_url):
        self.url = url
        self.title = title
        self.body = body
        self.img_url = img_url

    def __str__(self):
        result = ""
        result += f"URL: {self.url}\n"
        result += f"Title: {self.title}\n"
        result += f"Body: {self.body[:25]}\n"
        result += f"Img_url: {self.img_url}\n"
        return result

class Website:
    """
    일단은 미래를 위해 추가했다. 네이버 뉴스에 국한되지 않으려면 필요할 것 같은데 아직은 잘 모르겠수
    """
    def __init__(self, name, url, titleTag, bodyTag, imgTag):
        self.name = name
        self.url = url
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        self.imgTag = imgTag


def contents_factory(news_url, soup):
    """
    페이지 soup을 이용해 Content 객체를 리턴하는 함수
    news_url은 그저 Content를 생성하기 위해 전달받았다.
    """
    title_div = soup.find("div", class_="article_info")
    body_div = soup.find("div", class_="_article_body_contents")
    
    
    title = title_div.find('h3').get_text()
    img_url = body_div.find('img')['src']
    body = str.strip(body_div.get_text())

    content = Content(news_url, title, body, img_url)

    print(content)
    return content

def get_urls(soup):
    """
    main page 안에서 세부 뉴스들의 url을 찾아 리스트 형태로 리턴하는 함수
    """
    ret = []
    div = soup.find("div", class_ = 'list_body newsflash_body')

    for dt in div.find_all("dt", class_="photo"):
        href = dt.find('a')['href']
        ret.append(href)

    return ret

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
            # print(text.strip()[:100])
            content_soup = bs(text, 'html.parser')
            news_content = contents_factory(news_url, content_soup)
            # TODO news_content를 쿼리로 쏘는 코드 작성

    print(f"Received request to {news_url}")

async def main():
    response = get_request(TARGET_URL)

    newslist_html = response.text
    newslist_soup = bs(newslist_html, 'html.parser')

    news_urls= get_urls(newslist_soup)

    futures = [asyncio.ensure_future(get_contents(news_url)) for news_url in news_urls]

    await asyncio.gather(*futures)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()

    print(f'time taken: {end - start}')