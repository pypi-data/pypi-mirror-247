from httpx import Response, AsyncClient, ConnectTimeout
import asyncio
from typing import List
from bs4 import BeautifulSoup
from AsyncURLCrawler.url_utils import normalize_url, validate_url


class Parser:
    def __init__(self, delay_start: float = 0.1, max_retries: int = 5,
                 request_timeout: float = 1, user_agent=': str = Mozilla/5.0'):
        self._delay_start = delay_start
        self._current_delay = delay_start
        self._max_retries = max_retries
        self._request_timeout = request_timeout
        self._current_retry = 0
        self._user_agent = user_agent

    def reset(self):
        self._current_retry = 0
        self._current_delay = self._delay_start

    async def _fetch_page(self, url: str) -> [Response, None]:
        # TODO Check file format before fetching! ignore jpg, pdf, ...
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    timeout=self._request_timeout,
                    headers={"User-Agent": self._user_agent},
                )
            except ConnectTimeout:
                return None
            return response

    def _extract_urls(self, response: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(response, 'html.parser')
        urls = list()
        for link in soup.find_all('a', href=True):
            n_link = normalize_url(link.get('href'), base_url)
            if validate_url(n_link):
                urls.append(n_link)
        return urls

    async def probe(self, url: str) -> List[str]:
        # TODO Check response size!
        response = await self._fetch_page(url)
        status_code = None
        if response:
            status_code = response.status_code
        while status_code is None or status_code == 429 or status_code >= 500:
            if self._current_retry == self._max_retries:
                break
            await asyncio.sleep(self._current_delay)
            self._current_delay *= pow(2, self._current_retry)
            self._current_retry += 1
            response = await self._fetch_page(url)
            if response:
                status_code = response.status_code
        if status_code != 200:
            return []
        urls = self._extract_urls(response.text, url)
        return urls
