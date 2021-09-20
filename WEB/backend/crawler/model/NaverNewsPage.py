from . import NewsPage as np

class NaverNewsPage(np.NewsPage):
    def __init__(self, jsonfile):
        np.NewsPage.__init__(self, jsonfile)
