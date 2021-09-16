import requests
from bs4 import BeautifulSoup as bs
import time

# 앞으로는 date와 page를 for 문으로 돌면서 검색하는 함수 만들면 될듯
TARGET_URL = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=268&sid1=100&date=20210916&page=1"
custom_header = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def scrap_body_contents(soup):
    div = soup.find("div", class_="_article_body_contents")
    
    result = div.get_text()

    # print(result)
    return result

def get_contents(soup):
    ret = []

    div = soup.find("div", class_ = 'list_body newsflash_body')

    for dt in div.find_all("dt", class_="photo"):
        temp_dict = {}
        href = dt.find('a')['href']
        temp_dict['href'] = href
        temp_dict['img'] = dt.find('img')['src']
        temp_dict['title'] = dt.find('img')['alt'] # 일단은 테스트로 제목을 img의 alt로 가져왔지만 수정이 필요함. crawling함수 안에서 처리할 수도 있을 듯
        temp_dict['body_contents'] = str.strip(scrap_body_contents(bs(requests.get(href, headers = custom_header).text, "html.parser")))

        ret.append(temp_dict)

    return ret

def get_request(url):
    response = requests.get(url, headers = custom_header)

    return response


def main():
    cur_time = time.time()
    response = get_request(TARGET_URL)

    newslist_html = response.text
    newslist_soup = bs(newslist_html, 'html.parser')

    news_contents = get_contents(newslist_soup)
    
    for tmp in news_contents:
        print("title: " + tmp['title'] + "\nhref: " + tmp['href'] + "\nimage: " + tmp['img'] + '\ncontent:\n' + tmp['body_contents'] + '\n\n')

    print("\n\n\n" + str(time.time() - cur_time))

if __name__ == '__main__':
    main()