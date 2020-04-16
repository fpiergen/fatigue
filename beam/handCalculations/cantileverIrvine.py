from minersFatigueBeamSolver import MinersFatigueBeamSolver
from context import Context
from squareBeam import SquareBeam

class CantileverIrvine(MinersFatigueBeamSolver):

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
        self.spanToHole = args.sth
        self.rho = args.rho

    def N(self, S):
        return  10**((34809 - S)/2466)

    def S(self, N):
        return -2466*np.log10(N) + 34809  # PSI

    def fatigueMe(self):
        # First let's get the first bending frequency for the cantilever beam.
        context = Context(SquareBeam(self.w, self.ht, self.rho, self.E, self.wt, self.span))
        fn = context.strategy.fn

        # input PSD
        self.psdInput(fn)

        # Calculate the stress levels based on the gs and MC/I

        k = 3 # Stress concentration factor round hole

        # The sress given is max at base of beam the hole is a bit up from base see beam.pdf in ref directory.
        oneSigma = (self.spanToHole/self.span)*context.strategy.maxStressCantileverPointMass(self.gsRMS, k) 
        print("See table that will open up on your default browser.  This will show the 1,2, and 3 sigma stresses for {:.1f} hz, corresponding cycles and n/N".format(fn))
        self.minersRuleApplication(oneSigma, fn)

        print("Max 1 Sigma Bending Stress at hole: " , float(round(oneSigma, 3)))

print("________________________________________________________________________________")
print("Fatigue results for Irvine RFatigue paper on cantilver beam.")
print("________________________________________________________________________________")

parser = MinersFatigueBeamSolver.getHelpParser('Rectangular cantilever beam from Irvine Paper RFatige given in reference directory')

parser.add_argument('--rho', '-rho', dest="rho", type=float, \
                    action='store', \
                    help="Density of beam-[slug-inch for rho of beam[(2700Kg/m3*2.2*0.0254**3)/386.4->0.00025]")
parser.add_argument('--sth', '-sth', dest="sth", type=float, \
                    action='store', \
                    help="Span to solder hole")

args = parser.parse_args()

cantileverIrvine = CantileverIrvine(args)
cantileverIrvine.fatigueMe();
