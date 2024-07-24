import pytest

from bus_factor_estimator import BusFactorEstimator


def test_wrong_project_count():
    with pytest.raises(ValueError):
        BusFactorEstimator("rust", 0)


def test_wrong_sorting_order():
    with pytest.raises(ValueError):
        BusFactorEstimator("python", 1, "up")


def test_missing_parameters():
    with pytest.raises(TypeError):
        BusFactorEstimator()
