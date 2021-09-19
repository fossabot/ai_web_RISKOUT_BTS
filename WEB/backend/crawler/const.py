#네이버 뉴스 하드코딩
POLITICS = 100
NORTH_KOREA = 268

NAVER_BASE = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={NORTH_KOREA}&sid1={POLITICS}"
CUSTOM_HEADER = {
    'referer' : "https://www.naver.com/",
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

# 크롤링할 날짜 수
CRAWL_DATEAMOUNT = 1

# 테스트용으로 크롤링할 페이지 수 제한
MAX_LISTPAGE_CRAWL = 2