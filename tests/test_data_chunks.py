import pytest

from bus_factor_estimator import BusFactorEstimator


@pytest.mark.asyncio
async def test_proces_page(mocked_git_api):
    data = await BusFactorEstimator("rust", 30)._process_page(30, 1)
    assert len(data) == 8


@pytest.mark.asyncio
async def test_check_bus_factor(mocked_git_api):
    result = await BusFactorEstimator("bash", 2)._check_bus_factor(
        {
            "name": "ohmyzsh",
            "contributors_url": "https://api.github.com/repos/ohmyzsh/ohmyzsh/contributors",
        }
    )
    assert result is None
