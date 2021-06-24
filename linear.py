from ortools.linear_solver import pywraplp

#initialize a wrapper for solver
solver = pywraplp.Solver.CreateSolver('GLOP')


#adding variables
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

#finding number of variables
print(solver.NumVariables())


