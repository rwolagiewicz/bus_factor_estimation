import pytest

from bus_factor_estimator import BusFactorEstimator


@pytest.mark.parametrize("language, project_count, results", (
    ('rust', 30, [{'project': '996.ICU', 'user': '996icu', 'percentage': 0.8}, {'project': 'ripgrep', 'user': 'BurntSushi', 'percentage': 0.89}, {'project': 'swc', 'user': 'kdy1', 'percentage': 0.78}, {'project': 'Rocket', 'user': 'SergioBenitez', 'percentage': 0.86}, {'project': 'exa', 'user': 'ogham', 'percentage': 0.85}, {'project': 'rustdesk', 'user': 'rustdesk', 'percentage': 0.8}, {'project': 'appflowy', 'user': 'appflowy', 'percentage': 0.79}, {'project': 'sonic', 'user': 'valeriansaliou', 'percentage': 0.92}]),
    ('haskell', 20, [{'project': 'shellcheck', 'user': 'koalaman', 'percentage': 0.83}, {'project': 'pandoc', 'user': 'jgm', 'percentage': 0.84}]),
    ('cobol', 5, [{'project': 'node-cobol', 'user': 'IonicaBizau', 'percentage': 0.9}, {'project': 'cobweb', 'user': 'xtuc', 'percentage': 1.0}]),
    ('python', 10, [{'project': 'awesome-python', 'user': 'vinta', 'percentage': 0.87}, {'project': 'httpie', 'user': 'jakubroztocil', 'percentage': 0.84}, {'project': 'you-get', 'user': 'soimort', 'percentage': 0.75}]),
    ('golang', 10, [{'project': 'frp', 'user': 'fatedier', 'percentage': 0.88}, {'project': 'fzf', 'user': 'junegunn', 'percentage': 0.93}]),
))
def test_estimation(mocked_git_api, language, project_count, results):
    assert results == BusFactorEstimator(language, project_count).bus_factor_repositories()
