import argparse
from csp import CSP
import cs_equation as cseq
import constraints as cs


def required_range(rmin, rmax):
    class RequiredRange(argparse.Action):
        def __call__(self, parser, args, value, option_string=None):
            if not rmin <= value <= rmax:
                msg = (
                    f"argument {self.dest} must be in range ({rmin}, {rmax})"
                )
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, value)

    return RequiredRange


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-v",
        "--variant",
        help="equation id from the course task",
        required=False,
        type=int,
        action=required_range(0, len(cseq.EQUATIONS))
    )
    ap.add_argument(
        "-e",
        "--equation",
        help="equation for the problem",
        type=str,
        default="",
        required=False
    )
    ap.add_argument(
        "-z",
        "--zfirst",
        help="enables zero '0' as the first digit of numbers",
        action='store_true'
    )
    args = vars(ap.parse_args())

    #
    # equation to solve
    #
    if args['variant']:
        v = args['variant']
        equation = cseq.EQUATIONS[v]
    elif args['equation']:
        equation = args['equation']
    else:
        equation = "SEND + MORE = MONEY"

    print(f'Equation to solve:\n> "{equation}"')
    #
    # setup problem
    #
    equation_cnstr = cs.EquationConstraint(equation)
    variables = equation_cnstr.variables
    words = equation_cnstr.words

    domains = {}
    for letter in variables:
        domain = [i for i in range(10)]
        if args['zfirst'] == False \
        and any([letter == word[0] for word in words]):
            domain.remove(0)
        try:
            domain = [int(letter)]
        except ValueError:
            pass

        domains[letter] = domain

    problem = CSP(variables, domains)
    problem.add_constraint(equation_cnstr)
    problem.add_constraint(cs.UniqueConstraint(variables))

    #
    # find and display solution if exists
    #
    print('Solving...')
    solution = problem.solve()

    if solution is None:
        print("No solution found!")
    else:
        answer = list(equation)
        for idx, letter in enumerate(answer):
            if letter in solution:
                answer[idx] = str(solution[letter])
        answer = "".join(answer)
        print(f'Found a solution:\n> "{equation}"\n< "{answer}"')
