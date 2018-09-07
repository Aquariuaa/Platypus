from platypus import Problem, Real
from platypus.algorithms.bas import BAS
from math import sin, pi, cos, exp, sqrt


class gold(Problem):
    def __init__(self):
        super(gold, self).__init__(nvars=2, nobjs=1)
        self.types[:] = [Real(-2, 2), Real(-2, 2)]

    def evaluate(self, solution):
        vars = solution.variables[:]
        x1 = vars[0]
        x2 = vars[1]
        fact1a = (x1 + x2 + 1) ** 2
        fact1b = 19 - 14 * x1 + 3 * x1 ** 2 - 14 * x2 + 6 * x1 * x2 + 3 * x2 ** 2
        fact1 = 1 + fact1a * fact1b

        fact2a = (2 * x1 - 3 * x2) ** 2
        fact2b = 18 - 32 * x1 + 12 * x1 ** 2 + 48 * x2 - 36 * x1 * x2 + 27 * x2 ** 2
        fact2 = 30 + fact2a * fact2b
        solution.objectives[:] = [fact1 * fact2]


class mich(Problem):
    def __init__(self):
        super(mich, self).__init__(nvars=2, nobjs=1)
        self.types[:] = [Real(-6, -1), Real(0, 2)]

    def evaluate(self, solution):
        vars = solution.variables[:]
        x1 = vars[0]
        x2 = vars[1]
        y1 = -sin(x1) * ((sin((x1 ** 2) / pi)) ** 20)
        y2 = -sin(x2) * ((sin((2 * x2 ** 2) / pi)) ** 20)
        solution.objectives[:] = [y1 + y2]


class Ackley(Problem):
    def __init__(self):
        super(Ackley, self).__init__(nvars=2, nobjs=1)
        self.types[:] = [Real(-15, 30), Real(-15, 20)]

    def evaluate(self, solution):
        vars = solution.variables[:]
        n = 2
        a = 20
        b = 0.2
        c = 2 * pi
        s1 = 0
        s2 = 0
        for i in range(n):
            s1 = s1 + vars[i] ** 2
            s2 = s2 + cos(c * vars[i])
        y = -a * exp(-b * sqrt(1 / n * s1)) - exp(1 / n * s2) + a + exp(1)
        solution.objectives[:] = [y]


problem = gold()
problem2 = mich()
problem3 = Ackley()

for i in range(1):
    algorithm = BAS(problem, step=1, c=5)
    algorithm.run(100)

    print(algorithm.best)

    algorithm2 = BAS(problem2, step=5)
    algorithm2.run(1000)
    print(algorithm2.best)

    algorithm3 = BAS(problem3, step=30, c=0.1)
    algorithm3.run(300)
    print(algorithm3.best)
