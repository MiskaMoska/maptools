import random
import numpy as np
from typing import Any, TypeVar, Generic, Callable
from maptools.nlrt.encoding import LayoutPatternCode, RoutingPatternCode
from abc import ABCMeta, abstractmethod
from copy import deepcopy, copy

_Solution = TypeVar('_Solution')

class BaseSimulatedAnnealing(Generic[_Solution], Callable, metaclass=ABCMeta):

    def __init__(
        self, 
        func: Callable[[_Solution], float], 
        x0: _Solution, 
        T_max: float = 100,
        T_min: float = 1e-7, 
        L: int = 300, 
        max_stay_counter: int = 150,
        silent: bool = False,
        **kwargs
    ) -> None:
        '''
        Base Class for Simulated Annealing Algorithm.
        This class is borrowed from the version of scikit-opt
        https://github.com/guofei9987/scikit-opt/blob/master/sko/SA.py
        with some application-specific modifications.
        
        Parameters
        ----------
        func: Callable[[_Solution], float]
            the objective function to be optimized.
            this function must have a scalar-value output
            and the goal is to minimize (not maximize) the function output.
            
        x0: _Solution
            initial solution, must be the same type with the input of `func`.

        T_max: float
            maximum or initial temperature.

        T_min: float
            minimum or final temperature.

        L: int
            number of iterations under every temperature.

        max_stay_counter: int
            invariance counter threshold.

        silent: bool
            whether to run without logging to the terminal.

        dummy_sa: bool
            never accept worse solutions. 
        '''
        super().__init__()

        self.func = func
        assert T_max > T_min > 0, 'T_max > T_min > 0'
        self.T_max = T_max # initial temperature
        self.T_min = T_min # end temperature
        self.L = int(L) # num of iteration under every temperature（also called Long of Chain

        self.dummy_sa = False
        self.__dict__.update(kwargs)
        
        # stop if best_y stay unchanged over max_stay_counter times (also called cooldown time)
        self.max_stay_counter = max_stay_counter
        self.best_x = x0
        self.silent = silent

        self.best_y = self.func(self.best_x)
        self.T = self.T_max
        self.iter_cycle = 0
        self.generation_best_Y = [self.best_y]

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=1e-30) -> bool:
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    @abstractmethod
    def update(self, x: _Solution) -> None: ...

    @abstractmethod
    def undo_update(self, x: _Solution) -> None: ...

    @abstractmethod
    def cool_down(self) -> None: ...

    def __call__(self) -> _Solution:
        return self.run()

    def run(self) -> _Solution:
        x_current, y_current = self.best_x, self.best_y
        stay_counter = 0

        while True:
            accept_probs = []
            for i in range(self.L):
                self.update(x_current)
                y_new = self.func(x_current)
                df = y_new - y_current

                if (not self.dummy_sa) and df > 0: # get a worse
                    accept_prob = np.exp(-df / self.T)
                    accept_probs.append(accept_prob)

                if df < 0 or (
                    (not self.dummy_sa) and 
                    (df > 0 and (np.random.random() < accept_prob))
                ): # accept new x
                    y_current = y_new
                    if y_new < self.best_y: # record best x
                        self.best_x = deepcopy(x_current)
                        self.best_y = y_new

                else: # discard new x
                    self.undo_update(x_current)

            if not self.silent:
                if len(accept_probs) == 0:
                    log_accept_prob = 'N'
                else: log_accept_prob = round(np.average(accept_probs), 4)

                print('%-13s%-25s%-13s%-12s%-9s%-11s%-10s%-10s' % (
                    'temperature:', self.T,
                    'accept_prob:', log_accept_prob,
                    'y_value:', round(self.best_y, 4),
                    'stay_cnt:', stay_counter
                ))

            self.iter_cycle += 1
            self.cool_down()
            self.generation_best_Y.append(self.best_y)

            # if best_y stay for max_stay_counter times, stop iteration
            if self.isclose(self.generation_best_Y[-1], self.generation_best_Y[-2]):
                stay_counter += 1
            else:
                stay_counter = 0

            if self.T < self.T_min:
                break

            if stay_counter > self.max_stay_counter:
                break
        
        print('num_best_cases:', len(self.generation_best_Y))

        return self.best_x
    
    def reset(self) -> None:
        self.best_x.reset()
        self.best_y = self.func(self.best_x)
        self.T = self.T_max
        self.iter_cycle = 0
        self.generation_best_Y = [self.best_y]


class LayoutSimulatedAnnealing(BaseSimulatedAnnealing[LayoutPatternCode]):

    def update(self, x: LayoutPatternCode) -> None:
        x.mutation()
    
    def undo_update(self, x: LayoutPatternCode) -> None:
        x.undo_mutation()

    def cool_down(self) -> None:
        self.T = self.T_max / (1 + np.log(1 + self.iter_cycle))


class RoutingSimulatedAnnealing(BaseSimulatedAnnealing[RoutingPatternCode]):

    def update(self, x: RoutingPatternCode) -> None:
        x.mutation()

    def undo_update(self, x: RoutingPatternCode) -> None:
        x.undo_mutation()

    def cool_down(self) -> None:
        self.T = self.T_max / (1 + np.log(1 + self.iter_cycle))
        # self.T *= 0.99