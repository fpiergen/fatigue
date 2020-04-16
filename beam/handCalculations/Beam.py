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

    def natFreqCantilverPointMassAndMassOfBeam(self, rho):
        return 1/(2*math.pi)*((3*self.E*self.I)/((0.2235*rho*self.span + self.m)*self.span**3))**0.5 # the 0.2235 is effective mass stuff found in beam.pdf in ref dir
        # slug -inch for rho of beam -> (2700Kg/m3 * 2.2*0.0254**3)/386.4 ---> 0.00025

    def maxStressSimplySupportedPointMass(self, gs):
        Mmax = self.m*386.4*gs*(self.span/2)*1/2 # 1/2 the weight
        Sigma = Mmax*(self.h/2)/self.I
        return Sigma

    def maxStressCantileverPointMass(self, gs, k):
        effectiveMass = (0.2235*self.rho*self.span + self.m)
        fOneSigma = effectiveMass * gs * 386.4
        Mmax = fOneSigma * self.span
        Sigma = k*Mmax*(self.h/2)/self.I
        return Sigma


    @abstractmethod
    def momentOfInertia(self, data):
        pass
