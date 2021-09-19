import json

"""
특정 뉴스 목록 페이지를 읽기 위한 방법(태그, 클래스 등)을 명시하는 클래스임
따라서 가급적 메소드 추가하지 않는 방향으로 갈 것.
걍 설명서임
"""
class ListPage:
    def __init__(self, jsonfile):
        config = json.load(jsonfile)
        self.name = config['name']

        self.list_div = config['list']['div']
        self.list_div_class = config['list']['div_class']

# 일단 네이버 뉴스에만 적용되므로 이건 파일을 따로 안 나눔
class NaverListpage(ListPage):
    def __init__(self, jsonfile):
        ListPage.__init__(self, jsonfile)