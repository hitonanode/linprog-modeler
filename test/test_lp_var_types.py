import pytest

from modeler import LPModel, LPStatus, LPVar, LPVarType


def test_semicontinuos() -> None:
    x = LPVar(
        "x",
        lower_bound=19,
        upper_bound=21,
        variable_type=LPVarType.SEMICONTINUOUS,
    )

    y = LPVar(
        "y",
        lower_bound=18,
        upper_bound=20,
        variable_type=LPVarType.SEMICONTINUOUS,
    )

    model = LPModel()

    model.add_constraint(x + y >= 10)
    model.add_constraint(x + y <= 30)

    model.set_objective(-x - y)

    model.solve()

    assert model.status == LPStatus.OPTIMAL

    assert x.value() == pytest.approx(21)
    assert y.value() == pytest.approx(0)


def test_semiinteger() -> None:
    x = LPVar(
        "x",
        lower_bound=19.5,
        upper_bound=21.5,
        variable_type=LPVarType.SEMIINTEGER,
    )

    y = LPVar(
        "y",
        lower_bound=18.5,
        upper_bound=20.5,
        variable_type=LPVarType.SEMIINTEGER,
    )

    model = LPModel()

    model.add_constraint(x + y >= 10)
    model.add_constraint(x + y <= 30)

    model.set_objective(-x - y)

    model.solve()

    assert model.status == LPStatus.OPTIMAL

    assert x.value() == pytest.approx(21)
    assert y.value() == pytest.approx(0)
