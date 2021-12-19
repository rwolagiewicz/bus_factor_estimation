import pytest
import sys
import json

sys.path.append(".")

@pytest.fixture
def mocked_git_api(monkeypatch):
    """Use this fixture for mocking GitHub's REST API responses.
    Shortened responses saved in file: tests/resources/test_data.json
    """
    from bus_factor_estimator import BusFactorEstimator

    async def _mocked_make_request(*args, **kwargs):
        class MockResponse:
            def __init__(self, data, status):
                self._data = data
                self.status = status

            async def json(self):
                return self._data

        with open('tests/resources/test_data.json') as f:
            data = json.load(f)
            url = args[1]
            params = [str(x) for x in kwargs.get('params').values()]
            key = '&'.join([url, *params])
            resp_data = data.get(key)
            resp = MockResponse(resp_data, 200)
            return resp
    monkeypatch.setattr(BusFactorEstimator, '_make_request', _mocked_make_request)
