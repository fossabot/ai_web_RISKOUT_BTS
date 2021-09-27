class CrawlerError(Exception):
    def __init__(self, msg = "basic error"):
        self.msg = msg

    def __str__(self):
        return self.msg

class PageDivNotFoundError(CrawlerError):
    def __init__(self, msg = "PageDivNotFoundError: can't find page div"):
        self.msg = msg

class PagingTagNotFoundError(CrawlerError):
    def __init__(self, msg = "PagingTagNotFoundError: can't find pageing tag"):
        self.msg = msg
