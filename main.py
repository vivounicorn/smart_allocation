"""Simple solve."""
from basic.bipartite_graph import BipartiteGraph
from basic.customer import Customer
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


def tt():
    """Showcases assumptions."""
    # Creates the model.
    # [START model]
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    # [END model]

    # Creates the variables.
    # [START variables]
    x = model.NewIntVar(0, 10, 'x')
    y = model.NewIntVar(0, 10, 'y')
    z = model.NewIntVar(0, 10, 'z')
    a = model.NewBoolVar('a')
    b = model.NewBoolVar('b')
    c = model.NewBoolVar('c')
    d = model.NewBoolVar('d')
    # [END variables]

    # Creates the constraints.
    # [START constraints]
    model.Add(x > y).OnlyEnforceIf(a)
    model.Add(y > z).OnlyEnforceIf(b)
    model.Add(z > x).OnlyEnforceIf(c)
    model.Add(x + y > z).OnlyEnforceIf(d)
    # [END constraints]

    # Add assumptions
    model.AddAssumptions([d, a, b, c])
    print(a.Index(), ',', b.Index(), ',', c.Index(), ',', d.Index())

    # Creates a solver and solves.
    # [START solve]
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # [END solve]

    # Print solution.
    # [START print_solution]
    print(f'Status = {solver.StatusName(status)}')
    if status == cp_model.INFEASIBLE:
        print('SufficientAssumptionsForInfeasibility = '
              f'{solver.SufficientAssumptionsForInfeasibility()}')
    # [END print_solution]


def build_one_customer(cp: CpModelOptimizer):
    funds = '200, 300'
    cus = Customer(200, 86000, 36, 0, 0, 0.1288, 0.0121, 0.85, 485, 0.15, 0)
    [cus.funders.append(cp.funders_struct_map[f.strip()]) for f in funds.split(',')]
    return cus


if __name__ == "__main__":

    cfg = ConfigTools(path='./')

    cp_model = CpModelOptimizer(cfg)
    cp_model.build_problem()

    customer = build_one_customer(cp_model)

    cp_model.bp.add_customer(customer)
    cp_model.build_problem()

    cp_model.bp.remove_customer(customer.id)
    cp_model.build_problem()
