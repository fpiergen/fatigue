from minersFatigueBeamSolver import MinersFatigueBeamSolver
from context import Context
from boxBeam2SideBySide import BoxBeam2SideBySide
import numpy as np

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

    def N(self, S):
        return  10**((34809 - S)/2466)

    def S(self, N):
        return -2466*np.log10(N) + 34809  # PSI

    def fatigueMe(self):
        # First let's get the first bending frequency for the cantilever beam.
        context = Context(BoxBeam2SideBySide(self.w, self.ht, self.th, self.E, self.wt, self.span))
        fn = context.strategy.fn

        # input PSD
        self.psdInput(fn)

        self.plotSOfN()
        # Calculate the stress levels based on the gs and MC/I

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

args = parser.parse_args()

taxiTop = TaxiTopSupport(args)
taxiTop.fatigueMe();
'''
print("________________________________________________________________________________")
print("Fatigue results for simply supported beam two side by side with given crossection")
print("________________________________________________________________________________")
# First let's get the first bending frequency from the simply supported beam.
context = Context(BoxBeam2SideBySide(w, ht, th, E, wt, span))
fn = context.strategy.fn

# Next get the rms gs for the natural frequency and selected PSD
root = tk.Tk()
root.withdraw()
psd = PSDInput()
psd.readData(root)
vr = VRAtFn(psd, df, fn, Q)
gsRMS = vr.calculateRMS()

# Now get the stress levels

print("Max Bending Stress: " ,
        float(round(context.strategy.maxStressSimplySupportedPointMass(gsRMS),3)))
        '''
