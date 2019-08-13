import pandas as pd
import numpy as np
from datetime import datetime

#adds tom swinfield's extracted LiDAR points

root=('C:/Users/hp/Documents/2018/Dataloggers/Data')


def combineDatasets(vegplotdata,lidar_topo,lidar_PAI,lidar_tch,dataloggers,allpoints,outfile):
	'''
	combines the vegplot, lidar topography, lidar PAI and lidar tch datasets with the dailyData 
	(dailyData is summarised datalogger data by point and date)
	'''

	#open files
	topo=pd.read_csv(lidar_topo)
	PAI=pd.read_csv(lidar_PAI)
	tch=pd.read_csv(lidar_tch)
	veg=pd.read_csv(vegplotdata)
	data=pd.read_csv(dataloggers)
	xl=pd.ExcelFile(allpoints)
	widths=xl.parse('SAFEPoints.txt')

	#extract headers of veg and lidar variables
	topoHeaders=topo.columns[3:] 
	PAIHeaders=PAI.columns[3:]
	tchHeaders=tch.columns[3:]
	vegHeaders=veg.columns[2:]

	###change point codes in lidar files to have a 0 before the point number
	for i in topo.index:
		topo.loc[i,'Plot']=str(topo.loc[i,'Plot'].split('-')[0])+'-0'+str(topo.loc[i,'Plot'].split('-')[1])
	for i in PAI.index:
		PAI.loc[i,'Plot']=str(PAI.loc[i,'Plot'].split('-')[0])+'-0'+str(PAI.loc[i,'Plot'].split('-')[1])
	for i in topo.index:
		tch.loc[i,'Plot']=str(topo.loc[i,'Plot'].split('-')[0])+'-0'+str(tch.loc[i,'Plot'].split('-')[1])

	#create month number for GAM
	for i in data.index:
		data.loc[i,'month']=int(data.loc[i,'Date'].split('/')[1])
	#create year number for GAM
	for i in data.index:
		data.loc[i,'year']=int(data.loc[i,'Date'].split('/')[2])

	
	for i in data.index:
		data.loc[i,'Date2']=str(data.loc[i,'Date'])[:-4]+'2000'
		data.loc[i,'DateTime2']= datetime.strptime(data.loc[i,'Date2'],'%d/%m/%Y')
		data.loc[i,'date_minus_year']=str(data.loc[i,'DateTime2']-datetime.strptime('01/01/2000','%d/%m/%Y')).split(' ')[0]

	for i in topoHeaders: #create new columns in dataframe with lidar variables
		data[i]=''
	for i in PAIHeaders: #create new columns in dataframe with lidar variables
		data[i]=''
	for i in tchHeaders: #create new columns in dataframe with lidar variables
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


	print('Search through lidar databases matching sites and appending data.')
	for i in topo.index:
		for j in data.index:
			if topo.loc[i,'Plot']==data.loc[j,'RiverPointCode']:
				for k in topoHeaders:
					data.loc[j,k]=topo.loc[i,k]
	for i in PAI.index: 
		for j in data.index:
			if PAI.loc[i,'Plot']==data.loc[j,'RiverPointCode']:
				for k in PAIHeaders:
					data.loc[j,k]=PAI.loc[i,k]
	for i in tch.index: 
		for j in data.index:
			if tch.loc[i,'Plot']==data.loc[j,'RiverPointCode']:
				for k in tchHeaders:
					data.loc[j,k]=tch.loc[i,k]

	print('Search through vegplot database matching sites and appending data.')
	for i in veg.index: #searches through the lidar database for matching sites and appends veg data to dataloggers data
		for j in data.index:
			if veg.loc[i,'Plot #']==data.loc[j,'RiverPointCode']:
				for k in vegHeaders:
					data.loc[j,k]=veg.loc[i,k]

	'''
	Generate landuse bins for plotting purposes and generate distances from the buffer edge and river for each file
	'''

	data=append_site_data(data,widths)

	#create empty distance columns for OP and CF that will not have matches. 
	data['Distance_from_edge']=''
	data['Distance_from_river']=''

	for i in data.index:
		if data.loc[i, 'Position']=='buffer5m':
			if data.loc[i,'width']!='':
				if data.loc[i,'width']>=5:
					data.loc[i,'Distance_from_edge']=data.loc[i,'width']-5
					data.loc[i,'Distance_from_river']=5
				else:
					data.loc[i,'LandUse']='?'

		elif data.loc[i,'Position']=='buffer15m':
			if data.loc[i,'width']!='':
				if data.loc[i,'width']>=15:
					data.loc[i,'Distance_from_edge']=data.loc[i,'width']-15
					data.loc[i,'Distance_from_river']=15
				else:
					data.loc[i,'LandUse']='?'

		elif data.loc[i,'Position']=='bufferedge':
			if data.loc[i,'width']!='':
				if data.loc[i,'width']>=25: #if more than 5m from previous logger
					data.loc[i,'Distance_from_edge']=5
					data.loc[i,'Distance_from_river']=(data.loc[i,'width'])-5
				elif data.loc[i,'width']>=20: #otherwise if not more than 5m from logger
					data.loc[i,'Distance_from_edge']=5
					data.loc[i,'Distance_from_river']=(data.loc[i,'width'])
					data.loc[i,'LandUse']='?'
				else:
					data.loc[i,'LandUse']='?'


		if data.loc[i,'River']=='ROP2' or data.loc[i,'River']=='ROP10':
					data.loc[i,'LandUseBins']='RR=0'
		elif data.loc[i,'LandUse']!='RR':
			data.loc[i,'LandUseBins']=data.loc[i,'LandUse']


		elif data.loc[i,'width']!='' and data.loc[i,'Distance_from_edge']!='' and data.loc[i,'Distance_from_river']!='':
			if data.loc[i, 'Distance_from_edge']<30:
				data.loc[i,'LandUseBins']='RR<30m'
			elif data.loc[i,'Distance_from_edge']<60:
				data.loc[i,'LandUseBins']='RR<60m'
			elif data.loc[i, 'Distance_from_edge']<90:
				data.loc[i,'LandUseBins']='RR<90m'
			elif data.loc[i, 'Distance_from_edge']>=90:
				data.loc[i,'LandUseBins']='RR90m+'

		else:
			data.loc[i,'LandUseBins']='RR_UnknownWidth'


	data.to_csv(outfile, sep=',')

	print('Saved as /Final/Combined.csv')

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



combineDatasets(root+'/Final/vegplotData.csv',
	root+'/Final/Files_From_TS/SAFE/lidar_extraction_coords_JW_topo_scale_30.csv',
	root+'/Final/Files_From_TS/SAFE/lidar_extraction_coords_JW_scale_30.csv',
	root+'/Final/Files_From_TS/SAFE/lidar_extraction_coords_JW_tch_scale_30.csv',
	root+'/Final/DailyData.csv',
	root+'/Vegetation/allpoints.xlsx',
	root+'/Final/Combined.csv')