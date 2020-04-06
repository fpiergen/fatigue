import math
from abc import ABC, abstractmethod

class Beam(ABC):

    def __init__(self, E, m, span):
        self.E = E
        self.m = m
        self.span = span

# See beam.pdf in references, equation E-42
# First bending natural frequency
    def natFreqSimplySupportedPointMass(self):
        return 1/(2*math.pi)*6.928*((self.E*self.I)/(self.m*self.span**3))**0.5


    @abstractmethod
    def momentOfInertia(self, data):
        pass
