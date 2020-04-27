from minersFatigueBeamSolver import MinersFatigueBeamSolver
from context import Context
from boxBeam2SideBySide import BoxBeam2SideBySide
import numpy as np
import sys
sys.path.append("../../reference/thankYouIrvine")
sys.path.append("../../../utilities")
from vrAtFn import VRAtFn
from myUtilities import MyUtilities

class TaxiTopSupport(MinersFatigueBeamSolver):

    def __init__(self, args):

        super().__init__(args.dur, args.df, args.Q)
        self.w = args.w
        self.ht = args.ht
        self.E = args.E
        self.wt = args.wt
        self.span = args.span
        self.df = args.df
        self.Q = args.Q
        self.dur = args.dur
        self.th = args.th
        self.psdFilePath = args.pf

    def N(self, S):
        return  10**((34809 - S)/2466)

    def S(self, N):
        return -2466*np.log10(N) + 34809  # PSI

    def fatigueMe(self):
        # First let's get the first bending frequency for the cantilever beam.
        context = Context(BoxBeam2SideBySide(self.w, self.ht, self.th, self.E, self.wt, self.span))
        fn = context.strategy.fn

        # input PSD
        self.psdInput2(self.psdFilePath)

        # get the gsRms for response of a SDOD system with fn
        vr = VRAtFn(self.psd, self.df, fn, self.Q)
        self.gsRMS = vr.calculateRMS()

        self.plotSOfN()
        # Calculate the stress levels based on the gs and MC/I
        vr.plotVRAtFn()

        oneSigma = context.strategy.maxStressSimplySupportedPointMass (self.gsRMS) 
        print("See table that will open up on your default browser.  This will show the 1,2, and 3 sigma stresses for {:.1f} hz, corresponding cycles and n/N".format(fn))
        self.minersRuleApplication(oneSigma, fn)

        print("Max 1 Sigma Bending Stress: " , float(round(oneSigma, 3)))

print("________________________________________________________________________________")
print("Fatigue results for two box beams sisde by side holding smart top on taxi cab")
print("________________________________________________________________________________")

parser = MinersFatigueBeamSolver.getHelpParser('Two box beam\'s side by side. Simulate taxitop support')

parser.add_argument('--th', '-th', dest="th", type=float, \
                    action='store', \
                    help="Thickness of box section")

parser.add_argument('--pf', '-pf', dest="pf", type=str, \
                    action='store', \
                    help="Base input psd file")

args = parser.parse_args()
taxiTop = TaxiTopSupport(args)
taxiTop.fatigueMe();
