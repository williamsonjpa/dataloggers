import pandas as pd
import numpy as np
import openpyxl

root=('C:/Users/hp/Documents/Leeches/')

def summarise_and_combine_leech_mammal_dataframes(leech_infile,mammal_abundance,mammal_trap_effort,outfile):
	'''
	Takes the leech data and pools data by site. 
	Sums leeches found of each species, both species and sampling effort.
	Merges the two data frames (keeping 1 line per sampling site and years in separate cols)
	Takes the mammal data, summarises it and appends it as columns to the leech data set
	Saves as oufile
	'''

	#### load in the datasheets required
	xl=pd.ExcelFile(leech_infile)
	leech2015=xl.parse('2015') #leech 2015 data

	xl=pd.ExcelFile(leech_infile)
	leech2016=xl.parse('2016') # leech 2016 data 

	xl=pd.ExcelFile(mammal_abundance)
	mammal=xl.parse('MammalsONLY') # mammal data imported as mammal 

	mammal_effort=pd.read_csv(mammal_trap_effort)

	#combine the 2015 and 2016 into one datasheet with separate species counts
	leech_combined=generate_summary_leech_data(leech2015,leech2016)

	#add on mammal trapping effort
	mammal=add_mammal_trap_nights(mammal,mammal_effort)

	#pool the mammal samples into fragments
	mammal_summary=summarise_mammal_data(mammal)

	#combine the datasets
	leech_mammal_combined=combine_leech_mammal_dataframes(leech_combined,mammal_summary)

	#generate adjusted (by sampling effort) abundances of leech and mammal data 
	leech_mammal_combined=generate_leech_combined_summary_data(leech_mammal_combined)

	#save to the outfile location 
	leech_mammal_combined.to_csv(outfile)

def generate_summary_leech_data(leech2015,leech2016):
	'''
	generates total leech counts by species for each year
	combines into one df 'leech_combined'
	'''

	#keep the Site variable (e.g. A,B,LFE,VJR)
	Site=leech2015.groupby('hectare')[['site']].first()

	#get 2015 leech summary for each species
	TotalB15=leech2015.groupby('hectare')[['TOTAL.B15']].sum()	
	TotalT15=leech2015.groupby('hectare')[['TOTAL.T15']].sum()
	SamplingEffort15=leech2015.groupby('hectare')[['TOTAL.EFF']].sum()

	#get 2015 tiger summary for each species
	TotalB16=leech2016.groupby('hectare')[['TOTAL.B16']].sum()	
	TotalT16=leech2016.groupby('hectare')[['TOTAL.T16']].sum()
	SamplingEffort16=leech2016.groupby('hectare')[['TOTAL.EFF']].sum()

	#create new df for summary info 
	leech_combined=pd.DataFrame(Site)
	leech_combined.columns=['Site']

	#add sampling information to df
	leech_combined['TotalB15']=TotalB15
	leech_combined['TotalT15']=TotalT15
	leech_combined['SamplingEffort15']=SamplingEffort15
	leech_combined['TotalB16']=TotalB16
	leech_combined['TotalT16']=TotalT16
	leech_combined['SamplingEffort16']=SamplingEffort16

	return leech_combined

def add_mammal_trap_nights(abundance,effort):
	'''
	appends mammal trapping hours and days onto the end of the combined leech_mammal df
	'''
	#make the site ID column matchable to hectare column in mammal abundance
	for i in effort.index:
		effort.loc[i,'Site_ID']=effort.loc[i,'Site_ID'][3:]

	#add CTN and CTH to abundance
	for i in abundance.index:
		for j in effort.index:
			if abundance.loc[i,'Site']==effort.loc[j,'Site_ID']:
				abundance.loc[i,'CTNs']=effort.loc[j,'CTNs']
				abundance.loc[i,'CTHs']=effort.loc[j,'CTHs']

	return abundance

def summarise_mammal_data(mammal):
	'''
	pools the mammal data by fragment using the hectareMATCH column
	'''
	#generate list of mammal species from elephant onwards 
	mammal_columns=mammal.columns
	mammal_columns=mammal_columns.tolist()
	mammal_species=mammal_columns[3:]

	#generate sums of each species per plot
	mammal_summary=mammal.groupby('hectareMATCH')[mammal_species].sum()

	return mammal_summary

def combine_leech_mammal_dataframes(leech,mammal):
	'''
	uses the site codes to combine the datasets into one dataframe with each fragment being one row
	'''

	#generate species list
	mammal_species=mammal.columns.tolist()

	for i in leech.index:
		for j in mammal.index:
			if i==j: # if the site codes match up
				for k in mammal_species: #iterate down list of mammal species
					leech.loc[i,k]=mammal.loc[j,k]#add mammal data to leech df
					
		else:
			pass
	
	leech.dropna(inplace=True)

	combined=leech

	return combined


def generate_leech_combined_summary_data(leech):
	for i in leech.index:
		if leech.loc[i,'SamplingEffort15']!=0:
			leech.loc[i,'TotalB15.Adjusted']=leech.loc[i,'TotalB15']/leech.loc[i,'SamplingEffort15']
		else:
			leech.loc[i,'TotalB15.Adjusted']=leech.loc[i,'TotalB15']
		
		if leech.loc[i,'SamplingEffort15']!=0:
			leech.loc[i,'TotalT15.Adjusted']=leech.loc[i,'TotalT15']/leech.loc[i,'SamplingEffort15']
		else:
			leech.loc[i,'TotalT15.Adjusted']=leech.loc[i,'TotalT15']

		if leech.loc[i,'SamplingEffort16']!=0:
			leech.loc[i,'TotalB16.Adjusted']=leech.loc[i,'TotalB16']/leech.loc[i,'SamplingEffort16']
		else:
			leech.loc[i,'TotalB16.Adjusted']=leech.loc[i,'TotalB16']
		
		if leech.loc[i,'SamplingEffort16']!=0:
			leech.loc[i,'TotalT16.Adjusted']=leech.loc[i,'TotalT16']/leech.loc[i,'SamplingEffort16']
		else:
			leech.loc[i,'TotalT16.Adjusted']=leech.loc[i,'TotalT16']

		leech.loc[i,'TotalBT15.Adjusted']=leech.loc[i,'TotalB15.Adjusted']+leech.loc[i,'TotalT15.Adjusted']
		leech.loc[i,'TotalBT16.Adjusted']=leech.loc[i,'TotalB16.Adjusted']+leech.loc[i,'TotalT16.Adjusted']



	mammal_species=leech.columns[7:-8].tolist()

	for i in mammal_species:
		for j in leech.index:
			species_adjusted_name=i+'.AdjustedHours'
			if leech.loc[j,i]!='NA':
				leech.loc[j,species_adjusted_name]=leech.loc[j,i]/leech.loc[j,'CTHs']

	for i in leech.index:
		leech.loc[i,'Total.Mammal.Abundance.Adjusted.Hours']=leech.loc[i,leech.columns[59:].tolist()].sum()

	for i in leech.index:
		leech.loc[i,'Total.Mammal.Abundance.Adjusted.Hours.NOPIG']=leech.loc[i,'Total.Mammal.Abundance.Adjusted.Hours']-leech.loc[i,'Bearded Pig.AdjustedHours']


	return leech

summarise_and_combine_leech_mammal_dataframes(root+'LeechAbundance.xlsx',\
	root+'MammalAbundance.xlsx',root+'MammalTrapEffort.csv',root+'Mammal_Leech_Combined.csv')
