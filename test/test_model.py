from modeler import LPModel, LPVar


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
