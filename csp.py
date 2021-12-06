from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar


Variable = TypeVar("Variable")
Value    = TypeVar("Value")


class Constraint(Generic[Variable, Value], ABC):
    def __init__(self, variables: List[Variable]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[Variable, Value]) -> bool:
        pass


class CSP(Generic[Variable, Value]):
    """
    A constraint satisfaction problem consists of variables of type 'Variable'
    that have ranges of values known as domains of type 'Domain' and constraints
    that determine whether a particular variable's domain selection is valid
    """

    def __init__(
        self, variables: List[Variable], domains: Dict[Variable, List[Value]]
    ) -> None:
        self.variables: List[Variable] = variables
        self.domains: Dict[Variable, List[Value]] = domains
        self.constraints: Dict[Variable, List[Constraint[Variable, Value]]] = {}
        #
        # every variable must have some domain
        #
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[Variable, Value]) -> None:
        """
        add a constraint to every variable
        """
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: Variable, assignment: Dict[Variable, Value]) -> bool:
        """
        check if all variables satisfy their constraints
        """
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(
        self, assignment: Dict[Variable, Value] = {}
    ) -> Optional[Dict[Variable, Value]]:
        """
        looks recursively for any satisfactory assignment 
        and returns one if it exists
        """
        #
        # assignment is complete if every variable is assigned
        #
        if len(assignment) == len(self.variables):
            return assignment
        #
        # gets all veriables in the CSP with no assignment
        #
        unassigned: List[Variable] = [
            var for var in self.variables if var not in assignment
        ]
        #
        # for the first unassigned variable tries to make an assignment 
        # from its domain
        #
        first: Variable = unassigned[0]
        for value in self.domains[first]:
            some_assignment = assignment.copy()
            some_assignment[first] = value

            if self.consistent(first, some_assignment):
                result: Optional[Dict[Variable, Value]] = self.backtracking_search(
                    some_assignment
                )

                if result is not None:
                    return result

        return None

    def solve(self) -> Optional[Dict[str, int]]:
        return self.backtracking_search()