# Fatigue ( WORK IN PROGRESS )
Examples using Calculix and other sources to solve fatigue problems in Mechanical Engineering
## Summary
The motivation for this work is to be able to come up with a workflow for fatigue analysis using the open source Calculix finite element 
software package. We will start by doing a simple example using hand calculations. This example is one that is taken from the work done by Tom Irvine. The file 
is beam.pdf and is included in this repository. We then use that example and apply it to a problem I am currently working on. Apply 
a more advanced fatigue technique called Dirlik. Finally we will try to use Calculix to get stresses to be used with the Dirlik technique.


## History
- Modified Irvine VRS  code to seperate out objects to make it easier to add to and understand
- Modified Irvine VRS gui. Added calculation of the response of a given SDOF system(its natural frequency and Q as input) to a given PSD base input. 
- To use  go into reference/thankYouIrvine
```Python
python3 vrsGui.py
```
- With this gui you can export the psd response to be used with Dirlik method.

- Created taxiTopSupport and cantileverIrvine using strategy pattern. Use python3 <>.py --help to see input
(See also minersFatigueSolver abstract class)
- cantileverIrvine solves the problem outlined in RFatigue.pdf in reference directory
- taxitopSupport uses the same technique on the support for taxitop
- taxitopSupportDirlik uses the Dirlik fatigue method 

```Python
python3 taxiTopSupportUsingDirlik.py -w 1.5 -ht 0.75 -th .065 -E 10e6 -wt 20 -span 43 -df 0.5 -Q 10 -dur 1440 -df 0.5 -pf ISO16750-PSD-SPRUNG.dat
```
- NEXT:  Build an FE model of beam and get stress for harmonic input of base with RMS accelerations from PSD input. Use that as psd stress for input into the Dirlik fatigue method.

