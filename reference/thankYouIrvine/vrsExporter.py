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

import sys

if sys.version_info[0] == 2:
    print ("Python 2.x")
    from tkFileDialog import asksaveasfilename
           
if sys.version_info[0] == 3:
    print ("Python 3.x")    
    from tkinter.filedialog import asksaveasfilename       

###############################################################################

class VRSExporter:

    def __init__(self, num_fi, fi, vrAtFn, ff, rdvrs, avrs, tsvrs, nsvrs, num_fn, ne):    


        self.num_fi=num_fi
        self.fi=fi
        self.vrAtFn=vrAtFn
        self.ff=ff
        self.rdvrs=rdvrs
        self.avrs=avrs
        self.tsvrs=tsvrs
        self.nsvrs=nsvrs
        self.num_fn=num_fn
        self.ne = ne

###############################################################################

    def export(self, master):
        root=master    
        #ne= int(self.Lbe.curselection()[0]) 

        output_file_path = asksaveasfilename(parent=root,title="Enter the output filename")           
        output_file = output_file_path.rstrip('\n') 

        if(self.ne==0):
            WriteData2(self.num_fn,self.ff,self.avrs,output_file)  

        if(self.ne==1):
            WriteData2(self.num_fn,self.ff,self.tsvrs,output_file)  

        if(self.ne==2):    
            WriteData2(self.num_fn,self.ff,self.nvrs,output_file)  

        if(self.ne==3):
            WriteData2(self.num_fn,self.ff,self.rdvrs,output_file)             

        if(self.ne==4):
            WriteData2(self.num_fi, self.fi, self.vrAtFn, output_file)             

