import pytest

from bus_factor_estimator import BusFactorEstimator


@pytest.mark.asyncio
async def test_repositories_contributors_data(mocked_git_api):
    data = await BusFactorEstimator('rust', 30)._get_repositories_with_cotributors()
    assert len(data) == 30


@pytest.mark.asyncio
async def test_repositories_contributors_urls(mocked_git_api):
    repositories, urls = await BusFactorEstimator('bash', 2)._get_repositories_contributors_urls()
    assert repositories == ['ohmyzsh', 'realworld']
    assert urls == ['https://api.github.com/repos/ohmyzsh/ohmyzsh/contributors',
                    'https://api.github.com/repos/gothinkster/realworld/contributors']
