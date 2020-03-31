from Beam import Beam

class BoxBeam(Beam):

    def __init__(self, w, h, th):
        super().__init__(29e6, 60/386.4, 43)
        self.w = w
        self.h = h
        self.th = th
        self.I = self.momentOfInertia()
        self.fn = self.natFreqSimplySupportedPointMass()

    def momentOfInertia(self):
        return 1/12*(self.w*self.h**3 - (self.w-2*self.th)*((self.h-2*self.th))**3)
