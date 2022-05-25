"""Simple solve."""

from optimizer.optimization import CpModelOptimizer
from tools.config_tools import ConfigTools


"""Simple Constraint optimization example."""

from ortools.constraint_solver import pywrapcp


def SimpleSatProgram():
    """Entry point of the program."""
    # Instantiate the solver.
    solver = pywrapcp.Solver('CPSimple')

    # Create the variables.
    num_vals = 3
    x = solver.IntVar(0, num_vals - 1, 'x')
    y = solver.IntVar(0, num_vals - 1, 'y')
    z = solver.IntVar(0, num_vals - 1, 'z')

    # Constraint 0: x != y.
    solver.Add(x != y)
    print('Number of constraints: ', solver.Constraints())

    # Solve the problem.
    decision_builder = solver.Phase([x, y, z], solver.CHOOSE_FIRST_UNBOUND,
                                    solver.ASSIGN_MIN_VALUE)

    # Print solution on console.
    count = 0
    solver.NewSearch(decision_builder)
    while solver.NextSolution():
        count += 1
        solution = 'Solution {}:\n'.format(count)
        for var in [x, y, z]:
            solution += ' {} = {}'.format(var.Name(), var.Value())
        print(solution)
    solver.EndSearch()
    print('Number of solutions found: ', count)

    print('Advanced usage:')
    print('Problem solved in ', solver.WallTime(), 'ms')
    print('Memory usage: ', pywrapcp.Solver.MemoryUsage(), 'bytes')


if __name__ == "__main__":
    # SimpleSatProgram()

    cfg = ConfigTools(path='/Users/liyiran/Gitlab/smart_allocation')

    cp_model = CpModelOptimizer(cfg)
    cp_model.build_problem()
