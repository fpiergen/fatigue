from beam import Beam

class SquareBeam(Beam):

    def __init__(self, w, h, rho, E, wt, span):
        super().__init__(E, wt/386.4, span)
        self.w = w
        self.h = h
        self.rho = rho*w*h
        self.I = self.momentOfInertia()
        self.fn = self.natFreqCantilverPointMassAndMassOfBeam(self.rho)

    def momentOfInertia(self):
        return 1/12*(self.w*self.h**3)
