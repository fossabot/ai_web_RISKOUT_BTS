import requests
from bs4 import BeautifulSoup as bs

custom_header = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def crawling(soup):
    div = soup.find("div", class_="_article_body_contents")
    
    result = div.get_text()

    print(result)
    return None

def get_href(soup):
    result = []

    div = soup.find("div", class_ = 'list_body newsflash_body')

    for dt in div.find_all("dt", class_="photo"):
        result.append(dt.find('a')['href'])

    return result

def get_request(url):
    response = requests.get(url, headers = custom_header)

    return response


def main():
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=100&sid2=268"
    response = get_request(url)

    html= response.text
    soup = bs(html, 'html.parser')

    href_list = get_href(soup)

    print(href_list)

    result = []

    for href in href_list:
        href_req = requests.get(href, headers = custom_header)
        href_soup = bs(href_req.text, "html.parser")
        result.append(crawling(href_soup))
    
    print(result)

if __name__ == '__main__':
    main()