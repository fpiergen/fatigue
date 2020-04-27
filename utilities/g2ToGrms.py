import math
import argparse
from myUtilities import MyUtilities

parser = argparse.ArgumentParser( \
        description='Calculate GRMS from PSD (see https://femci.gsfc.nasa.gov/random/randomgrms.html)', \
            add_help=True, allow_abbrev=True)
parser.add_argument('--fl', '-fl', dest="fl", type=float, \
                    action='store', \
                    help="Lower frequency")
parser.add_argument('--fh', '-fh', dest="fh", type=float, \
                    action='store', \
                    help="High frequency")

parser.add_argument('--PSDl', '-pl', dest="PSDl", type=float, \
                    action='store', \
                    help="PSD [g2/hz] at lower frequency")

parser.add_argument('--PSDh', '-ph', dest="PSDh", type=float, \
                    action='store', \
                    help="PSD [g2/hz] at high frequency")

args = parser.parse_args()


fl  = args.fl
fh  = args.fh
PSDl  = args.PSDl
PSDh  = args.PSDh

printInfo = False
val1 = MyUtilities.g2ToRMS(PSDl, PSDh, fl, fh, printInfo)
val2 = MyUtilities.RMSTog2(val1, fh-fl)
print ("rms: ", val1)
print ("g2/hz: ", val2)
