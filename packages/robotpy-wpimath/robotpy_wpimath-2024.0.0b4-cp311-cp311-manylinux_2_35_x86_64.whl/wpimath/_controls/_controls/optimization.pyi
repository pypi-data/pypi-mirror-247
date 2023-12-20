from __future__ import annotations
import typing
__all__ = ['SimulatedAnnealing']
class SimulatedAnnealing:
    """
    An implementation of the Simulated Annealing stochastic nonlinear
    optimization method.
    
    @see <a
    href="https://en.wikipedia.org/wiki/Simulated_annealing">https://en.wikipedia.org/wiki/Simulated_annealing</a>
    @tparam State The type of the state to optimize.
    """
    def __init__(self, initialTemperature: float, neighbor: typing.Callable[[typing.Any], typing.Any], cost: typing.Callable[[typing.Any], float]) -> None:
        """
        Constructor for Simulated Annealing that can be used for the same functions
        but with different initial states.
        
        :param initialTemperature: The initial temperature. Higher temperatures make
                                   it more likely a worse state will be accepted during iteration, helping
                                   to avoid local minima. The temperature is decreased over time.
        :param neighbor:           Function that generates a random neighbor of the current
                                   state.
        :param cost:               Function that returns the scalar cost of a state.
        """
    def solve(self, initialGuess: typing.Any, iterations: int) -> typing.Any:
        """
        Runs the Simulated Annealing algorithm.
        
        :param initialGuess: The initial state.
        :param iterations:   Number of iterations to run the solver.
        
        :returns: The optimized state.
        """
