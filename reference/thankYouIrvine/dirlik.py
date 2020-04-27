########################################################################
# program: dirlik.py
# author: Tom Irvine
# Modified to be used as object (Fabio Piergentili)
# version: 1.2
# date: April 21, 2020
# description:  
#    
# This program calculates the Dirlik rainflow range histogram for a
# response power spectral density.
#
#              
########################################################################

from __future__ import print_function

import matplotlib.pyplot as plt
from math import exp,sqrt,log 

from tompy import enter_float,GetInteger2,WriteData1
from vbUtilities import read_two_columns_from_dialog

from numpy import zeros,array,interp,floor,ceil,diff

import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename

           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename 
########################################################################  

class Dirlik:

    def __init__(self, f, psd, T):

        self.aa = f
        self.bb = psd
        self.T = T # seconds
        self.num = len(f)
        self.df = f[1] - f[0] 
        self.processPSD()
        self.calculate()



    def processPSD(self):
        """
        a = frequency column
        b = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """
        print ("\n samples = %d " % self.num)

        
        if(self.aa[0] <= 1.0e-20):
            self.f=self.aa[1:(self.num-1)]
            self.b=self.bb[1:(self.num-1)]
        else:
            self.f=self.aa
            self.b=self.bb
        
        nm1=self.num-1

        self.slope =zeros(nm1,'f')

        ra=0

        for i in range (0,nm1):
#
            s=log(self.b[i+1]/self.b[i])/log(self.f[i+1]/self.f[i])
            
            self.slope[i]=s
#
            if s < -1.0001 or s > -0.9999:
                ra+= ( self.b[i+1] * self.f[i+1]- self.b[i]*self.f[i])/( s+1.)
            else:
                ra+= self.b[i]*self.a[i]*log( self.f[i+1]/self.f[i])        

        self.rms=sqrt(ra)
        

########################################################################


########################################################################
    def calculate(self):
        self.m0=0
        self.m1=0
        self.m2=0
        self.m4=0

        n=len(self.f)

        for i in range(0,n):
            self.m0=self.m0+self.b[i]
            self.m1=self.m1+self.b[i]*self.f[i]
            self.m2=self.m2+self.b[i]*self.f[i]**2
            self.m4=self.m4+self.b[i]*self.f[i]**4

        self.m0=(self.m0*self.df)
        self.m1=(self.m1*self.df)
        self.m2=(self.m2*self.df)
        self.m4=(self.m4*self.df)
        
        EP=sqrt(self.m4/self.m2)
        
        x=(self.m1/self.m0)*sqrt(self.m2/self.m4)
        gamma=self.m2/(sqrt(self.m0*self.m4))
        
        D1=2*(x-gamma**2)/(1+gamma**2)
        R=(gamma-x-D1**2)/(1-gamma-D1+D1**2)
        D2=(1-gamma-D1+D1**2)/(1-R)
        D3=1-D1-D2
        
        Q=1.25*(gamma-D3-D2*R)/D1
        
        
        maxS=8*self.rms
        
        ds=maxS/400
        
        n=int(round(maxS/ds))
        
        self.N=zeros(n,'f')
        self.S=zeros(n,'f')
        self.cumu=zeros(n,'f')
        
        area=0
        cum=0
        
        for i in range(0,n): 
            self.S[i]=i*ds
            Z=self.S[i]/(2*sqrt(self.m0))
            t1=(D1/Q)*exp(-Z/Q)
            a=-Z**2
            b=2*R**2
        
            t2=(D2*Z/R**2)*exp(a/b)
            t3=D3*Z*exp(-Z**2/2)
        
            pn=t1+t2+t3
            pd=2*sqrt(self.m0)
            p=pn/pd
            
            self.N[i]=p
        
        self.N=self.N*EP*self.T
        
        for i in range(0,n): 
            area=area+self.N[i]*ds
            self.cumu[i]=area
        
        
        num=int(ceil(self.cumu[n-1]))
        
        xq=zeros(num,'d')
        for i in range(0,num):    
            xq[i]=i
        
        
        vq1 = interp(xq,self.cumu,self.S)
        
        
        peak_range=array(vq1)
        self.peak_range=sorted(peak_range, reverse=True)
        
        self.nn=len(peak_range)
        
        self.amp=[]
        
        for i in range(0,self.nn):
            self.amp.append(peak_range[i]/2.)
        
        print("\n Number of expected acceleration range = %d \n" %num)

    def exportArrays(self): 
        print (" ")
        print (" Find output dialog box") 

        root = tk.Tk() ; root.withdraw()
        output_file_path = asksaveasfilename(parent=root,title="Save the range values as...")           
        output_file = output_file_path.rstrip('\n')
        WriteData1(self.nn,self.peak_range,output_file)
   
        root = tk.Tk() ; root.withdraw()
        output_file_path = asksaveasfilename(parent=root,title="Save the amplitude values as...")
        output_file = output_file_path.rstrip('\n')
        WriteData1(self.nn,self.amp,output_file)

    def fatigueDamageIndex(self, b): 

        print ("\n Enter fatigue exponent")

        d=0
        for i in range(0,len(self.amp)):
            d=d+self.amp[i]**b

        print(" Relative fatigue damage index from amplitude = %8.4g " %d)
        return d

    def minersRatio(self, fatigueCurve):
       ratio=0
       i=0
       for stress in self.S:
           #print('Stress:', stress)
           #print('Count:', self.N[i])
           ratio = ratio + self.N[i]/fatigueCurve(stress/2)
           i = i + 1
        
       print ("Ratio = " , ratio)
       return 'TODO'
########################################################################

    def plot(self):
        plt.figure(1)     
        plt.plot(self.f,self.b)
        title_string='Stress Power Spectral Density   '+str("%6.3g" %self.rms)+' RMS Overall '
        plt.title(title_string)
        plt.ylabel(' PSD (units^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        
        
        plt.figure(2)
        plt.plot(self.S,self.N)
        plt.title('Histogram of Range (peak-valley)')
        plt.xlabel('Range')
        plt.ylabel('Counts')
        plt.grid(True)
        
        plt.figure(3)
        plt.plot(self.S,self.cumu)
        plt.title('Cumulative Histogram of Range (peak-valley)')
        plt.xlabel('Range')
        plt.ylabel('Count Running Sum')
        plt.grid(True)
        
        plt.show()
