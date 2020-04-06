# fatigue
Examples using Calculix and other sources to solve fatigue problems in Mechanical Engineering

## History
- Created main.py in beam directory. Use python3 main.py --help
```
Beam hand calculations for fatigue

optional arguments:
  -h, --help            show this help message and exit
  --w W, -w W           Width of box baem section
  --ht HT, -ht HT       Height of box baem section
  --th TH, -th TH       Thickness of box baem section
  --E E, -E E           Youngs Modulus [lbs/in2]
  --wt WT, -wt WT       Weight of point mass a center in lbs
  --span SPAN, -span SPAN
                        Span of beam
```

- Modified Irvine VRS  code to seperate out objects to make it easier to add to and understand
- Modified Irvine VRS gui to include response of single natural frequency
- To use  go into reference/thankYouIrvine
```Python
python3 vrsGui.py
```

