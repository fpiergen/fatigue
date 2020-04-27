# importing the required module
import matplotlib.pyplot as plt
import numpy as np
from numpy import trapz

import sys
sys.path.append("../../../utilities")
#sys.path.append("../../utilities")

from myUtilities import MyUtilities


class VRAtFn:

    def __init__(self, psd, df, fn, Q):

        self._fi, self._ai = psd.convertPSDToHigherResolution(df)
        #self._fi = np.arange(1, psd[len(psd)-1], self.df)
        self._df = df
        self._vrAtFn=[]
        self._fn = fn
        self._zeta = 1./(2.*Q)
        self.__calculateVRAtFn()

    @property
    def fi(self):
        return self._fi

    @property
    def ai(self):
        return self._ai

    @property
    def vrAtFn(self):
        return self._vrAtFn

    def __calculateVRAtFn(self):
        rhoi =  self._fi/self._fn
        self._vrAtFn = ((1 + (2*self._zeta*rhoi)**2) / ((1 - rhoi**2)**2 + (2*self._zeta*rhoi)**2)) * self._ai

    def calculateRMS(self):
        area = trapz(self._vrAtFn, self._fi)
        grms = area**(1/2)
        print("GRMS(fn=",  float(round(self._fn,1)) , "hz) =", grms)
        return  grms;

    def asGsRMS(self):
        #rmsTot = 0; 
        f=[]
        grms=[]
        for i in range(len(self.fi)-1):
           rms = MyUtilities.g2ToRMS(self.vrAtFn[i], self.vrAtFn[i+1], self.fi[i], self.fi[i+1], False) 
           f.append(self.fi[i] + self._df/2)
           grms.append(rms)
        return (f, grms)
           #rmsTot = rmsTot + rms**2
       #print(rmsTot**(1/2))
        
    def plotGsRms(self, f, grms):
        plt.plot(f, grms)
        title_string='GsRMS '
        plt.title(title_string)
        plt.ylabel(' Grms (GMS)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
       


    def plotVRAtFn(self):

        grms = str(float(round(self.calculateRMS(),3)))
        plt.plot(self._fi, self._vrAtFn)
        title_string='Vibration Resp( fn=' + str(self._fn) + ' hz). GRMS: ' + grms
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()

'''
    def plotAll(self):
        plt.plot(self._PSDInput.fi, self._PSDResp)
        plt.plot(self._PSDInput.fi, self._PSDInput.PSD)
        title_string='Power Spectral Density With Resp   '+str("%6.3g" %self._PSDInput.rms)+' GRMS Overall '
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
'''

