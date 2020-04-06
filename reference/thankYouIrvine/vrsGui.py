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

import sys
from vrsCalculator import VRSCalculator
from vrsExporter  import VRSExporter
from vrAtFn  import VRAtFn
from psdInput import PSDInput


if sys.version_info[0] == 2:
    print ("Python 2.x")
    import Tkinter as tk
    from tkFileDialog import asksaveasfilename
    import tkMessageBox

if sys.version_info[0] == 3:
    print ("Python 3.x")    
    import tkinter as tk 
    from tkinter.filedialog import asksaveasfilename       
    import tkinter.messagebox as tkMessageBox





from vbUtilities import read_two_columns_from_dialog,WriteData2  
from numpy import array,zeros,log,pi,sqrt,floor
from matplotlib.ticker import ScalarFormatter

import matplotlib.pyplot as plt


###############################################################################

class VRSGUI:

    def __init__(self,parent):    

        self.psdInput = PSDInput()
        self.vrsCalculator=''

        self.master=parent        # store the parent
        top = tk.Frame(parent)    # frame for all class widgets
        top.pack(side='top')      # pack frame in parent's window

        self.master.minsize(400,400)
        self.master.geometry("550x725")
        self.master.title("vb_vrs_gui.py ver 1.6  by Tom Irvine") 

###############################################################################


        crow=0

        self.hwtext3=tk.Label(top,text='=== PSD in(2 cols: Freq-Hz & Accel-G^2/Hz ===')
        self.hwtext3.grid(row=crow, column=0,columnspan=2, pady=6,sticky=tk.W)

        root=self.master  

        self.button_quit=tk.Button(top, text="Quit", command=lambda root=root:quit(root))
        self.button_quit.config( height = 2, width = 6, justify=tk.RIGHT )
        self.button_quit.grid(row=crow, column=1,pady=20)  



        crow=crow+1

        self.hwtext4=tk.Label(top,text='Select Output Units')
        self.hwtext4.grid(row=crow, column=1,columnspan=1, pady=6,sticky=tk.S)

        crow=crow+1

        self.button_read = tk.Button(top, text="Read Input File",command=self.readData)
        self.button_read.config( height = 3, width = 15 )
        self.button_read.grid(row=crow, column=0,columnspan=1,padx=0,pady=2,sticky=tk.N)

        self.Lb1 = tk.Listbox(top,height=2,exportselection=0)
        self.Lb1.insert(1, "G, in/sec, in")
        self.Lb1.insert(2, "G, m/sec, mm")
        self.Lb1.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lb1.select_set(0)

        crow=crow+1

        self.hwtext10=tk.Label(top,text='==================== VRS Calculation ==================')
        self.hwtext10.grid(row=crow, column=0,columnspan=2, pady=10,sticky=tk.S)    

        crow=crow+1

        self.hwtext_Q=tk.Label(top,text='Enter Q')
        self.hwtext_Q.grid(row=crow, column=0, columnspan=1, padx=14, pady=10,sticky=tk.S)

        self.hwtext_fn=tk.Label(top,text='Enter Duration (sec)')
        self.hwtext_fn.grid(row=crow, column=1, columnspan=1, padx=14, pady=10,sticky=tk.S)

        crow=crow+1

        self.Qr=tk.StringVar()  
        self.Qr.set('10')  
        self.Q_entry=tk.Entry(top, width = 12,textvariable=self.Qr)
        self.Q_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)    

        self.durr=tk.StringVar()  
        self.durr.set('')  
        self.dur_entry=tk.Entry(top, width = 12,textvariable=self.durr)
        self.dur_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)  



        crow=crow+1

        self.hwtext10=tk.Label(top,text='Minimum Plot Freq (Hz)')
        self.hwtext10.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.S)    

        self.hwtext11=tk.Label(top,text='Maximum Plot Freq (Hz)')
        self.hwtext11.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.S)


        crow=crow+1

        self.fminr=tk.StringVar()  
        self.fminr.set('')  
        self.fmin_entry=tk.Entry(top, width = 12,textvariable=self.fminr)
        self.fmin_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)  

        self.fmaxr=tk.StringVar()  
        self.fmaxr.set('')  
        self.fmax_entry=tk.Entry(top, width = 12,textvariable=self.fmaxr)
        self.fmax_entry.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)          

######


        crow=crow+1    

        self.button_calculate = tk.Button(top, text="Calculate", command=self.calculation)
        self.button_calculate.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate.grid(row=crow, column=1, padx=14, pady=1,sticky=tk.N)   
        #self.button_calculate.grid(row=crow, column=1, pady=20)         

        crow=crow+1

        self.hwtext10=tk.Label(top,text='=============== VR at fn Calculation ================')
        self.hwtext10.grid(row=crow, column=0,columnspan=2, pady=10,sticky=tk.S)    

        crow=crow+1

        self.hwtext10=tk.Label(top,text='fn (Hz)')
        self.hwtext10.grid(row=crow, column=0,columnspan=1, pady=10,sticky=tk.S)    

        self.hwtext11=tk.Label(top,text='Resolution (df)')
        self.hwtext11.grid(row=crow, column=1,columnspan=1, pady=10,sticky=tk.S)
        crow=crow+1

        self.fn=tk.StringVar()  
        self.fn.set('')  
        self.fn_entry=tk.Entry(top, width = 12,textvariable=self.fn)
        self.fn_entry.grid(row=crow, column=0,padx=14, pady=1,sticky=tk.N)  

        self.df=tk.StringVar()  
        self.df.set('')  
        self.df=tk.Entry(top, width = 12,textvariable=self.df)
        self.df.grid(row=crow, column=1,padx=14, pady=1,sticky=tk.N)  

        crow=crow+1
        self.button_calculate2 = tk.Button(top, text="Calculate", command=self.plotAtFn)
        self.button_calculate2.config( height = 2, width = 15,state = 'disabled')
        self.button_calculate2.grid(row=crow, column=1, padx=14, pady=1,sticky=tk.N)   

        crow=crow+1

        self.hwtext10=tk.Label(top,text='=================== Data Exporter ====================')
        self.hwtext10.grid(row=crow, column=0,columnspan=2, pady=10,sticky=tk.S)    

        crow=crow+1   

        self.button_export = tk.Button(top, text="Export Data", command=self.export)
        self.button_export.config( height = 2, width = 15,state = 'disabled')
        self.button_export.grid(row=crow, column=0, pady=10,sticky=tk.N)   

        self.Lbe = tk.Listbox(top,height=4,exportselection=0)
        self.Lbe.insert(1, "Accel VRS GRMS")
        self.Lbe.insert(2, "Accel VRS 3-sigma")
        self.Lbe.insert(3, "Accel VRS n-sigma")
        self.Lbe.insert(4, "Rel Disp VRS RMS")        

        self.Lbe.grid(row=crow, column=1, pady=2,sticky=tk.N)
        self.Lbe.select_set(0)  



###############################################################################
#
    def plotAtFn(self):
        print(self.fn.get())
        vrAtFn = VRAtFn(self.psdInput, float(self.df.get()), float(self.fn.get()), float(self.Qr.get()))
        vrAtFn.plotVRAtFn()

    def readData(self):
        self.psdInput.readData(self.master)
        self.psdInput.plot()
        self.button_calculate.config(state = 'normal')
        self.button_calculate2.config(state = 'normal')

    def calculation(self):
        nu = int(self.Lb1.curselection()[0])
        Q = float(self.Qr.get())
        dur = float(self.durr.get())
        fminp = float(self.fminr.get())
        fmaxp = float(self.fmaxr.get())
        self.vrsCalculator = VRSCalculator(dur, Q, fminp, fmaxp, self.psdInput, nu)
        self.vrsCalculator.calculate()
        self.vrsCalculator.plotIt()
        self.button_export.config(state = 'normal')

    def export(self):
        ne= int(self.Lbe.curselection()[0])
        vrsExporter = VRSExporter(self.vrsCalculator.ff,
                self.vrsCalculator.rdvrs, self.vrsCalculator.avrs,
                self.vrsCalculator.tsvrs, self.vrsCalculator.nsvrs, self.vrsCalculator.numFn, ne)
        vrsExporter.export(self.master)

    def quit(root):
        root.destroy()

###############################################################################
root = tk.Tk()
app = VRSGUI(root)
root.mainloop()
