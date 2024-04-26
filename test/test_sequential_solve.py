from typing import cast

import pytest

from lpmodeler.model import LPModel, LPStatus, LPVar


def test_sequential_solve() -> None:
    x = LPVar("x", lower_bound=0)

    model = LPModel()

    model.set_objective(x)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert x.value() == pytest.approx(0.0)
    assert model.objective.value() == pytest.approx(0.0)

    model.add_constraint(x >= 1)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert x.value() == pytest.approx(1.0)
    assert model.objective.value() == pytest.approx(1.0)


def test_sequential_solve_no_solution() -> None:
    x = LPVar("x", lower_bound=0)

    model = LPModel()

    model.set_objective(x)

    model.solve()

    assert model.status == LPStatus.OPTIMAL
    assert x.value() == pytest.approx(0.0)
    assert model.objective.value() == pytest.approx(0.0)

    model.add_constraint(x <= -1)

    model.solve()

    status2 = cast(LPStatus, model.status)
    assert status2 == LPStatus.INFEASIBLE
    assert x.value() is None
    assert model.objective.value() is None
