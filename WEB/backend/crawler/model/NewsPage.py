import json

# 특정 뉴스 페이지를 읽기 위한 방법(태그, 클래스 등)을 명시하는 클래스임
# 따라서 가급적 메소드 추가하지 않는 방향으로 갈 것
class NewsPage:
    def __init__(self, jsonfile):
        config = json.load(jsonfile)
        self.name = config['name']

        # title
        # div와 div_class를 통해 해당 데이터 주변에 접근
        # tag를 통해 정확한 데이터 확보
        self.title_div = config['title']['div']
        self.title_div_class = config['title']['div_class']
        self.title_tag = config['title']['tag']

        # body
        self.body_div = config['body']['div']
        self.body_div_class = config['body']['div_class']

        # img
        self.img_div = config['img']['div']
        self.img_div_class = config['img']['div_class']


class NaverNewsPage(NewsPage):
    def __init__(self, jsonfile):
        NewsPage.__init__(self, jsonfile)
