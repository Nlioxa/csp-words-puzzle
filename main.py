from csp import CSP
import cs_equation as sm
import constraints as cs


if __name__ == "__main__":
    #
    # equation to solve
    #
    # equation = "SEND + MORE = MONEY"
    # equation = "КУЩІ * 9 = ХАЩІ"
    equation = sm.EQUATIONS[17]

    #
    # setup problem
    #
    equation_cnstr = cs.EquationConstraint(equation)
    variables = equation_cnstr.variables
    words = equation_cnstr.words

    domains = {}
    for letter in variables:
        domain = [i for i in range(10)]
        # if any([letter == word[0] for word in words]):
            # domain.remove(0)
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
    solution = problem.solve()

    print(equation)
    if solution is None:
        print("No solution found!")
    else:
        answer = list(equation)
        for idx, letter in enumerate(answer):
            if letter in solution:
                answer[idx] = str(solution[letter])
        answer = "".join(answer)
        print(answer)
