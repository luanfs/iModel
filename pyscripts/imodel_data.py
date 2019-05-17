#! /usr/bin/env python3
#
#
#   Given data (x,y), add line plot to graph
#
#
#   Pedro Peixoto <ppeixoto@usp.br>
#
#
#---------------------------------------------------

import os
import sys
import stat
import math
import csv
import numpy as np
import string
import re 
import json

#For data structuring
import itertools



class imodelData(object):
	def __init__(self, input_filename):
		self.infile=input_filename

		#Get header
		lines = open(input_filename).readlines()
		self.datahead = lines[0].split()
		self.ncol=len(self.datahead)
		
		#Check first line to get types
		line1 = lines[1].split()
		if len(line1)!=self.ncol:
			print("Table data not matching with header")
			sys.exit(1)

		datatypes = []
		datastr = []
		datanum = []
		for i, x in enumerate(line1):
			#print(x)
			try:
				float(x)
				datatypes.append('f16')	
				datanum.append(self.datahead[i])
			except ValueError:
				datatypes.append('U60')
				datastr.append(self.datahead[i])
			
		#Get data
		self.data = np.genfromtxt(input_filename, skip_header=1, dtype=datatypes, autostrip=True, names=self.datahead)

		self.datastr = datastr #String data header
		self.datanum = datanum #Numeric data header

		print("Data with strings")
		print(datastr)
		print()
		print("Data with numbers")
		print(datanum)
		print(	)
		self.GetOptions()

	def FancyNames(self, filename):	
		self.fancynames = {}
		with open(filename, mode='r') as infile:
			reader = csv.reader(infile)
			self.fancynames = {rows[0]:rows[1] for rows in reader}

	def GetOptions(self):
		#Check option in string variables
		print()
		print("String options to filter")
		d = {}
		for x in self.datastr:
			print(x)
			y=self.data[x]
			if x=='Grid': #Remove numbers from grid names
				y= [ i.rstrip(string.digits).replace('_', '') for i in y]
			y=sorted(set(y))
			print(y)
			d[x]=y
		print()
		print("Numerics options to filter")
		for x in self.datanum:
			
			y=self.data[x]
			y=sorted(set(y))
			if all( i==int(i) for i in y): #ignore floats
				print(x)
				d[x]=y
				print(y)	
			
		self.varoptions=d
		return

	def UserOptions(self, filename):	
		with open(filename, mode='r') as infile:
			reader = csv.reader(infile)
			#for row in reader:
			#	self.filter[row[0]]=row[1]
			userdata = list(reader)
			n=len(userdata)
			for i in range(n):
				if userdata[i][0] in self.varoptions.keys():
					#This option exists!
					if userdata[i][1] != "all":
						self.varoptions[userdata[i][0]]=userdata[i][1:]
				else: #This is new options of loop/var option
					self.varoptions[userdata[i][0]]=userdata[i][1:]

	def ConfigFigures(self, input_filename):

		outloop = []
		for xout in self.varoptions["OutLoop"]:
			outloop.append(self.varoptions[xout])

		outeroptions=list(itertools.product(*outloop))
		#print(outeroptions)

		self.figures = []
		for op in outeroptions:
			self.figures.append(Figure(op, self.varoptions["OutLoop"], self))
		print('Created figure layouts')
		for fig in self.figures:
			print(fig.param)
			for yvar in self.varoptions["MidLoop"]:
				print(yvar)
				fig.addpanel(yvar, self)
			
	
class Figure(object):
	panels = []
	def __init__(self, param, names, data):
		label=""
		title=""
		for i, xout in enumerate(names):
			label=label+xout+str(int(param[i]))+"_"
			title=title+xout+" "+str(int(param[i]))+" "
		self.label=label
		self.param = {}
		for i, name in enumerate(names):
			self.param[name]=param[i]
		self.filename=data.infile

	def addpanel(self, yvar, data):
		self.panels.append(Panel(yvar, self.param, data))

class Panel(object):
	def __init__(self, yvar, param, data):
		self.xvar=data.varoptions['xVar'][0]
		self.yvar=yvar
		print(self.xvar, self.yvar)
		self.x = []
		self.y = []
		for i, val in enumerate(data.data[yvar]):
			print(i)
			for figopt in param.keys():
				print(figopt)
				if data.data[figopt][i] != param[figopt]:
					print('skip this line', data.data[figopt][i])
					break
			print('added this line' )
			self.x.append(data.data[self.xvar][i])
			self.y.append(val)
		print(self.x,self.y)
			#or varop in data.varoptions['InLoop']:
			#	print(varop, fig.param.keys())
			#	if varop in fig.param.keys():
			#		print(varop, data.data[varop][i], fig.param[varop])
			#		if data.data[varop][i] != fig.param[varop] :
			#			print(i, val, data.data[self.xvar][i], val)
				#if field[i] == f and methods[i] == mtd and gridnames[i] == grd:
				#	x.append(gridres[i])
				#		ymax.append(maxerrors[i])
				#
				#figure.plot( 0, x, ymax, label=name, i=c)
				#figure.plot( 1, x, yrms, label=name, i=c)
				#c = c + 1
				
				#plt.show()