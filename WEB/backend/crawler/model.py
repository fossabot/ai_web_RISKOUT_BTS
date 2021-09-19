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

def contents_factory(news_url, soup):
    """
    페이지 soup을 이용해 Content 객체를 리턴하는 함수
    news_url은 그저 Content를 생성하기 위해 전달받았다.
    """
    title_div = soup.find("div", class_="article_info")
    body_div = soup.find("div", class_="_article_body_contents")
    img_div = soup.find("span", class_="end_photo_org")
    
    try:
        title = title_div.find('h3').get_text()
    except:
        title = "No Title"
    img_url = img_div.find('img')['src']
    body = str.strip(body_div.get_text())

    content = Content(news_url, title, body, img_url)

    print(content)
    return content


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


