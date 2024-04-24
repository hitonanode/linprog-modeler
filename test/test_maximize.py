import pytest

from lpmodeler.model import LPModel, LPSense, LPStatus, LPVar


def test_maximize() -> None:
    x = LPVar("x", lower_bound=1, upper_bound=2)

    model = LPModel(sense=LPSense.MAXIMIZE)

    model.set_objective(x + 1.0)

    model.solve()

    assert model.status == LPStatus.OPTIMAL

    assert x.value() == pytest.approx(2.0)
    assert model.objective.value() == pytest.approx(3.0)


def test_maximize_const_no_variable() -> None:
    model = LPModel(sense=LPSense.MAXIMIZE)

    model.set_objective(-2.0)

    model.solve()

    assert model.status == LPStatus.OPTIMAL

    assert model.objective.value() == pytest.approx(-2.0)
