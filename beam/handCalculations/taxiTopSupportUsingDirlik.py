import tkinter as tk 
import numpy as np
import sys
sys.path.append("../.")
sys.path.append("../../reference/thankYouIrvine")
sys.path.append("../../utilities")
from myUtilities import MyUtilities
from minersFatigueBeamSolver import MinersFatigueBeamSolver
from boxBeam2SideBySide import BoxBeam2SideBySide
from context import Context
from vrAtFn import VRAtFn
from dirlik import Dirlik

class TaxiTopSupportUsingDirlik(MinersFatigueBeamSolver):

    def __init__(self, args):

        super().__init__(args.dur, args.df, args.Q)
        self.psdFile = args.pf
        self.w = args.w
        self.ht = args.ht
        self.E = args.E
        self.wt = args.wt
        self.span = args.span
        self.df = args.df
        self.Q = args.Q
        self.dur = args.dur
        self.th = args.th
        self.fatigueMe()

    def N(self, S):
        return  10**((34809 - S)/2466)

    def S(self, N):
        return -2466*np.log10(N) + 34809  # PSI


    def fatigueMe(self):

        # Base input PSD
        self.psdInput2(self.psdFile)

        # Let's get the first bending frequency for two box beams side by side using given input.
        context = Context(BoxBeam2SideBySide(self.w, self.ht, self.th, self.E, self.wt, self.span))
        fn = context.strategy.fn

        # lets get the response for a SDOF system estimation of the beam 
        vrForFn = VRAtFn(self.psd, self.df, fn, self.Q)
        # vrForFn.plotVRAtFn()

        # Get the GsRMS
        f,grms = vrForFn.asGsRMS()
        #vrForFn.plotGsRms(f,grms)

        # Get stress at each spectral location
        stresses = []
        for gs in grms:
            stresses.append(context.strategy.maxStressSimplySupportedPointMass(gs))
        # MyUtilities.plot(f, stresses, 'Stress', 'Frequency(Hz)','Stress(psi)')

        # Convert to PSD stress
        psdStresses = []
        for stress in stresses:
            psdStresses.append(MyUtilities.RMSTog2(stress, self.df))
        # MyUtilities.plot(f, psdStresses, 'Stress', 'Frequency(Hz)','Stress(psi**2/hz)')

        # Use the dirlik method for fatigue estimation
        dirlik = Dirlik(f, psdStresses, self.dur*60)
        dirlik.plot()

        # Apply miners to see if part is safe
        dirlik.minersRatio(self.N)

print("________________________________________________________________________________")
print("Fatigue results for two box beams side by side holding smart top on taxi cab. ISOBlah for base input.")
print("________________________________________________________________________________")

parser = MinersFatigueBeamSolver.getHelpParser('Two box beam\'s side by side. Simulate taxitop support')

parser.add_argument('--th', '-th', dest="th", type=float, \
                    action='store', \
                    help="Thickness of box section")

parser.add_argument('--pf', '-pf', dest="pf", type=str, \
                    action='store', \
                    help="Input PSD File")

args = parser.parse_args()
#root = tk.Tk()
taxiTop = TaxiTopSupportUsingDirlik(args)
#root.mainloop()
