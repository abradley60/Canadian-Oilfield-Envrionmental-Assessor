import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import csv
import collections
import pylab
import re

def get_production_data():

	count = 0;
	file_location = "C:/Users/alexander.bradley/Google Drive/University of Calgary_/Masters Research/Western Canadian Tight Oil/Python/Production Analysis/All_Montney_Prod_Data.csv"
	date_location = []
	well_IDs = []
	production_data_headings = []
	well_data_headings = []

	switch = 0;
	m3tobbl = 6.28981;
	m3toscf = 35.315
	init = 0 # we will use this to get the headings for the well data

	production_data = collections.OrderedDict()
	well_header_data = collections.OrderedDict()

	remove_characters = ['/', '-', ' ']

	with open(file_location) as f:
		reader = csv.reader(f)
		for row in reader:
			
			if row[0] == 'Unique Well ID':
				switch = 0;
				well_ID = re.sub("|".join(remove_characters), "", row[1]) #stripping characters to be consistant with other files
				well_header_data[well_ID] = [row[1]]
				well_IDs.append(well_ID);
			
			if init == 0:
				well_data_headings.append(row[0])

			if switch == 0:
				well_header_data[well_ID].append(row[1])

			if switch == 1:
				try:
					production_data[well_ID].append(row)
				except:
					production_data[well_ID] = [row]

			if row[0] == 'Date':
				switch = 1
				init = 1
				production_data_headings = row 

			count = count + 1;
		
	#data example - last entry
	#print(production_data['100141503010W500'][-1])

	return production_data_headings, production_data, well_data_headings, well_header_data

#print(get_production_data()[0])

def production_data_summary(production_data_headings, production_data, production_well_data_headings, well_header_data, general_well_data_headings, general_well_data, OPGEE_data, OPGEE_headings):

	#get start and end date so we know how long it has produced
	

	for i in range(0,len(production_well_data_headings)):
		if production_well_data_headings[i] == 'Production Begin Date':
			start_date_index = i+1
		if production_well_data_headings[i] == 'Production End Date':
			end_date_index = i+1

	for well in well_header_data:
		start_date = well_header_data[well][start_date_index]
		OPGEE_headings[well].append(production_well_data_headings[start_date_index])
		OPGEE_data[well].append(start_date)
		end_date = well_header_data[well][end_date_index]
		OPGEE_headings[well].append(production_well_data_headings[end_date_index])
		OPGEE_data[well].append(end_date)


	#Cumulatives for each well 
	index_array = []

	for i in range(0, len(production_data_headings)):
		
		if production_data_headings[i] == 'PRD Cumulative GAS e3m3':
			cum_gas_index = i
			index_array.append(i)
		if production_data_headings[i] == 'PRD Cumulative OIL m3':
			cum_oil_index = i
			index_array.append(i)
		if production_data_headings[i] == 'PRD Cumulative WTR m3':
			cum_wtr_index = i
			index_array.append(i)
		if production_data_headings[i] == 'PRD Cumulative CND m3':
			cum_cnd_index = i
			index_array.append(i)
		if production_data_headings[i] == 'Date':
			date_index = i

	count = 0
	date_max = 2016 # this is the latest date in the range we are assessing for an LCA (eg end of 2016)
	wells_in_date = []

	for well in production_data:
			if len(production_data[well][-1]) < len(production_data_headings): #some have only a single date entry
				most_recent_data = production_data[well]
			else:
				most_recent_data = production_data[well][-1]
			for i in range(0,len(index_array)):
				try:
					OPGEE_data[well].append(float(most_recent_data[index_array[i]]))
					OPGEE_headings[well].append(production_data_headings[index_array[i]])
				except:
					OPGEE_data[well].append(most_recent_data[index_array[i]])
					OPGEE_headings[well].append(production_data_headings[index_array[i]])
			
			completion_year = well_header_data[well][start_date_index][0:4]
			try:
				if float(completion_year) <= date_max:
					wells_in_date.append(well)
			except:
				pass

	'''
	print('\n\n~~~~~~~~~~ Production Data Summary ~~~~~~~~~~\n')
	print('Maximum Date for Our Analysis: ' + str(date_max))
	print('Number of producing wells from start date to end date: ' + str(len(wells_in_date)))
	print('\n')


	#how many wells are producing in 2016-01, we want to compare this to wells connected to batteries
	
	for i in range(0, len(general_well_data_headings)):
		if general_well_data_headings[i] == 'Area':
			area_index = i

	for well in production_data:
		if len(production_data[well][-1]) < len(production_data_headings):
			if production_data[well][date_index] == '2016-01':
				if general_well_data[well][area_index] == 'AB':
					count = count + 1
		else:
			for i in range(0,len(production_data[well])):
				if production_data[well][i][date_index] == '2016-01':
					if general_well_data[well][area_index] == 'AB':
						count = count + 1
		 
	'''
	
	#print('AB wells producing in 2016-01: ' + str(count))

	return OPGEE_data, OPGEE_headings