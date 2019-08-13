import pandas as pd
import numpy as np
import openpyxl
import math

root=('C:/Users/hp/Documents/Leeches/')

def summarise_and_combine_leech_mammal_dataframes(leech_infile,leech_coordinates,leech_radius,\
	mammal_radius,lidar,mammal_abundance,mammal_trap_effort,outfile):
	'''
	Takes the leech data and pools data by site. 
	You can set the leech and mammal radius required for points to be merged. 
	'''

	#### load in the datasheets required
	xl=pd.ExcelFile(leech_infile)
	leech2015=xl.parse('2015') #leech 2015 data

	xl=pd.ExcelFile(leech_infile)
	leech2016=xl.parse('2016') # leech 2016 data 

	xl=pd.ExcelFile(mammal_abundance)
	mammal=xl.parse('MammalsONLY') # mammal data imported as mammal

	leech_coord=pd.read_csv(leech_coordinates) # read in leech coordinates

	effort=pd.read_csv(mammal_trap_effort)#read in mammal trapping effort

	lidar=pd.read_csv(lidar) # read in lidar dataset

	#generate groups to later merge close together leech points
	leech_merged=merge_leech_points(leech2015,leech2016,leech_coord,leech_radius,lidar)

	#merge the points fully and generate summary data
	leech_summary=generate_summary_leech_data(leech_merged)

	#adds mammal trapping effort and coordinates to the abundance data
	mammal=add_mammal_trap_nights(mammal,effort)

	#add in mammal data for close by points
	(leech_combined,mammal)=add_mammal_data(leech_summary,mammal,mammal_radius)

	leech_combined.to_csv(outfile)

	mammal.to_csv('C:/Users/hp/Documents/Leeches/MammalTest.csv')

	leech_summary.to_csv('C:/Users/hp/Documents/Leeches/LeechTest.csv')




def merge_leech_points(leech2015,leech2016,leech_coord,merge_radius,lidar):
	'''
	adds the 2016 data to the 2015 data frame
	creates a radius around eachpoint and merges leech points that are within that radius of eachother
	note these can daisy chain together 
	'''

	#combine the leech data
	leech2015['TOTAL.B16']=leech2016['TOTAL.B16']
	leech2015['TOTAL.T16']=leech2016['TOTAL.B16']
	leech2015['Effort15']=leech2015['TOTAL.EFF']
	leech2015['Effort16']=leech2016['TOTAL.EFF']

	leech=leech2015


	#the coordinates of the rivers in the abundance doc need formatting to add 0s e.g. R0-1 is R0-01
	for i in leech.index:
		if str(leech.loc[i,'second'])[:2]=='R0'or str(leech.loc[i,'second'])[:3]=='R30' or str(leech.loc[i,'second'])[:4]=='RLFE':
			if str(leech.loc[i,'second'][-1])!=str(0):
				leech.loc[i,'second']=leech.loc[i,'second'][:-1]+'0'+leech.loc[i,'second'][-1]

	#lets get the leech coordinates in 
	for i in leech.index:
		for j in leech_coord.index:
			if str(leech.loc[i,'second'])==str(leech_coord.loc[j,'SiteNum']):
				leech.loc[i,'Lat']=leech_coord.loc[j,'Lat']
				leech.loc[i,'Long']=leech_coord.loc[j,'Long']

	#a variable to track whether a point has already merged with another point
	leech['Merged']='No'

	##this pairs up the points
	for i in leech.index:
		if math.isnan(leech.loc[i,'Lat']) == False:
			for j in leech.index:
				if math.isnan(leech.loc[j,'Lat']) == False:
				#doesnt allow the same lines to match up 
					if i != j:
						x=(abs(leech.loc[i,'Lat']-leech.loc[j,'Lat'])**2+abs(leech.loc[i,'Long']-leech.loc[j,'Long'])**2)
						x=math.sqrt(x)
						if x*111111<merge_radius:
							#check to see if the row (i) has already been assigned to a group or is its own group
							if leech.loc[i,'Merged']=='No':
							#if this point has not been matched up before, group them together
								if leech.loc[j, 'Merged']=='No':
									leech.loc[i,'Merged']=i
									leech.loc[j,'Merged']=i
								#if this point has been matched up before, change i merged group to j merged group
								elif leech.loc[j,'Merged']!='No':
									leech.loc[i,'Merged']=leech.loc[j,'Merged']
							else:
								#if j hasnt been assigned a group yet
								if leech.loc[j, 'Merged']=='No':
									leech.loc[j,'Merged']=leech.loc[i,'Merged']
								#if j has been assigned a group and i has been assigned a group, 
								# overwrite all of j groups with i group
								elif leech.loc[j,'Merged']!='No':
									group_to_replace=leech.loc[j,'Merged']
									for k in leech.index:
										if leech.loc[k,'Merged']==group_to_replace:
											leech.loc[k,'Merged']=leech.loc[i,'Merged']

	for i in leech.index:
		for j in lidar.index:
			if str(leech.loc[i,'second'])==str(lidar.loc[j,'ID'][-3:]):
				leech.loc[i,'canopy_height_mean']=lidar.loc[j,'canopy_height_mean']
				leech.loc[i,'canopy_height_moran']=lidar.loc[j,'canopy_height_moran']
				leech.loc[i,'pai_mean']=lidar.loc[j,'pai_mean']

	return leech

def generate_summary_leech_data(leech):
	
	Site=leech.groupby('Merged')[['hectare']].first()

	#number of points merged
	Size=leech.groupby('Merged')[['hectare']].size()

	#get 2015 leech summary for each species
	TotalB15=leech.groupby('Merged')[['TOTAL.B15']].sum()	
	TotalT15=leech.groupby('Merged')[['TOTAL.T15']].sum()
	SamplingEffort15=leech.groupby('Merged')[['Effort15']].sum()

	#get 2015 tiger summary for each species
	TotalB16=leech.groupby('Merged')[['TOTAL.B16']].sum()	
	TotalT16=leech.groupby('Merged')[['TOTAL.T16']].sum()
	SamplingEffort16=leech.groupby('Merged')[['Effort16']].sum()

	#generate central latitude and longitude points
	MeanLat=leech.groupby('Merged')[['Lat']].mean()
	MeanLong=leech.groupby('Merged')[['Long']].mean()

	#lidar variables
	canopy_height_mean=leech.groupby('Merged')[['canopy_height_mean']].mean()
	canopy_height_moran=leech.groupby('Merged')[['canopy_height_moran']].mean()
	pai_mean=leech.groupby('Merged')[['pai_mean']].mean()


	#create new df for summary info 
	leech_summary=pd.DataFrame(Site)
	leech_summary.columns=['Site']

	#add sampling information to df
	leech_summary['TotalB15']=TotalB15
	leech_summary['TotalT15']=TotalT15
	leech_summary['Effort15']=SamplingEffort15
	leech_summary['TotalB16']=TotalB16
	leech_summary['TotalT16']=TotalT16
	leech_summary['Effort16']=SamplingEffort16
	leech_summary['MeanLat']=MeanLat
	leech_summary['MeanLong']=MeanLong
	leech_summary['Size']=Size
	leech_summary['canopy_height_mean']=canopy_height_mean
	leech_summary['canopy_height_moran']=canopy_height_moran
	leech_summary['pai_mean']=pai_mean


	#only keep groups with 3 or less points (no centres of plots)
	# leech_summary=leech_summary.loc[leech_summary['Size']<4]

	return leech_summary

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
				abundance.loc[i,'Lat']=effort.loc[j,'Latitude']
				abundance.loc[i,'Long']=effort.loc[j,'Longitude']

	return abundance

def add_mammal_data(leech,mammal,mammal_radius):

	#generate list of mammal names and the trapping efforts
	mammal_list=mammal.columns[3:-2]

	#generate a variable to check if the mammal point has been matched with a leech point yet
	mammal['Match']='No'
	mammal['DuplicateMatch']='No'

	##this finds mammal points to append to leech groups
	for i in mammal.index:
		for j in leech.index:
			x=(abs(leech.loc[j,'MeanLat']-mammal.loc[i,'Lat'])**2+\
				abs(leech.loc[j,'MeanLong']-mammal.loc[i,'Long'])**2)
			x=math.sqrt(x)
			if x*111111<mammal_radius:
				#if not already match up
				if mammal.loc[i,'Match']=='No':
					mammal.loc[i,'Match']=j
				#if already matched record in the duplicate match column
				else:
					mammal.loc[i,'DuplicateMatch']='Yes'

	###this takes the mammal matches and puts them into the leech dataframe
	mammal_summary=mammal.groupby('Match')[mammal_list].sum()
	for i in mammal_summary.index:
		for j in leech.index:
			if j == i:
				for k in mammal_list:
					leech.loc[j, k]=mammal_summary.loc[i,k]

	leech.dropna(inplace=True)

	return (leech,mammal)


summarise_and_combine_leech_mammal_dataframes(root+'LeechAbundance.xlsx',root+'LeechCoord.csv',170,250,\
	root+'LiDAR.csv',root+'MammalAbundance.xlsx',root+'MammalTrapEffort.csv',root+'Mammal_Leech_Combined.csv')