import math
import matplotlib.pyplot as plt
import os
import sys
import re
import numpy as np


# see https://femci.gsfc.nasa.gov/random/randomgrms.html
class MyUtilities():

    @staticmethod
    def g2ToRMS(PSDl, PSDh, fl, fh, printMe=True):

        dBValue= 10*math.log10(PSDh/PSDl)

        # slope
        numberOfOctaves = math.log10(fh/fl)/math.log10(2)
        m = dBValue/numberOfOctaves

        # grms for bandwidth
        A = 10*math.log10(2)*(PSDh/(10*math.log10(2)+m))*(fh-fl*(fl/fh)**(m/(10*math.log10(2))))
        grms = math.sqrt(A)

        if (printMe) :
            print ("Number of octaves = " + str(numberOfOctaves))
            print ("PSDBandDbValue = " + str(dBValue))
            print ("m = " + str(m))
            print ("A = " + str(A))
            print ("grms = " + str(grms))

        return grms

    @staticmethod
    def RMSTog2(grms, df):
        return grms**2/df

    @staticmethod
    def plot(x, y, title, xlabel, ylabel):
        plt.plot(x, y)
        title_string=title
        plt.title(title_string)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.grid(which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()

    @staticmethod
    def readFile(file_path):

        print (file_path)
        if not os.path.exists(file_path):
            print ("This file doesn't exist")

        if os.path.exists(file_path):
            print ("This file exists")
            print (" ")
            infile = open(file_path,"rb")
            lines = infile.readlines()
            print('Numnber of lines read', len(lines))
            infile.close()

            a = []
            b = []
            num=0
            for line in lines:
#
                if sys.version_info[0] == 3:            
                    line = line.decode(encoding='UTF-8') 
            
                if re.search(r"(\d+)", line):  # matches a digit
                    iflag=0
                else:
                    iflag=1 # did not find digit
#
                if re.search(r"#", line):
                    iflag=1
#
                if iflag==0:
                    line=line.lower()
                    if re.search(r"([a-d])([f-z])", line):  # ignore header lines
                        iflag=1
                    else:
                        line = line.replace(","," ")
                        col1,col2=line.split()
                        a.append(float(col1))
                        b.append(float(col2))
                        num=num+1
            a=np.array(a)
            b=np.array(b)

        return a,b,num


