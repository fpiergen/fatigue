########################################################################
# program: vb_vrs_gui.py
# author: Tom Irvine
# Email: tom@vibrationdata.com
# version: 1.6
# date: October 17, 2014
# description:  
#    
#  This script will calculate a vibration response spectrum for a 
#  PSD base input.
#              
########################################################################

from numpy import array,zeros,log,pi,sqrt,floor

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt


###############################################################################

class VRSCalculator:

    def __init__(self, dur, Q, fminp, fmaxp, psd, nu):    

        # Input
        self.Q = Q
        self.dur = dur
        self.fminp = fminp
        self.fmaxp = fmaxp
        self.psd = psd
        self.nu = nu

        # output
        self._ff=[]
        self._rdvrs=[]
        self._avrs=[]
        self._tsvrs=[] 
        self._nsvrs=[]

        self._numFn=0

###############################################################################


    @property
    def ff(self):
        return self._ff

    @property
    def rdvrs(self):
        return self._rdvrs

    @property
    def avrs(self):
        return self._avrs

    @property
    def tsvrs(self):
        return self._tsvrs

    @property
    def nsvrs(self):
        return self._nsvrs

    @property
    def numFn(self):
        return self._numFn

    def calculate(self):

        tpi=2*pi
        tpi_sq=tpi**2

        # Set the frequency resolution
        df= 1/40.

        if( self.fminp >= 1):
            df =  self.fminp/40.

        # Convert the PSD to higher resolution frequency spectrum and set variables
        # required for furher calculation
        fi,ai = self.psd.convertPSDToHigherResolution(df)
        last=len(fi)
        a_vrs=zeros(last,'f')
        rd_vrs=zeros(last,'f')


        # Build the natural frequency spectrum 
        fn,kk,nfn = self.buildFn(fi, last, tpi, tpi_sq)
        
        # From here on in we calculate the VRS based on equation 8 in vrs.pdf
        # given in reference directory in this repository

        i1=0
        i2=0
        i3=0
        i4=0
        L1=0.2
        L2=0.4
        L3=0.6
        L4=0.8

        # Variables required below
        damp=1./(2.*self.Q)
        tdamp=2*damp
        tdamp2=tdamp**2.

        print (" ")
        print ("calculating vrs.  Percent complete: ")
        # The nested loops is the calculation of equation 8 including the
        # displacement format
        for i in range(0,int(kk)):   # natural frequency loop

            ratio=float(i)/float(kk)


            if(ratio>L1 and i1==0):
                i1=1
                print("%3.0f" %(100*ratio))

            if(ratio>L2 and i2==0):
                i2=1
                print("%3.0f" %(100*ratio))

            if(ratio>L3 and i3==0):
                i3=1
                print("%3.0f" %(100*ratio))

            if(ratio>L4 and i4==0):
                i4=1
                print("%3.0f" %(100*ratio))

#   absolute acceleration

            fn2=fn[i]**2.

            suma=0.
            sumr=0.

            for j in range(0,int(last)):

                rho = fi[j]/fn[i]
                tdr=tdamp*rho

                c1= tdr** 2.
                c2= (1.- (rho**2.))** 2.

                suma+= ai[j]*(1.+ c1 ) / ( c2 + c1 )

                fi2=fi[j]**2.

                c1= (fn2-fi2)**2.
                c2= tdamp2*fn2*fi2

                sumr+= ai[j]/ ( c2 + c1 )


            rd_vrs[i]=sqrt(sumr*df)/tpi_sq
            a_vrs[i]=sqrt(suma*df)


        ratio=1
        print("%3.0f" %(100*ratio))
        print ("")    
###############################################################################

        nn=len(a_vrs) 

        ff=[]
        avrs=[]
        tsvrs=[]
        nsvrs=[]
        rdvrs=[]

        if(self.nu==0):
            rd_vrs*=386
        else:
            rd_vrs*=9.81*1000


        for i in range(0,int(nn)):

            if(fn[i]>=self.fminp and fn[i]<=self.fmaxp):
                ff.append(fn[i])
                avrs.append(a_vrs[i])
                tsvrs.append(3*a_vrs[i])
                c=sqrt(2*log(fn[i]*self.dur))
                ms=c + 0.5772/c
                nsvrs.append(ms*a_vrs[i])
                rdvrs.append(rd_vrs[i])

        self._ff=ff
        self._avrs=avrs
        self._tsvrs=tsvrs
        self._nsvrs=nsvrs
        self._rdvrs=rdvrs
        self._numFn=len(self._ff)

    def buildFn( self, fi, last, tpi, tpi_sq ):

        fn=zeros(20000,'f')

        fn[0]=5.
        oct=1./24.

        nfn=len(fn)


        kk=0

        for i in range(0,int(nfn)):   # natural frequency loop
            if(fn[i] > nfn):
                break

            if(fn[i] > 2.*fi[last-1] ):
                break

            fn[i+1] = fn[i]*(2.**oct)  

            kk+=1

        return fn, kk, nfn



    def plotIt(self):

        plt.close(2)
        plt.figure(2)

        plt.plot(self._ff,self._nsvrs,label='peak')
        plt.plot(self._ff,self._tsvrs,label='3-sigma')
        plt.plot(self._ff,self._avrs,label='1-sigma')


        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        #Q=1/(2*damp)
        title_string= 'Acceleration Vibration Response Spectrum Q='+str(self.Q)
#
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= 'Acceleration Vibration Response Spectrum Q='+str(i)
                break
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')
        plt.ylabel('Accel (G)')
        plt.grid(True, which="both")

        plt.legend(loc="upper left") 

        if(self.fminp==20 and self.fmaxp==2000):

            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(self.fminp,self.fmaxp))    

            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              

        plt.xlim([self.fminp,self.fmaxp])    

        plt.draw()


###############################################################################

        plt.close(3)
        plt.figure(3)        

        plt.plot(self._ff,self._rdvrs)

        if(self.nu==0):
            plt.ylabel('Rel Disp (inch RMS)')
        else:
            plt.ylabel('Rel Disp (mm RMS)')      


        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True)
#
        #Q=1/(2*damp)
        title_string= 'Relative Displacement Vibration Response Spectrum Q='+str(self.Q)
#
        for i in range(1,200):
            if(self.Q==float(i)):
                title_string= 'Relative Displacement Vibration Response Spectrum Q='+str(i)
                break
#
        plt.title(title_string)
        plt.xlabel('Natural Frequency (Hz) ')        

        plt.grid(True, which="both")

        if(self.fminp==20 and self.fmaxp==2000):

            ax=plt.gca().xaxis
            ax.set_major_formatter(ScalarFormatter())
            plt.ticklabel_format(style='plain', axis='x', scilimits=(self.fminp,self.fmaxp))    

            extraticks=[20,2000]
            plt.xticks(list(plt.xticks()[0]) + extraticks)                              

        plt.xlim([self.fminp,self.fmaxp])          

        plt.draw()      


        #self.ff=ff
        #self.rdvrs=rdvrs
        #self.avrs=avrs
        #self.tsvrs=tsvrs
        #self.nsvrs=nsvrs        

        #self.num_fn=len(ff)

        # self.button_export.config(state = 'normal')        

        print ("Calculation complete.  View Plots.")
