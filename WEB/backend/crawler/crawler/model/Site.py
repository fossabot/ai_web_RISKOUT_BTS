from crawler.model.ListPage import ListPage as listpage
from crawler.model.ContentsPage import ContentsPage as contentspage
from crawler.model import Content
from crawler.model import const as const
import crawler.const as crawler_const

import crawler.db as database

from datetime import datetime, timedelta

# for multiprocess
import asyncio
import aiohttp

# for crawl
import requests
from bs4 import BeautifulSoup as bs

# for checking elapesed time
import time

class Site:
    def __init__(self, listjson, contentjson):
        self.listpage = listpage(listjson)
        self.contentspage = contentspage(contentjson)

    def get_request(self, url):
        pass

    async def get_contents(self, news_url, news_page, db):
        pass

    def crawl(self):
        pass