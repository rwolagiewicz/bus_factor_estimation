import asyncio
import os

from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse

GIT_TOKEN = os.getenv("GIT_TOKEN")
API_URL = "https://api.github.com"
MAX_PER_PAGE = 100
BUS_FACTOR_THRESHOLD = 0.75

SORTING_TYPES = ("stars", "forks", "help-wanted-issues", "updated")
SORTING_ORDERS = ("asc", "desc")


class BusFactorEstimator:
    """
    Alows to extract list of projects for provided programming languague on github,
    having its bus factor equal 1.
    """

    def __init__(
        self,
        language: str,
        project_count: int,
        sort: str = "stars",
        sorting_order: str = "desc",
    ):
        self._language = language
        self._project_count = int(project_count)
        self._sort = sort
        self._sorting_order = sorting_order
        self._session: ClientSession | None = None

        if self._project_count <= 0:
            raise ValueError("project_count must be greater than 0!")
        if sort not in SORTING_TYPES:
            raise ValueError(f"sort must be on of: {SORTING_TYPES}")
        if sorting_order not in SORTING_ORDERS:
            raise ValueError(f"sorting_order must be one of: {SORTING_ORDERS}")

    def get_bus_factor_repositories(self) -> list[dict]:
        return asyncio.run(self._get_repositories())

    async def _get_repositories(self) -> list[dict]:
        async with ClientSession(
            headers={"Authorization": f"token {GIT_TOKEN}"}
        ) as session:
            self._session = session

            tasks = []
            pages_number = self._pages
            for page_nr in range(1, pages_number + 1):
                per_page = (
                    MAX_PER_PAGE if page_nr < pages_number else self._last_page_nr
                )
                tasks.append(asyncio.create_task(self._process_page(per_page, page_nr)))

            return [
                info for results in await asyncio.gather(*tasks) for info in results
            ]

    async def _process_page(self, per_page, page_nr) -> list[dict]:
        url = os.path.join(API_URL, "search/repositories")
        params = {
            "q": f"language:{self._language}",
            "sort": self._sort,
            "order": self._sorting_order,
            "per_page": per_page,
            "page": page_nr,
        }

        resp = await self._make_request(url, params=params)
        data = await resp.json()

        repositories_data = data.get("items")
        return [
            repo
            for repo in await asyncio.gather(
                *[
                    asyncio.create_task(self._check_bus_factor(repository))
                    for repository in repositories_data
                ]
            )
            if repo is not None
        ]

    async def _check_bus_factor(self, repository: dict) -> dict | None:
        resp = await self._make_request(
            repository["contributors_url"], params={"per_page": 25}
        )
        contributors = await resp.json()

        contributions = [x["contributions"] for x in contributors]
        if (
            contributions
            and (percentage := round(contributions[0] / sum(contributions), 2))
            >= BUS_FACTOR_THRESHOLD
        ):
            return {
                "project": repository["name"],
                "user": contributors[0]["login"],
                "percentage": percentage,
            }
        return None

    async def _make_request(self, url: str, params: dict) -> ClientResponse:
        if self._session is None:
            raise Exception("Session not initialised, please ClientSession first")
        resp = await self._session.get(url, params=params)
        if 400 <= resp.status < 500:
            raise Exception(
                f'Wrong parameters, maybe there is no language such as: "{self._language}"?'
            )
        elif resp.status != 200:
            resp.raise_for_status()
        return resp

    @property
    def _pages(self) -> int:
        return self._project_count // MAX_PER_PAGE + int(
            bool(self._project_count % MAX_PER_PAGE)
        )

    @property
    def _last_page_nr(self) -> int:
        remainder = self._project_count % MAX_PER_PAGE
        return remainder if remainder != 0 else MAX_PER_PAGE
