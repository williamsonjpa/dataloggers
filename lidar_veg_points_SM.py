import pandas as pd
import numpy as np
from datetime import datetime

#adds simon mitchell's extracted LiDAR points

root=('C:/Users/hp/Documents/2018/Dataloggers/Data')

def processLidar(infile,outfile):
	df=pd.read_csv(infile)  #this code just changes some weird point codes in lidar data
	for i in df.index:
		x=df.loc[i,'ID']
		if x[-4:-2]=='PC':
			df.loc[i,'ID']=x[:-5]+'-'+x[-2:]
	df.to_csv(outfile)

processLidar(root+'/Vegetation/Simon Mitchell Points LiDAR extraction_scale_20SAFE.csv',root+'/Final/lidar.csv')

def combineDatasets(vegplotdata,lidar,dataloggers,allpoints,outfile):
	###
	###
	### NEED TO INSERT A FUNCTION HERE TO AVERAGE THE DATALOGGER DATA TO POINTS PRE-MATCHING!
	###
	###

	lidar=pd.read_csv(lidar)
	veg=pd.read_csv(vegplotdata)
	data=pd.read_csv(dataloggers)
	xl=pd.ExcelFile(allpoints)
	widths=xl.parse('SAFEPoints.txt')

	lidarHeaders=lidar.columns[3:] #extract headers of veg and lidar variables
	vegHeaders=veg.columns[2:]

	for i in lidarHeaders: #create new columns in dataframe with lidar variables
		data[i]=''

	for i in vegHeaders: #create new columns in dataframe with veg variables
		data[i]=''

	print('Creating column of river points to match against lidar data.')
	#makes a column to match up the logger data to veg and lidar data with
	for i in data.index:
		if str(data.loc[i,'Point'])!='10':
			data.loc[i,'RiverPointCode']=data.loc[i,'River'].upper()+'-0'+str(data.loc[i,'Point'])
		else:
			data.loc[i,'RiverPointCode']=data.loc[i,'River'].upper()+'-'+str(data.loc[i,'Point'])


	print('Search through lidar database matching sites and appending lidar data.')
	for i in lidar.index: 
	 #searches through the lidar database for matching sites and appends lidar data to dataloggers data
		for j in data.index:
			if lidar.loc[i,'ID']==data.loc[j,'RiverPointCode']:
				for k in lidarHeaders:
					data.loc[j,k]=lidar.loc[i,k]

	print('Search through vegplot database matching sites and appending lidar data.')
	for i in veg.index: #searches through the lidar database for matching sites and appends veg data to dataloggers data
		for j in data.index:
			if veg.loc[i,'Plot #']==data.loc[j,'RiverPointCode']:
				for k in vegHeaders:
					data.loc[j,k]=veg.loc[i,k]

	'''
	Generate landuse bins for plotting purposes and generate distances from the buffer edge and river for each file
	'''

	data=append_site_data(data,widths)


	data.to_csv(outfile, sep=',')
	print('Saved as /Final/Combined_Point.csv')

def append_site_data(infile,allpoints):
	'''
	add columns to each logger file with the buffer width and the gps elevation for the point
	'''
	#read in the widths data and the infile
	data=infile
	widths=allpoints

	#generate code for each line of the width file to match against the logger files
	for i in widths.index:
		if str(widths.loc[i,'name'])[:3]=='SJI':
			widths.loc[i,'name']=str(widths.loc[i,'name'])[:4]+'-'+str(widths.loc[i,'name'])[-2:]

		#rr12 and rr14 are just down as r12 and r14 in the width file for some reason
		elif str(widths.loc[i,'name'])[:3]=='R12' or str(widths.loc[i,'name'])[:3]=='R14':
			widths.loc[i,'name']='R'+str(widths.loc[i,'name'][:3])+'-'+str(widths.loc[i,'name'])[-2:]
		elif str(widths.loc[i,'name'])[:2]=='RR':
			if str(widths.loc[i,'name'])[3]==' ':
				widths.loc[i,'name']=str(widths.loc[i,'name'])[:3]+'-'+str(widths.loc[i,'name'])[-2:]
			elif str(widths.loc[i,'name'])[4]==' ':
				widths.loc[i,'name']=str(widths.loc[i,'name'])[:4]+'-'+str(widths.loc[i,'name'])[-2:]
		#if not a riparian buffer, do not create a name to match
		else:
			pass

	#match up the width and elevation to the logger file, if no match found still create column but empty
	x=0
	for i in widths.index:
		if x==0:
			if widths.loc[i,'name']==data.loc[0,'RiverPointCode']:
				data.loc['width']=widths.loc[i,'width']
				data.loc['GPS_ele']=widths.loc[i,'GPS_ele']
				x=1
	if x==0:
		data['width']=''
		data['GPS_ele']=''

	#return the dataframe to feed into next function
	return data


combineDatasets(root+'/Final/vegplotData.csv',root+'/Final/lidar.csv',
	root+'/Final/pointData.csv',root+'/Vegetation/allpoints.xlsx',root+'/Final/Combined_Point.csv')