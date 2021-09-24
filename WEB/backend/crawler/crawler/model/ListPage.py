import json

"""
특정 목록 페이지를 읽기 위한 방법(태그, 클래스 등)을 명시하는 클래스임
걍 설명서임
"""
class ListPage:
    def __init__(self, jsonfile):
        with open(jsonfile, 'r') as f:
            config = json.load(f)
        
        self.name = config['name']

        self.list_div = config['list']['div']
        try:
            self.list_div_class = config['list']['div_class']
        except KeyError:
            self.list_div_class = None

        self.paging_div = config['paging']['div']
        self.paging_div_class = config['paging']['div_class']
        self.paging_tag = config['paging']['tag']

    def get_day_urlbases(self):
        pass

    def get_nowpage(self, soup):
        pass

    def get_contents_urls(self, soup):
        pass