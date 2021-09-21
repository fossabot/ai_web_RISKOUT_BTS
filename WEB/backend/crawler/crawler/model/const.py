#네이버 뉴스 하드코딩
POLITICS = 100
NORTH_KOREA = 268

NAVER_BASE = f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={NORTH_KOREA}&sid1={POLITICS}"


# 크롤링할 날짜 수
CRAWL_DATEAMOUNT = 1

# 테스트용으로 크롤링할 페이지 수 제한
MAX_LISTPAGE_CRAWL = 2