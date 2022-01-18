import os
import asyncio
from typing import Dict, List, Tuple, Union, Any
from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse


GIT_TOKEN = os.getenv("GIT_TOKEN")
API_URL = "https://api.github.com"
MAX_PER_PAGE = 100


ContributorsData = List[Dict[str, Any]]

class BusFactorEstimator:
    def __init__(
        self,
        language: str,
        project_count: int,
        sort: str = "stars",
        sorting_order: str = "desc",
    ):
        self._language = language
        assert project_count > 0, project_count
        assert sort in ("stars", "forks", "help-wanted-issues", "updated"), sort
        assert sorting_order in ("asc", "desc"), sorting_order
        self._project_count = project_count
        self._sort = sort
        self._sorting_order = sorting_order
        self._session = None

    def bus_factor_repositories(self) -> List[Dict[str, Union[str, float]]]:
        results = []
        repositories_with_contributors = asyncio.run(self._get_repositories_with_cotributors())

        for name, contributors in repositories_with_contributors.items():
            contributions = [x["contributions"] for x in contributors]
            percentage = round(contributions[0] / sum(contributions), 2)
            if percentage >= 0.75:
                results.append({"project": name, "user": contributors[0]["login"], "percentage": percentage})

        return results

    async def _get_repositories_with_cotributors(self) -> Dict[str, ContributorsData]:
        headers = {"Authorization": f"token {GIT_TOKEN}"}
        async with ClientSession(headers=headers) as session:
            self._session = session
            tasks = []
            names, urls = await self._get_repositories_contributors_urls()
            for url in urls:
                tasks.append(asyncio.create_task(self._get_contributors(url)))

            contributors = await asyncio.gather(*tasks)
            return dict(zip(names, contributors))

    async def _get_repositories_contributors_urls(self) -> Tuple[List[str], List[str]]:
        tasks = []
        pages_number = self._pages
        for page_nr in range(1, pages_number + 1):
            per_page = MAX_PER_PAGE if page_nr < pages_number else self._last_page_nr
            tasks.append(asyncio.create_task(self._get_repositories_page(per_page, page_nr)))

        responses = await asyncio.gather(*tasks)
        repository_names = []
        contributors_urls = []
        for resp in responses:
            for repository in resp:
                repository_names.append(repository["name"])
                contributors_urls.append(repository["contributors_url"])

        return repository_names, contributors_urls

    async def _get_repositories_page(self, per_page, page_nr) -> List[Dict[str, Any]]:
        url = os.path.join(API_URL, "search/repositories")
        params = {
            "q": f"language:{self._language}",
            "sort": self._sort,
            "order": self._sorting_order,
            "per_page": per_page,
            "page": page_nr
        }
        resp = await self._make_request(url, params=params)
        data = await resp.json()
        repositories_info = data.get("items")
        return repositories_info

    async def _get_contributors(self, url: str) -> ContributorsData:
        resp = await self._make_request(url, params={"per_page": 25})
        contributors = await resp.json()
        return contributors

    async def _make_request(self, url: str, *args, **kwargs) -> ClientResponse:
        resp = await self._session.get(url, *args, **kwargs)
        resp.raise_for_status()
        if resp.status != 200:
            resp.raise_for_status()
        return resp

    @property
    def _pages(self) -> int:
        return self._project_count // MAX_PER_PAGE + int(bool(self._project_count % MAX_PER_PAGE))

    @property
    def _last_page_nr(self) -> int:
        remainder = self._project_count % MAX_PER_PAGE
        return remainder if remainder != 0 else MAX_PER_PAGE
