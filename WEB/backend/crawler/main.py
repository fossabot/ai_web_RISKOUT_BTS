import asyncio
from crawler import crawl

async def main():
    site_list = [
        'NaverNews'
    ]
    
    futures = [asyncio.ensure_future(crawl(site)) for site in site_list]

    await asyncio.gather(*futures)


if __name__ == '__main__':
    main()
    