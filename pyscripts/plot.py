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

if len(sys.argv) <= 2 :
	print("I need a 2nd argument:")
	print("A filename containing the options of graphing (see options_template.csv")
	sys.exit(1)
	
if len(sys.argv) > 1:
	input_filename = sys.argv[1]
	opt_filename = sys.argv[2]


#Get data
data=imodelData(input_filename)

#Calculate 10-folding times, if required
data.CalcFoldingTimes()

#Dictionary for fancy naming
data.FancyNames("fancy.csv") #Load naming convention

# User inputs
data.UserOptions(opt_filename) #load user options

#User filters
data.UserFilters("filter.csv") #load user filters

#Organize all options
data.OrganizeOptions()

# Decide what to plot based on
# load user inner/outer loops for plotting - inner is within legend (each graph), outer
# Configure the figures to be plotted
fig = data.BuildFigures()

