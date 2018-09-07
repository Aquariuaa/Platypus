from abc import abstractmethod

import numpy as np

from ..core import Algorithm, ParetoDominance, Solution, PlatypusError
from ..operators import RandomGenerator


class AbstractBeetleAntennaeSearchAlgorithm(Algorithm):
    def __init__(self, problem,
                 population_size=1,
                 generator=RandomGenerator(),
                 comparator=ParetoDominance(),
                 **kwargs):
        super(AbstractBeetleAntennaeSearchAlgorithm, self).__init__(problem, **kwargs)
        self.population_size = population_size
        self.generator = generator
        self.comparator = comparator
        self.result = []

    def step(self):
        if self.nfe == 0:
            self.initialize()
            self.result = self.population
        else:
            self.iterate()
            self.result = self.population

    def initialize(self):
        self.population = [self.generator.generate(self.problem) for _ in range(self.population_size)]
        self.evaluate_all(self.population)

    @abstractmethod
    def iterate(self):
        raise NotImplementedError("method not implemented")


class BAS(AbstractBeetleAntennaeSearchAlgorithm):


    def __init__(self, problem,
                 eta=0.95, c=5,
                 eps=1e-8, step=1,
                 **kwargs):

        super(BAS, self).__init__(problem, **kwargs)
        self.offspring_size = 1
        self.eta = eta
        self.c = c
        self.eps = eps
        self.step1 = step

        if problem.nobjs != 1:
            raise PlatypusError("can not instantiate single objective algorithm "
                                "on problem with %d objectives" % problem.nobjs)

    def initialize(self):
        super(BAS, self).initialize()

        self.best = self.population[0]
        self.evaluate_all([self.best])
        # print(self.population[0].variables)

    def iterate(self):
        def handle_bound(vars):
            tmp = vars
            for i in range(self.problem.nvars):
                bound = self.problem.types[i]
                if tmp[i] > bound.max_value:
                    tmp[i] = bound.max_value
                elif tmp[i] < bound.min_value:
                    tmp[i] = bound.min_value
            return tmp

        d0 = self.step1 / self.c
        dirs = np.random.uniform(-1, 1,self.problem.nvars)
        dirs = dirs / (np.linalg.norm(dirs)+self.eps)

        # variation= d0 * dirs / 2
        x_left = Solution(self.problem)
        x_left.variables = self.best.variables
        x_left.variables = handle_bound(x_left.variables[:] + d0 * dirs/2)
        x_right = Solution(self.problem)
        x_right.variables = self.best.variables
        x_right.variables = handle_bound(x_right.variables[:] - d0 * dirs/2)
        self.evaluate_all([x_left,x_right])
        self.nfe-=2
        # print(offspring[0].objectives, offspring[1].objectives)


        xt = self.best.variables - self.step1 * dirs * np.sign(
            x_left.objectives[0] - x_right.objectives[0])
        xtnew = Solution(self.problem)
        xtnew.variables = handle_bound(xt)
        self.evaluate_all([xtnew])
        if xtnew.objectives[0]<self.best.objectives[0]:
            self.best=xtnew
        # print('Iteration = {:4d} \tBest={}'.format(self.nfe, x_left,x_right,self.step1, self.best))
        # update step
        self.step1 = self.eta * self.step1
#
# class BSAS(AbstractBeetleAntennaeSearchAlgorithm):
#
#     def __init__(self, problem,
#                  eta=0.95, c=5,
#                  eps=1e-8, step=1,
#                  **kwargs):
#         super(BSAS, self).__init__(problem, **kwargs)
#         self.offspring_size = 1
#         self.eta = eta
#         self.c = c
#         self.eps = eps
#         self.step1 = step
#
#         if problem.nobjs != 1:
#             raise PlatypusError("can not instantiate single objective algorithm "
#                                 "on problem with %d objectives" % problem.nobjs)
#
#     def initialize(self):
#         super(BSAS, self).initialize()
#
#         self.best = self.population[0]
#         self.evaluate_all([self.best])
#         print(self.population[0].variables)
#
#     def iterate(self):
#         def handle_bound(vars):
#             tmp = vars
#             for i in range(self.problem.nvars):
#                 bound = self.problem.types[i]
#                 if tmp[i] > bound.max_value:
#                     tmp[i] = bound.max_value
#                 elif tmp[i] < bound.min_value:
#                     tmp[i] = bound.min_value
#             return tmp
#
#         d0 = self.step1 / self.c
#         dirs = np.random.uniform(-1, 1,self.problem.nvars)
#         dirs = dirs / (np.linalg.norm(dirs)+self.eps)
#
#         variation= d0 * dirs / 2
#         x_left = Solution(self.problem)
#         x_left.variables = self.best.variables
#         x_left.variables = handle_bound(x_left.variables[:] + d0 * dirs/2)
#         x_right = Solution(self.problem)
#         x_right.variables = self.best.variables
#         x_right.variables = handle_bound(x_right.variables[:] - d0 * dirs/2)
#         self.evaluate_all([x_left,x_right])
#         # print(offspring[0].objectives, offspring[1].objectives)
#
#
#         xt = self.best.variables - self.step1 * dirs * np.sign(
#             x_left.objectives[0] - x_right.objectives[0])
#         xtnew = Solution(self.problem)
#         xtnew.variables = handle_bound(xt)
#         self.evaluate_all([xtnew])
#         if xtnew.objectives[0]<self.best.objectives[0]:
#             self.best=xtnew
#         print('Iteration = {:4d} \tBest={}'.format(self.nfe, x_left,x_right,self.step1, self.best))
#         # update step
#         self.step1 = self.eta * self.step1
#
# class BAS_WPT(AbstractBeetleAntennaeSearchAlgorithm):
#
#     def __init__(self, problem,
#                  eta=0.95, c=5,
#                  eps=1e-8, step=1,
#                  **kwargs):
#         super(BAS_WPT, self).__init__(problem, **kwargs)
#         self.offspring_size = 1
#         self.eta = eta
#         self.c = c
#         self.eps = eps
#         self.step1 = step
#
#         if problem.nobjs != 1:
#             raise PlatypusError("can not instantiate single objective algorithm "
#                                 "on problem with %d objectives" % problem.nobjs)
#
#     def initialize(self):
#         super(BAS_WPT, self).initialize()
#
#         self.best = self.population[0]
#         self.evaluate_all([self.best])
#         print(self.population[0].variables)
#
#     def iterate(self):
#         def handle_bound(vars):
#             tmp = vars
#             for i in range(self.problem.nvars):
#                 bound = self.problem.types[i]
#                 if tmp[i] > bound.max_value:
#                     tmp[i] = bound.max_value
#                 elif tmp[i] < bound.min_value:
#                     tmp[i] = bound.min_value
#             return tmp
#
#         d0 = self.step1 / self.c
#         dirs = np.random.uniform(-1, 1,self.problem.nvars)
#         dirs = dirs / (np.linalg.norm(dirs)+self.eps)
#
#         variation= d0 * dirs / 2
#         x_left = Solution(self.problem)
#         x_left.variables = self.best.variables
#         x_left.variables = handle_bound(x_left.variables[:] + d0 * dirs/2)
#         x_right = Solution(self.problem)
#         x_right.variables = self.best.variables
#         x_right.variables = handle_bound(x_right.variables[:] - d0 * dirs/2)
#         self.evaluate_all([x_left,x_right])
#         # print(offspring[0].objectives, offspring[1].objectives)
#
#
#         xt = self.best.variables - self.step1 * dirs * np.sign(
#             x_left.objectives[0] - x_right.objectives[0])
#         xtnew = Solution(self.problem)
#         xtnew.variables = handle_bound(xt)
#         self.evaluate_all([xtnew])
#         if xtnew.objectives[0]<self.best.objectives[0]:
#             self.best=xtnew
#         print('Iteration = {:4d} \tBest={}'.format(self.nfe, x_left,x_right,self.step1, self.best))
#         # update step
#         self.step1 = self.eta * self.step1