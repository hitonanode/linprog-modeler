from enum import Enum
from typing import SupportsFloat

from scipy.optimize import linprog  # type: ignore


class LPVarType(Enum):
    CONTINUOUS = 1
    INTEGER = 2


class _LPBase:
    def __add__(self, other: "LPExpressionLike") -> "LPExpression":
        return LPExpression.build(self) + other

    def __radd__(self, other: "LPExpressionLike") -> "LPExpression":
        return other + LPExpression.build(self)

    def __sub__(self, other: "LPExpressionLike") -> "LPExpression":
        return LPExpression.build(self) - other

    def __rsub__(self, other: "LPExpressionLike") -> "LPExpression":
        return other - LPExpression.build(self)

    def __mul__(self, other: SupportsFloat) -> "LPExpression":
        return LPExpression.build(self) * other

    def __rmul__(self, other: SupportsFloat) -> "LPExpression":
        return LPExpression.build(self) * other

    def __truediv__(self, other: SupportsFloat) -> "LPExpression":
        return LPExpression.build(self) / other

    def __neg__(self) -> "LPExpression":
        return -LPExpression.build(self)

    def __le__(
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(
            lhs=LPExpression.build(self),
            rhs=other,
            inequality_type=LPInequalityType.LESSEQ,
        )

    def __ge__(
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(
            lhs=other,
            rhs=LPExpression.build(self),
            inequality_type=LPInequalityType.LESSEQ,
        )

    def __eq__(  # type: ignore
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(
            lhs=LPExpression.build(self),
            rhs=other,
            inequality_type=LPInequalityType.EQUAL,
        )


class LPVar(_LPBase):
    def __init__(
        self,
        name: str,
        lower_bound: float | None = None,
        upper_bound: float | None = None,
        variable_type: LPVarType = LPVarType.CONTINUOUS,
    ) -> None:
        self.name = name
        self.lower_bound: float | None = lower_bound
        self.upper_bound: float | None = upper_bound
        self.variable_type: LPVarType = variable_type
        self._value: float | None = None

    def __str__(self) -> str:
        s = "{}(lb={}, ub={}, type={})".format(
            self.name,
            self.lower_bound,
            self.upper_bound,
            self.variable_type.name,
        )
        if self._value is not None:
            s += ": {}".format(self._value)
        return s

    def __repr__(self) -> str:
        return str(self)

    def value(self) -> float | None:
        return self._value


class LPInequalityType(Enum):
    LESSEQ = 1  # lhs <= rhs
    EQUAL = 2  # lhs == rhs


class _LPTerm(_LPBase):
    """
    A term of the form coefficient * variable.
    """

    def __init__(self, coefficient: float, variable: LPVar) -> None:
        self.coefficient: float = coefficient
        self.variable: LPVar = variable


class LPExpression:
    def __init__(
        self,
        const: SupportsFloat,
        terms: list[_LPTerm],
    ) -> None:
        self.const = float(const)
        self.terms = terms.copy()
        self._value: float | None = None

    @classmethod
    def build(self, x: "LPExpressionLike | _LPBase") -> "LPExpression":
        if isinstance(x, LPExpression):
            return LPExpression(x.const, x.terms)
        elif isinstance(x, _LPTerm):
            return LPExpression(0, [x])
        elif isinstance(x, LPVar):
            return LPExpression(0, [_LPTerm(1.0, x)])
        elif isinstance(x, SupportsFloat):
            return LPExpression(x, [])
        else:
            raise TypeError("Invalid type for LPExpression")

    def __add__(self, other: "LPExpressionLike") -> "LPExpression":
        rhs = LPExpression.build(other)
        return LPExpression(
            self.const + rhs.const,
            self.terms + rhs.terms,
        )

    def __radd__(self, other: "LPExpressionLike") -> "LPExpression":
        return self + other

    def __sub__(self, other: "LPExpressionLike") -> "LPExpression":
        rhs = LPExpression.build(other)
        return self + (-rhs)

    def __rsub__(self, other: "LPExpressionLike") -> "LPExpression":
        return LPExpression.build(other) + (-self)

    def __mul__(self, other: SupportsFloat) -> "LPExpression":
        return LPExpression(
            self.const * float(other),
            [
                _LPTerm(
                    t.coefficient * float(other),
                    t.variable,
                )
                for t in self.terms
            ],
        )

    def __rmul__(self, other: SupportsFloat) -> "LPExpression":
        return self * other

    def __truediv__(self, other: SupportsFloat) -> "LPExpression":
        return LPExpression(
            self.const / float(other),
            [
                _LPTerm(
                    t.coefficient / float(other),
                    t.variable,
                )
                for t in self.terms
            ],
        )

    def __neg__(self) -> "LPExpression":
        return LPExpression(
            -self.const,
            [_LPTerm(-t.coefficient, t.variable) for t in self.terms],
        )

    def __le__(
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(self, other, LPInequalityType.LESSEQ)

    def __ge__(
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(other, self, LPInequalityType.LESSEQ)

    def __eq__(  # type: ignore
        self,
        other: "LPExpressionLike",
    ) -> "LPInequality":
        return LPInequality(self, other, LPInequalityType.EQUAL)

    def __str__(self) -> str:
        ret = ["{}".format(self.const)]

        for t in self.terms:
            sgn = "+" if t.coefficient >= 0 else ""
            ret.append("{}{}{}".format(sgn, t.coefficient, t.variable.name))

        return " ".join(ret)

    def value(self) -> float | None:
        return self._value


LPExpressionLike = LPExpression | _LPTerm | LPVar | SupportsFloat


class LPInequality:
    def __init__(
        self,
        lhs: LPExpressionLike,
        rhs: LPExpressionLike,
        inequality_type: LPInequalityType,
    ) -> None:
        """
        lhs <= rhs
        -> terms + const (<= or ==) 0
        """

        self.lhs = LPExpression.build(lhs) - LPExpression.build(rhs)
        self.inequality_type = inequality_type

    def __str__(self) -> str:
        if self.inequality_type == LPInequalityType.LESSEQ:
            return "{} <= 0".format(self.lhs)
        elif self.inequality_type == LPInequalityType.EQUAL:
            return "{} == 0".format(self.lhs)
        else:
            raise ValueError("Invalid inequality type")

    def __repr__(self) -> str:
        return str(self)


class LPModel:
    def __init__(self) -> None:
        self.constraints: list[LPInequality] = []
        self.objective: LPExpression = LPExpression(0, [])

    def add_constraint(self, constraint: LPInequality) -> None:
        self.constraints.append(constraint)

    def set_objective(self, objective: LPExpressionLike) -> None:
        self.objective = LPExpression.build(objective)

    def solve(self) -> None:
        var_dict: dict[int, LPVar] = {}
        for constraint in self.constraints:
            for term in constraint.lhs.terms:
                var_dict.setdefault(id(term.variable), term.variable)

        for term in self.objective.terms:
            var_dict.setdefault(id(term.variable), term.variable)

        id_to_idx = {id(v): i for i, v in enumerate(var_dict.values())}

        A_ub: list[list[float]] = []
        b_ub: list[float] = []
        A_eq: list[list[float]] = []
        b_eq: list[float] = []

        for constraint in self.constraints:
            lhs: list[float] = [0.0] * len(var_dict)
            rhs = -constraint.lhs.const

            for term in constraint.lhs.terms:
                lhs[id_to_idx[id(term.variable)]] += term.coefficient

            if constraint.inequality_type == LPInequalityType.LESSEQ:
                A_ub.append(lhs)
                b_ub.append(rhs)
            elif constraint.inequality_type == LPInequalityType.EQUAL:
                A_eq.append(lhs)
                b_eq.append(rhs)
            else:
                raise ValueError("Invalid inequality type")

        bounds = [(v.lower_bound, v.upper_bound) for v in var_dict.values()]

        integrality = [
            int(variable.variable_type == LPVarType.INTEGER)
            for variable in var_dict.values()
        ]

        c: list[float] = [0.0] * len(var_dict)
        for term in self.objective.terms:
            c[id_to_idx[id(term.variable)]] += term.coefficient

        res = linprog(
            c,
            A_ub=A_ub or None,
            b_ub=b_ub or None,
            A_eq=A_eq or None,
            b_eq=b_eq or None,
            bounds=bounds,
            integrality=integrality,
        )

        if res.status == 0:
            for i, variable in enumerate(var_dict.values()):
                variable._value = res.x[i]

            self.objective._value = res.fun + self.objective.const
