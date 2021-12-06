from typing import Dict, List
from csp import Constraint, Variable, Value

class UniqueConstraint(Constraint[str, int]):
    def __init__(self, variables: str) -> None:
        super().__init__(variables)

    def satisfied(self, assignment: Dict[Variable, Value]) -> bool:
        #
        # check for duplicates in the assignment
        #
        if len(set(assignment.values())) != len(assignment):
            return False
        #
        # no conflict
        #
        return True
