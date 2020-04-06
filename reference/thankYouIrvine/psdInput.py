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

from __future__ import print_function

from vbUtilities import read_two_columns_from_dialog,WriteData2  

from numpy import array,zeros,log,pi,sqrt,floor

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt


###############################################################################

class PSDInput:

    def __init__(self):

        self.f_=[]
        self.a_=[]
        self.slope_=[]
        self.grms_in=0

###############################################################################

    @property
    def f(self):
        return self.f_

    @property
    def a(self):
        return self.a_

    @property
    def slope(self):
        return self.slope_

    def readData(self, master):            
        """
        f = frequency column
        a = PSD column
        num = number of coordinates
        slope = slope between coordinate pairs    
        """

        print (" ")
        print (" The input file must have two columns: freq(Hz) & accel(G^2/Hz)")

        f,a,num =read_two_columns_from_dialog('Select Input File',master)

        print ("\n samples = %d " % num)

        f = array(f)
        a = array(a)

        nm1 = num-1

        slope = zeros(nm1,'f')

        ra=0

        for i in range (0,int(nm1)):
#
            s=log(a[i+1]/a[i])/log(f[i+1]/f[i])

            slope[i]=s
#
            if s < -1.0001 or s > -0.9999:
                ra+= ( a[i+1] * f[i+1]- a[i]*f[i])/( s+1.)
            else:
                ra+= a[i]*f[i]*log( f[i+1]/f[i])
        rms=sqrt(ra)
        three_rms=3*rms

        print (" ")
        print (" *** Input PSD *** ")
        print (" ")

        print (" Acceleration ")
        print ("   Overall = %10.3g GRMS" % rms)
        print ("           = %10.3g 3-sigma" % three_rms)

        self.grms_in=rms
        self.f_=f
        self.a_=a

        self.slope_=slope

    def  convertPSDToHigherResolution( self, df ):
        # The following converting the input PSD to a higher resolution to be
        # used to calculate the VRS.
        # The number of spectral points 
        nif=int(floor((max(self.f)-min(self.f))/df))

        # Frequence axis
        fi=zeros(nif,'f')
        # Acceleration level at each spectral location 
        ai=zeros(nif,'f')

        # The first point is what is given in PSD
        fi[0]=self.f[0]
        ai[0]=self.a[0]
        fmax=max(self.f)
        m=len(self.f)
        for i in range (0, int(nif)):

            fi[i]=self.f[0]+df*i

            if( fi[i] > fmax ):
                break

            iflag=0

            for j in range (0, int(m-1)):

                if( ( fi[i] >= self.f[j] ) and ( fi[i] <= self.f[j+1] ) and iflag==0  ):
                    ai[i]=self.a[j]*( ( fi[i] / self.f[j] )**self.slope[j] )
                    iflag=1

            #            print (fi[i],ai[i])
            # print  ("\n interp df = %10.4g Hz  nif=%d  max(fi)=%8.4g  m=%d\n" %(df,nif,max(fi),m))

        return  fi,ai


    def plot(self):
        plt.ion()
        plt.clf()
        plt.close(1)
        plt.figure(1)
        plt.plot(self.f_,self.a_)
        title_string='Power Spectral Density   '+str("%6.3g" %self.grms_in)+' GRMS Overall '
        plt.title(title_string)
        plt.ylabel(' Accel (G^2/Hz)')
        plt.xlabel(' Frequency (Hz) ')
        plt.grid(which='both')
        plt.savefig('power_spectral_density')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()
'''
        omega = 2*pi*a

        av=zeros(num,'f')
        ad=zeros(num,'f')

        for i in range (0,int(num)):
            av[i]=a[i]/omega[i]**2

        av=av*386**2
        rv=0

        for i in range (0,int(nm1)):
#
            s=log(av[i+1]/av[i])/log(f[i+1]/f[i])
#
            if s < -1.0001 or s > -0.9999:
                rv+= ( av[i+1] * f[i+1]- av[i]*f[i])/( s+1.)
            else:
                rv+= av[i]*f[i]*log( f[i+1]/f[i])         


        for i in range (0,int(num)):         
            ad[i]=av[i]/omega[i]**2

        rd=0

        for i in range (0,int(nm1)):
#
            s=log(ad[i+1]/ad[i])/log(f[i+1]/f[i])
#
            if s < -1.0001 or s > -0.9999:
                rd+= ( ad[i+1] * f[i+1]- ad[i]*f[i])/( s+1.)
            else:
                rd+= ad[i]*f[i]*log( f[i+1]/f[i])         
'''

