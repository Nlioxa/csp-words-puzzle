from typing import Dict, List
from csp import Constraint, Variable, Value
from re import findall
import operator as op


EQUATIONS = (
    "SEND + MORE = MONEY",
    "КОКА + КОЛА = ВОДА",
    "SATURN + URANUS = PLANETS",
    "ВАГ0Н + ВАГ0Н = П0ТЯГ",
    "КНИГА + КНИГА + КНИГА = НАУКА",
    "FORTY + TEN + TEN = SIXTY",
    "SEVEN + SEVEN + SIX = TWENTY",
    "BASE + BALL = GAMES",
    "WWW + DOWN = ERROR",
    "СТРАВА + СТРАВА = ВЕЧЕРЯ",
    "АТАКА + УДАР + УДАР = НОКАУТ",
    "КОЗА + КОЗА + КОЗА = СТАДО",
    "БАЛЕТ + БАЛЕТ = ТЕАТР",
    "BLACK + GREEN = ORANGE",
    "ДВА * ДВА = ЧОТИРИ",
    "ДОШКА * 5 = ЧОВЕН",
    "ПРАВДА * ? = ІСТИНА",
    "КУЩІ * 9 = ХАЩІ",
    "РІЧКА * 6 = ОЗЕРО",
    "EAT + THAT = APPLE",
)


"""
map operators to functions
"""
OPERATORS = {
    "*": op.mul,
    "/": op.truediv,
    "+": op.add,
    "-": op.sub,
    "=": op.eq,
    "**": op.pow,
}

""" 
precedence from left to right. 
operators at same index have same precendece.
"""
PRECEDENCE_LEVELS = (
    {"**"},
    {"*", "/"},
    {"+", "-"},
    {"="},
)


class EquationConstraint(Constraint[str, int]):
    def __init__(self, equation: str) -> None:
        self.words = findall("[^\+\-\*\/\= ]+", equation)
        self.operators = findall("[\+\-\*\/\=]+", equation)
        self.variables = set("".join(self.words))
        super().__init__(self.variables)

    def __substitute(self, assignment: Dict[str, int]):
        words = self.words.copy()
        for wi, word in enumerate(words):
            word = list(word)
            for ci, chr in enumerate(word):
                word[ci] = str(assignment[chr])
            words[wi] = "".join(word)
        return words

    def __evaluate(self, numbers: List[str]):
        operators = self.operators.copy()
        for level in PRECEDENCE_LEVELS:
            #
            # Operator with this precedence level exists
            #
            while any(operator in operators for operator in level):
                #
                # next operator with this precedence
                #
                idx, opr = next(
                    (i, opr) for i, opr in enumerate(operators) if opr in level
                )
                #
                # remove this operator from the operator list
                #
                operators.pop(idx)
                #
                # convert operands into floating point numbers
                #
                values = map(float, numbers[idx : idx + 2])
                #
                # calculate operator on two numbers
                #
                value = OPERATORS[opr](*values)
                #
                # update operands list
                #
                numbers[idx : idx + 2] = [value]

        return numbers[0] if len(numbers) > 0 else None

    def satisfied(self, assignment: Dict[Variable, Value]) -> bool:
        #
        # all variables uniqly assigned -> evaluate equation
        #
        if len(assignment) == len(self.variables):
            return self.__evaluate(numbers=self.__substitute(assignment))
        #
        # no conflict
        #
        return True
