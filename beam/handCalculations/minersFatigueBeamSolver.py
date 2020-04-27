import tkinter as tk 
import argparse

import sys
sys.path.append("../../reference/thankYouIrvine")
from psdInput import PSDInput
from vrAtFn import VRAtFn
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from abc import ABC, abstractmethod

class MinersFatigueBeamSolver(ABC):

    def __init__(self, dur, df, Q):
        self.dur = dur
        self.df = df
        self.Q = Q
        self.psd = ''

    @staticmethod
    def getHelpParser(description ):

        descriptionCommon = """We are assuming a normal distribution and that the
        load is all at the natural frequency which gives the  highest stress
        which is conservative. We are not taking into account the stress that
        fall out of the 3 Sigma range. That is not conservative. Also it is
        assumed he beam only vibrates at is natural frequency for calculating
        the cycles.""" 
        parser = argparse.ArgumentParser( \
                description=descriptionCommon + description, \
                add_help=True, allow_abbrev=True)
        parser.add_argument('--w', '-w', dest="w", type=float, \
                action='store', \
                help="Width of beam section")
        parser.add_argument('--ht', '-ht', dest="ht", type=float, \
                action='store', \
                help="Height of beam section")
        parser.add_argument('--E', '-E', dest="E", type=float, \
                action='store', \
                help="Youngs Modulus [lbs/in2]")
        parser.add_argument('--wt', '-wt', dest="wt", type=float, \
                action='store', \
                help="Weight of point mass in lbs")
        parser.add_argument('--span', '-span', dest="span", type=float, \
                action='store', \
                help="Span of beam")
        parser.add_argument('--df', '-df', dest="df", type=float, \
                action='store', \
                help="Frequency Resolution")
        parser.add_argument('--Q', '-Q', dest="Q", type=float, \
                action='store', \
                help="Q-factor (damping)")
        parser.add_argument('--dur', '-dur', dest="dur", type=float, \
                action='store', \
                help="Duration of load in mimutes")

        return parser


     # Ask for PSD then use it to get the rms gs for the natural frequency calculated above
    def psdInput(self, fn):
        root = tk.Tk()
        root.withdraw()
        psd = PSDInput()
        psd.readData(root)
        vr = VRAtFn(psd, self.df, fn, self.Q)
        self.gsRMS = vr.calculateRMS()

    def psdInput1(self, master):
        psd = PSDInput()
        psd.readData(master)
        self.psd = psd

    def psdInput2(self, file_path):
        psd = PSDInput(file_path)
        psd.readData('')
        self.psd = psd


    @abstractmethod
    def N(self, S):
        pass

    @abstractmethod
    def S(self, N):
        pass

    def plotSOfN(self):
        N1 = np.arange(1.0, 10e9, 10000)
        plt.figure()
        plt.title("S/N curve of material")
        plt.xlabel("Cycles")
        plt.ylabel("Stress")
        plt.semilogx(N1, self.S(N1))
        plt.show()

    def minersRuleApplication(self, oneSigma, fn):
        twoSigma = 2 * oneSigma
        threeSigma = 3 * oneSigma
        # Let's use Miners Rule to figure out if part can withstand the load
        # wihtout breaking
        #  %'s calculated from normal distribution   | 68.28  |
        #                                       |     95.45      |
        #                                    |       99.73          |
        
        stress = {'sigmas': np.around([oneSigma, twoSigma, threeSigma],1),
                'percentage': np.around([68.27/100, (95.45-68.27)/100, (99.73-95.45)/100],4)}
        testCycles = np.around(stress['percentage']*(fn*60*self.dur))
        limitCycles = np.around(self.N(stress['sigmas']),1) # this picks the N's from the graph based on stress
        nOverN = np.around(testCycles/self.N(stress['sigmas']),1)
        
        # Miners rule
        # Rn = n1/N1 + n2/N2 ...
        # When Rn = 1 part will fail
        # 
        # Below we tablulate it. It will open up on your browser. Fro there you can evaluate if part is safe.
        
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Stress', 'Time Ratio', 'Test Cycles(n)', 'Limit Cycles (N) from S-N', "n/N"],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
            cells=dict(values=[stress['sigmas'], # 1st column
                               stress['percentage'], # 2nd column
                               testCycles,
                               limitCycles,
                               nOverN], # 4th column
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='left'))
        ])
        
        fig.update_layout(width=800, height=400)
        fig.show()
