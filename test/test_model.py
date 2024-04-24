import pytest

from modeler import LPModel, LPStatus, LPVar


def test_simple_lp() -> None:
    x = LPVar("x")
    y = LPVar("y")

    model = LPModel()

    model.add_constraint(x + y <= 10)
    model.add_constraint(x + 2 * y <= 10)
    model.add_constraint(x * 2 + y <= 10)
    model.add_constraint(-x <= 2)

    model.set_objective(-x - y * 1.3)

    model.solve()


def test_simple_lp_nonnegative() -> None:
    x = LPVar("x", lower_bound=0.0)
    y = LPVar("y", lower_bound=0.0)

    model = LPModel()

    model.add_constraint(x + 2 * y <= 10)
    model.add_constraint(x * 2 + y <= 10)

    model.set_objective(x + y)

    model.solve()


def test_identity_constraint_feasible() -> None:
    x = LPVar("x")

    model = LPModel()

    model.add_constraint(x <= 9.7)
    model.add_constraint(3 <= 5)

    model.set_objective(-x)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert x.value() == pytest.approx(9.7)


def test_identity_constraint_infeasible() -> None:
    x = LPVar("x")

    model = LPModel()

    model.add_constraint(6 <= 5)

    model.set_objective(x)

    model.solve()

    assert model.status == LPStatus.INFEASIBLE
    assert x.value() is None
