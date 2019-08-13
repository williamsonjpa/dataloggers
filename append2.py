import os
import glob
import os.path
import pandas as pd
import numpy as np

def iterate_append(root,site_data,veg,lidar):
	'''
	iterate append2 script over files in added info directory
	'''

	indirectory = root + '/Data/Edited'
	outdirectory = root + '/Data/Appended'

	###clear out the folder where the edited files are going to be produced
	clear_directory(outdirectory,'.csv')

	infilelist = glob.glob(os.path.join(indirectory, "*.csv"))
	filenumber = 0

	for f in infilelist:
		file = f.split('/')[-1]
		data = append_site_data(f,site_data)
		outfile = generate_distance_data(data)
		# outfile=append_veg_and_lidar(outfile,veg,lidar)
		outfile.to_csv(outdirectory + '/' + file)
	   
		#only prints the progess message every 10th file or for the last file
		filenumber += 1
		infile_length = len(infilelist)
		if str(filenumber)[-1] == '0' or filenumber == infile_length:
			print('Appended ' + str(filenumber) + ' of ' + str(infile_length) + ' files!')


def clear_directory(directory,extension):
	for dirpath, dirnames, files in os.walk(directory):
		for name in files:
			if name.lower().endswith(extension):
				os.remove(os.path.join(dirpath, name))

def append_site_data(infile,allpoints):
	'''
	add columns to each logger file with the buffer width and the gps elevation for the point
	'''
	#read in the widths data and the infile
	data = pd.read_csv(infile)
	xl = pd.ExcelFile(allpoints)
	widths = xl.parse('SAFEPoints.txt')


	#generate code for each logger file to match against width dataframe
	if str(data.loc[0,'Point'])!='10':
		data['RiverPointCode']=data.loc[0,'River'].upper()+'-0'+str(data.loc[0,'Point'])
	else:
		data['RiverPointCode']=data.loc[0,'River'].upper()+'-'+str(data.loc[0,'Point'])

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
	x = 0
	for i in widths.index:
		if x == 0:
			if widths.loc[i,'name'] == data.loc[0,'RiverPointCode']:
				data['width'] = widths.loc[i,'width']
				data['GPS_ele'] = widths.loc[i,'GPS_ele']
				x = 1
	if x == 0:
		data['width'] = ''
		data['GPS_ele'] = ''

	#return the dataframe to feed into next function
	return data


def generate_distance_data(infile):
	'''
	Generate landuse bins for plotting purposes and generate distances from the buffer edge and river for each file
	'''
	data=infile
	#create empty distance columns for OP and CF that will not have matches. 
	data['Distance_from_edge']=''
	data['Distance_from_river']=''

	if data.loc[0, 'Position']=='buffer5m':
		if data.loc[0,'width']!='':
			if data.loc[0,'width']>=5:
				data['Distance_from_edge']=data.loc[0,'width']-5
				data['Distance_from_river']=5
			else:
				data['LandUse']='OP'

	elif data.loc[0,'Position']=='buffer15m':
		if data.loc[0,'width']!='':
			if data.loc[0,'width']>=15:
				data['Distance_from_edge']=data.loc[0,'width']-15
				data['Distance_from_river']=15
			else:
				data['LandUse']='OP'

	elif data.loc[0,'Position']=='bufferedge':
		if data.loc[0,'width']!='':
			if data.loc[0,'width']>=25: #if more than 5m from previous logger
				data['Distance_from_edge']=5
				data['Distance_from_river']=(data.loc[0,'width'])-5
			elif data.loc[0,'width']>=20: #otherwise if not more than 5m from logger
				data['Distance_from_edge']=5
				data['Distance_from_river']=(data.loc[0,'width'])
				data['LandUse']='?'
			else:
				data['LandUse']='OP'


	if data.loc[0,'River']=='ROP2' or data.loc[0,'River']=='ROP10':
				data['LandUseBins']='RR=0'
	elif data.loc[0,'LandUse']!='RR':
		data['LandUseBins']=data.loc[0,'LandUse']


	elif data.loc[0,'width']!='' and data.loc[0,'Distance_from_edge']!='' and data.loc[0,'Distance_from_river']!='':
		if data.loc[0, 'Distance_from_edge']<30:
			data['LandUseBins']='RR<30m'
		elif data.loc[0,'Distance_from_edge']<60:
			data['LandUseBins']='RR<60m'
		elif data.loc[0, 'Distance_from_edge']<90:
			data['LandUseBins']='RR<90m'
		elif data.loc[0, 'Distance_from_edge']>=90:
			data['LandUseBins']='RR90m+'

	else:
		data['LandUseBins']='RR_UnknownWidth'

	return data


def append_veg_and_lidar(infile,vegplotdata,lidar):
	'''
	matches any existing lidar and vegetation data to the infile
	'''

	lidar=pd.read_csv(lidar)
	veg=pd.read_csv(vegplotdata)
	data=infile

	lidarHeaders=lidar.columns[3:] #extract headers of veg and lidar variables
	vegHeaders=veg.columns[2:]

	for i in lidarHeaders: #create new columns in dataframe with lidar variables
		data[i]=''

	for i in vegHeaders: #create new columns in dataframe with veg variables
		data[i]=''

	for i in lidar.index: 
	 #searches through the lidar database for matching sites and appends lidar data to dataloggers data
		if lidar.loc[i,'ID']==data.loc[0,'RiverPointCode']:
			for k in lidarHeaders:
				data.loc[k]=lidar.loc[i,k]

	for i in veg.index: #searches through the lidar database for matching sites and appends veg data to dataloggers data
		if veg.loc[i,'Plot #']==data.loc[0,'RiverPointCode']:
			for k in vegHeaders:
				data.loc[k]=veg.loc[i,k]

	return data
# iterate_append(root+'/Data/Edited',root+'/Data/Appended',root+'/Data/Vegetation/allpoints.xlsx',root+'/Final/vegplotData.csv',root+'/Final/lidar.csv')

