#! /usr/bin/env python3
#---------------------------------
#   Plots errors of experiments
#      obtained from iModel output
#   Pedro Peixoto (ppeixoto@usp.br)
#   May 2019
#----------------------------------


import sys
import os
import re
import string
import numpy as np

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#Custom plotting setup
import imodel_plot
from imodel_plot import Plotter, PlotterPanel

#imodel routines
import imodel_data
from imodel_data import imodelData 

# input filename
input_filename = 'errors.txt'
if len(sys.argv) <= 1 :
	print("I need 1 argument:")
	print("A filename containing the errors generated by imodel")
	sys.exit(1)
	
if len(sys.argv) > 1:
	input_filename = sys.argv[1]
	
data=imodelData(input_filename)

#Dictionary for fancy naming
data.FancyNames("naming_conv.csv") #Load naming convention
print()

#Filter options based on user input
data.UserOptions("options.csv") #load user options

# Decide what to plot based on
# -Inloop - goes into a graph
# -MidLoop - goes into separate panels - defines the flot data to be plotted
# -OutLoop - goes into different figures
# See header 
#data.LoopOptions() #load user inner/outer loops for plotting - inner is within legend (each graph), outer


#Loop over outer loop
for xout in data.varoptions["OutLoop"]:
	print(xout)
	for x in data.varoptions[xout]:
		print(x)

#plot swm convergence data
#outname=input_filename.replace('.txt','.eps')

#title="Test case "+str(int(data.data["TCase"][1]))
#print(title)

""" 
if 'Field' in data.datastr:
for f in fields_list:
	
	title=dict.names.get(f, f)
	figure = PlotterPanel( 2, title, ["grid points", "grid points"], ["max error", "rms error"])
	c = 0
	for mtd in methods_list:
		mtdname=dict.names.get(mtd, mtd)
		for grd in grids_list:
			grdname=dict.names.get(grd, grd)
			name=mtdname+" "+grdname			
			x = []
			ymax = []
			yrms = []
			for i, val in enumerate(maxerrors):
				if field[i] == f and methods[i] == mtd and gridnames[i] == grd:
					x.append(gridres[i])
						ymax.append(maxerrors[i])
						yrms.append(rmserrors[i])
				figure.plot( 0, x, ymax, label=name, i=c)
				figure.plot( 1, x, yrms, label=name, i=c)
				c = c + 1
				
				#plt.show()
				
		figure.finish(outname)

	#figurerms.finish(outnamerms)


#plt.show()
 """
