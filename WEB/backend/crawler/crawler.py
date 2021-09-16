import requests
from bs4 import BeautifulSoup as bs

custom_header = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

def crawling(soup):
    div = soup.find("div", class_="_article_body_contents")
    
    result = div.get_text()

    # print(result)
    return result

def get_href(soup):
    href = []
    img = []
    title = []

    div = soup.find("div", class_ = 'list_body newsflash_body')

    
    for dt in div.find_all("dt", class_="photo"):
        href.append(dt.find('a')['href'])
        img.append(dt.find('img')['src'])
        title.append(dt.find('img')['alt']) # 일단은 테스트로 제목을 img의 alt로 가져왔지만 수정이 필요함. crawling함수 안에서 처리할 수도 있을 듯

    return zip(href, img, title)

def get_request(url):
    response = requests.get(url, headers = custom_header)

    return response


def main():
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=100&sid2=268"
    response = get_request(url)

    html= response.text
    soup = bs(html, 'html.parser')

    href_img_list = get_href(soup)

    # print(href_img_list)

    result = []

    for href, img, title in href_img_list:
        href_req = requests.get(href, headers = custom_header)
        href_soup = bs(href_req.text, "html.parser")
        temp = []
        temp.append(str.strip(crawling(href_soup)))
        
        temp.append(img)
        temp.append(title)
        temp.append(href)
        result.append(temp)
    
    for tmp in result:
        print("title: " + tmp[2] + "\nhref: " + tmp[3] + "\nimage: " + tmp[1] + '\ncontent:\n' + tmp[0] + '\n\n')

if __name__ == '__main__':
    main()