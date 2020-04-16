# Fatigue ( WORK IN PROGRESS )
Examples using Calculix and other sources to solve fatigue problems in Mechanical Engineering
## Summary
The motivation for this work is to be able to come up with a workflow fatigue analysis using the open source Calculix finite element 
software package. We will start by doing a simple example using hand calculations. This example is one that is taken from the work done by Tom Irvine. 
The file is beam.pdf and is included in this repository. Next we will use that example and apply it to a problem I am currently working on. After that
we will apply a more advanced fatigue technique called Dirlik. Finally we will try to use Calculix to get stresses to be used with the Dirlik technique.


## History
- Modified Irvine VRS  code to seperate out objects to make it easier to add to and understand
- Modified Irvine VRS gui. Added calculation of the response of a given SDOF system(its natural frequency and Q as input) to a given PSD base input. 
- To use  go into reference/thankYouIrvine
```Python
python3 vrsGui.py
```
- Created taxiTopSupport and cantileverIrvine using strategy pattern. Use python3 <>.py --help to see input
(See also minersFatigueSolver abstract class)
- cantileverIrvine solves the problem outlined in beam.pdf in reference directory
- taxitopSupport uses the same technique on the support for taxitop
- With this gui you can export the psd response to be used with Dirlik method.
- TODO: Next use Dirlik's method to see how it compares to procedure above (beam.pdf)

