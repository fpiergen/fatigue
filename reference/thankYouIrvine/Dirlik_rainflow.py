########################################################################
# program: Dirlik_rainflow.py
# author: Tom Irvine
# version: 1.2
# date: November 9, 2013
# description:  
#    
# This program calculates the Dirlik rainflow range histogram for a
# response power spectral density.
#
# The response power spectral density may vary arbitrarily with frequency.
# The input file must have two columns: frequency(Hz) & psd(units^2/Hz)
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

def interpolate_PSD(f,a,s,df):

    nif=int(floor((max(f)-min(f))/df))

    fi=zeros(nif,'f')
    ai=zeros(nif,'f')

    fi[0]=f[0]
    ai[0]=a[0]

    fmax=max(f)

    m=len(f)
    
    j1=0

    for i in range (0,nif): 	
        fi[i]=f[0]+df*i

        if( fi[i] > fmax ):
            break
    
        iflag=0
    
        for j in range (j1,m-1):
		
            if( ( fi[i] >= f[j] ) and ( fi[i] <= f[j+1] ) and iflag==0  ):
					
                ai[i]=a[j]*( ( fi[i] / f[j] )**slope[j] )
                iflag=1
                j1=j
                break

    return fi,ai,nif    

########################################################################  

def EnterPSD():
    """
    a = frequency column
    b = PSD column
    num = number of coordinates
    slope = slope between coordinate pairs    
    """
    print (" ")
    print (" The input file must have two columns: freq(Hz) & PSD(unit^2/Hz)")
  
    aa,bb,num=read_two_columns_from_dialog('Select File', root)    

    print ("\n samples = %d " % num)

    
    if(aa[0] <= 1.0e-20):
        a=aa[1:(num-1)]
        b=bb[1:(num-1)]
    else:
        a=aa
        b=bb
    
    num=len(a)
    nm1=num-1

    slope =zeros(nm1,'f')

    ra=0

    for i in range (0,nm1):
#
        s=log(b[i+1]/b[i])/log(a[i+1]/a[i])
        
        slope[i]=s
#
        if s < -1.0001 or s > -0.9999:
            ra+= ( b[i+1] * a[i+1]- b[i]*a[i])/( s+1.)
        else:
            ra+= b[i]*a[i]*log( a[i+1]/a[i])        

    rms=sqrt(ra)
    
    return a,b,rms,num,slope         

########################################################################
root = tk.Tk()
#root.withdraw()

plt.close("all")

f,a,rms,num,slope = EnterPSD()

print (" ")
print (" Enter duration (sec)")

T=enter_float()

########################################################################

difff=diff(f)
dfmin=min(difff)
dfmax=max(difff)

if( abs(dfmax-dfmin) > 1.25*dfmin):
    print('\n PSD frequency step is variable. ')
    print('\n Enter frequency step (Hz) for interpolation ')
    df=enter_float()
    [fi,ai,n]=interpolate_PSD(f,a,slope,df)
else:
    np=len(f)
    df=(f[np-1]-f[0])/(np-1)
    fi=f
    ai=a


print (" Calculating moments ")

m0=0
m1=0
m2=0
m4=0

n=len(fi)

for i in range(0,n):    
    m0=m0+ai[i]
    m1=m1+ai[i]*fi[i]
    m2=m2+ai[i]*fi[i]**2
    m4=m4+ai[i]*fi[i]**4


m0=(m0*df)
m1=(m1*df)
m2=(m2*df)
m4=(m4*df)

EP=sqrt(m4/m2)

x=(m1/m0)*sqrt(m2/m4)
gamma=m2/(sqrt(m0*m4))

D1=2*(x-gamma**2)/(1+gamma**2)
R=(gamma-x-D1**2)/(1-gamma-D1+D1**2)
D2=(1-gamma-D1+D1**2)/(1-R)
D3=1-D1-D2

Q=1.25*(gamma-D3-D2*R)/D1


maxS=8*rms

ds=maxS/400

n=int(round(maxS/ds))

N=zeros(n,'f')
S=zeros(n,'f')
cumu=zeros(n,'f')

area=0
cum=0

for i in range(0,n): 
    S[i]=i*ds
    Z=S[i]/(2*sqrt(m0))
    t1=(D1/Q)*exp(-Z/Q)
    a=-Z**2
    b=2*R**2

    t2=(D2*Z/R**2)*exp(a/b)
    t3=D3*Z*exp(-Z**2/2)

    pn=t1+t2+t3
    pd=2*sqrt(m0)
    p=pn/pd
    
    N[i]=p

N=N*EP*T

for i in range(0,n): 
    area=area+N[i]*ds
    cumu[i]=area


num=int(ceil(cumu[n-1]))

xq=zeros(num,'d')
for i in range(0,num):    
    xq[i]=i


vq1 = interp(xq,cumu,S)


peak_range=array(vq1)
peak_range=sorted(peak_range, reverse=True)

nn=len(peak_range)

amp=[]

for i in range(0,nn):
    amp.append(peak_range[i]/2.)

print("\n Number of expected acceleration range = %d \n" %num)

print(' The following arrays are available in descending order:')
print(' ')
print(' The range values     (peak-valley)    : range ')
print(' The amplitude values (peak-valley)/2  : amp ')

print(" ")        
print("  Export arrays:  1=yes 2=no ")

idf = GetInteger2()
        
if(idf==1):
    
    print (" ")
    print (" Find output dialog box") 

    root = tk.Tk() ; root.withdraw()
    output_file_path = asksaveasfilename(parent=root,title="Save the range values as...")           
    output_file = output_file_path.rstrip('\n')
    WriteData1(nn,peak_range,output_file)
   
    root = tk.Tk() ; root.withdraw()
    output_file_path = asksaveasfilename(parent=root,title="Save the amplitude values as...")
    output_file = output_file_path.rstrip('\n')
    WriteData1(nn,amp,output_file)


print(" ")        
print("  Calculate relative fatigue damage index?  1=yes 2=no ")

ifat = GetInteger2()


b=0
if(ifat==1):
    print ("\n Enter fatigue exponent")
    b=enter_float()

    d=0
    for i in range(0,len(amp)):
        d=d+amp[i]**b
    
    print(" Relative fatigue damage index from amplitude = %8.4g " %d)

########################################################################

print (" ")
print (" view plots ")

plt.figure(1)     
plt.plot(fi,ai)
title_string='Power Spectral Density   '+str("%6.3g" %rms)+' RMS Overall '
plt.title(title_string)
plt.ylabel(' PSD (units^2/Hz)')
plt.xlabel(' Frequency (Hz) ')
plt.grid(which='both')
plt.savefig('power_spectral_density')
plt.xscale('log')
plt.yscale('log')


plt.figure(2)
plt.plot(S,N)
plt.title('Histogram of Range (peak-valley)')
plt.xlabel('Range')
plt.ylabel('Counts')
plt.grid(True)

plt.figure(3)
plt.plot(S,cumu)
plt.title('Cumulative Histogram of Range (peak-valley)')
plt.xlabel('Range')
plt.ylabel('Count Running Sum')
plt.grid(True)

plt.show()
