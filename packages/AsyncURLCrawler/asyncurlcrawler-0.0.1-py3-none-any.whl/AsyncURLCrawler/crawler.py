from typing import List, Dict
from AsyncURLCrawler.url_utils import (
    validate_urls,
    have_same_domain,
    have_exact_domain,
)
from collections import deque
from AsyncURLCrawler.parser import Parser
import asyncio


class Crawler:

    def __init__(self, seed_urls: List[str],
                 parser: Parser,
                 deep: bool = False,
                 exact: bool = True,
                 delay: float = 0):
        self._set_seed_urls(seed_urls)
        self._parser = parser
        self._deep = deep
        self._exact = exact
        self._delay = delay

    def _set_seed_urls(self, seed_urls: List[str]) -> None:
        validate_urls(seed_urls)
        self._seed_urls = seed_urls
        self._visited_urls = dict.fromkeys(seed_urls, set())

    def _update_queue(self, extracted_url: str, root_url: str) -> None:
        if self._deep:
            self._queue.append(extracted_url)
        else:
            if self._exact:
                if have_exact_domain(extracted_url, root_url):
                    self._queue.append(extracted_url)
            else:
                if have_same_domain(extracted_url, root_url):
                    self._queue.append(extracted_url)

    def _reset_queue(self) -> None:
        self._queue = deque()

    async def crawl(self) -> Dict:
        for root_url in self._seed_urls:
            self._reset_queue()
            self._queue.append(root_url)
            while self._queue:
                current_url = self._queue.popleft()
                self._parser.reset()
                extracted_urls = await self._parser.probe(current_url)
                for extracted_url in extracted_urls:
                    if extracted_url not in self._visited_urls[root_url]:
                        self._visited_urls[root_url].add(extracted_url)
                        self._update_queue(extracted_url, root_url)
                await asyncio.sleep(self._delay)
        return self._visited_urls

    def get_visited_urls(self) -> Dict:
        return self._visited_urls
