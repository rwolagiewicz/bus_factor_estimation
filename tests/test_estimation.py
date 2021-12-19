import pytest
from bus_factor_estimator import BusFactorEstimator

@pytest.mark.parametrize("language, project_count, results", (
    ('rust', 30, [{'project': '996.ICU', 'user': '996icu', 'percentage': 0.8}, {'project': 'ripgrep', 'user': 'BurntSushi', 'percentage': 0.89}, {'project': 'swc', 'user': 'kdy1', 'percentage': 0.78}, {'project': 'Rocket', 'user': 'SergioBenitez', 'percentage': 0.86}, {'project': 'exa', 'user': 'ogham', 'percentage': 0.85}, {'project': 'rustdesk', 'user': 'rustdesk', 'percentage': 0.8}, {'project': 'appflowy', 'user': 'appflowy', 'percentage': 0.79}, {'project': 'sonic', 'user': 'valeriansaliou', 'percentage': 0.92}]),
))
def test_estimation(mocked_git_api, language, project_count, results):
    assert results == BusFactorEstimator(language, project_count).bus_factor_repositories()
