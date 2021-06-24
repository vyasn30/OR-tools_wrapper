from ortools.linear_solver import pywraplp

#initialize a wrapper for solver
solver = pywraplp.Solver.CreateSolver('GLOP')


#adding variables
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

#finding number of variables
print(solver.NumVariables())

#solver.Add for adding constraints

solver.Add(x + 2 * y <= 14.0)
solver.Add(3 * x -  y >=0.0)
solver.Add(x - y <= 2.0)

#objective fuction is the function that we need to optimize

solver.Maximize(3 * x + 4 * y)

status =  solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
else:
        print('The problem does not have an optimal solution.')

status = solver.Solve()
