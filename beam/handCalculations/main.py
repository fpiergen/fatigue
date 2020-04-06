from BoxBeam import BoxBeam
from BoxBeam2SideBySide import BoxBeam2SideBySide
from Context import Context
import argparse

parser = argparse.ArgumentParser( \
        description='Beam hand calculations for fatigue ', \
            add_help=True, allow_abbrev=True)
parser.add_argument('--w', '-w', dest="w", type=float, \
                    action='store', \
                    help="Width of box baem section")
parser.add_argument('--ht', '-ht', dest="ht", type=float, \
                    action='store', \
                    help="Height of box baem section")
parser.add_argument('--th', '-th', dest="th", type=float, \
                    action='store', \
                    help="Thickness of box baem section")
parser.add_argument('--E', '-E', dest="E", type=float, \
                    action='store', \
                    help="Youngs Modulus [lbs/in2]")
parser.add_argument('--wt', '-wt', dest="wt", type=float, \
                    action='store', \
                    help="Weight of point mass a center in lbs")
parser.add_argument('--span', '-span', dest="span", type=float, \
                    action='store', \
                    help="Span of beam")

args = parser.parse_args()

w  = args.w
ht  = args.ht
th  = args.th
E  = args.E
wt  = args.wt
span  = args.span

context = Context(BoxBeam2SideBySide(w, ht, th, E, wt, span))
context.doYourThing()
