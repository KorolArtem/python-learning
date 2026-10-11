import asyncio
import time
import httpx
import random

class Pinger():
    def __init__(self, timeout=1., verbose=1, use_browser_headers=True):
        self.timeout = timeout
        self.verbose = verbose
        self.headers = None
        if use_browser_headers:
            self.headers = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 OPR/137.0.0.0",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 OPR/137.0.0.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 OPR/137.0.0.0"
                ])
            }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def ping(self, url):
        start_time = time.perf_counter()
        try:
            response = await self.client.head(url, timeout=self.timeout, follow_redirects=True)
            duration = time.perf_counter() - start_time
            if self.verbose>=2:
                print(f"[SUCCESS] {url} | STATUS: {response.status_code} | TIME : {duration:.3f}s")
        except httpx.RequestError as e:
            if self.verbose>=1:
                print(f"[ERROR]   {url} | {type(e).__name__}: {e}")

    async def ping_many(self, urls):
        if self.verbose>=1:
            print(f"Start pinging {len(urls)} urls...")
        
        start_time = time.perf_counter()

        tasks = [self.ping(url) for url in urls]
        await asyncio.gather(*tasks)

        duration = time.perf_counter() - start_time
        if self.verbose>=1:
            print(f"Pinged all urls in {duration:.3f}s")

async def main():
    urls = [
        "https://google.com",
        "https://github.com",
        "https://yandex.ru",
        "https://apple.com",
        "https://microsoft.com",
        "https://wikipedia.org",
        "https://reddit.com",
        "https://amazon.com",
        "https://python.org",
        "https://habr.com",
        "https://never-existed-domain-bla-bla.com"
    ]

    async with Pinger(verbose=2, use_browser_headers=True) as pinger:
        await pinger.ping_many(urls)
        await pinger.ping("https://youtube.com")

if __name__ == "__main__":
    asyncio.run(main())