import pytest

from modeler import LPModel, LPStatus, LPVar, LPVarType


def test_lpvar_objective() -> None:
    x = LPVar("x", variable_type=LPVarType.INTEGER)

    model = LPModel()

    model.add_constraint(x >= -10.5)

    model.set_objective(x)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert x.value() == pytest.approx(-10)


def test_float_objective() -> None:
    x = LPVar("x")

    model = LPModel()

    model.add_constraint(x >= -10.5)

    model.set_objective(1.0)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert isinstance(model.objective.value(), float)


def test_no_constraints() -> None:
    x = LPVar("x")

    model = LPModel()

    model.set_objective(x)

    model.solve()

    assert model.status == LPStatus.UNBOUNDED
    assert x.value() is None


def test_no_objective() -> None:
    x = LPVar("x")

    model = LPModel()
    model.add_constraint(x >= 0)
    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert isinstance(x.value(), float)


def test_no_constraints_float_objective() -> None:
    model = LPModel()

    model.set_objective(1.0)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert model.objective.value() == pytest.approx(1.0)


def test_no_constraint_no_objective() -> None:
    model = LPModel()

    model.solve()

    assert model.status == LPStatus.OPTIMAL
