import pandas as pd
import math

root=('C:/Users/hp/Documents/2018/Dataloggers/Data')

def append_width_and_elevation_data(infile,allpoints,outfile):

	data=pd.read_csv(infile)
	xl=pd.ExcelFile(allpoints)
	widths=xl.parse('SAFEPoints.txt')

	for i in data.index:
		if str(data.loc[i,'Point'])!='10':
			data.loc[i,'RiverPointCode']=data.loc[i,'River'].upper()+'-0'+str(data.loc[i,'Point'])
		else:
			data.loc[i,'RiverPointCode']=data.loc[i,'River'].upper()+'-'+str(data.loc[i,'Point'])
		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(data.index))+' riverpointcodes processed.')
			

	print('Creating column of river points in allpoints data to match buffer widths and elevation to.')
	for i in widths.index:
		if str(widths.loc[i,'name'])[:3]=='SJI':
			widths.loc[i,'name']=str(widths.loc[i,'name'])[:4]+'-'+str(widths.loc[i,'name'])[-2:]
		elif str(widths.loc[i,'name'])[:3]=='R12' or str(widths.loc[i,'name'])[:3]=='R14':
			widths.loc[i,'name']='R'+str(widths.loc[i,'name'][:3])+'-'+str(widths.loc[i,'name'])[-2:]
		elif str(widths.loc[i,'name'])[:2]=='RR':
			if str(widths.loc[i,'name'])[3]==' ':
				widths.loc[i,'name']=str(widths.loc[i,'name'])[:3]+'-'+str(widths.loc[i,'name'])[-2:]
			elif str(widths.loc[i,'name'])[4]==' ':
				widths.loc[i,'name']=str(widths.loc[i,'name'])[:4]+'-'+str(widths.loc[i,'name'])[-2:]
		else:

			pass
		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(data.index))+' widthscodes processed.')
			

	print('Search through allpoints data and append the elevation and bufferwidth data.')
	widthsHeaders=['width','GPS_ele']
	for i in widths.index:
		for j in data.index:
			if widths.loc[i,'name']==data.loc[j,'RiverPointCode']:
				print(str(i)+' out of '+str(len(widths.index))+' matched.')
				for k in widthsHeaders:
					data.loc[j,k]=widths.loc[i,k]
		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(data.index))+' widths appended.')
			

	print('Change landuse to OP if outside of riparian buffer width. Remove buffer edge files if width <25.')
	for i in data.index:
		if data.loc[i, 'Position']=='buffer5m':
			if type(data.loc[i,'width'])==type(np.float64(1)) or type(data.loc[i,'width'])==type(np.float(1)) or type(data.loc[i,'width'])==type(np.int(1)) or type(data.loc[i,'width'])==type(np.int64(1)):
				if data.loc[i,'width']>=5:
					data.loc[i,'Distance_from_edge']=data.loc[i,'width']-5
					data.loc[i,'Distance_from_river']=5
				else:
					data.loc[i,'LandUse']='OP'
		elif data.loc[i,'Position']=='buffer15m':
			if type(data.loc[i,'width'])==type(np.float64(1)) or type(data.loc[i,'width'])==type(np.float(1)) or type(data.loc[i,'width'])==type(np.int(1)) or type(data.loc[i,'width'])==type(np.int64(1)):
				if data.loc[i,'width']>=15:
					data.loc[i,'Distance_from_edge']=data.loc[i,'width']-15
					data.loc[i,'Distance_from_river']=15
				else:
					data.loc[i,'LandUse']='OP'
		elif data.loc[i,'Position']=='bufferedge':
			if type(data.loc[i,'width'])==type(np.float64(1)) or type(data.loc[i,'width'])==type(np.float(1)) or type(data.loc[i,'width'])==type(np.int(1)) or type(data.loc[i,'width'])==type(np.int64(1)):
				if data.loc[i,'width']>=25: #if more than 5m from previous logger
					data.loc[i,'Distance_from_edge']=5
					data.loc[i,'Distance_from_river']=(data.loc[i,'width'])-5
				elif data.loc[i,'width']>=20: #otherwise if not more than 5m from logger
					data.loc[i,'Distance_from_edge']=5
					data.loc[i,'Distance_from_river']=(data.loc[i,'width'])
					data.loc[i,'LandUse']='?'
				else:
					data.loc[i,'LandUse']='OP'
		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(data.index))+' distances processed.')


	for i in data.index:
		if data.loc[i,'River']=='ROP2' or data.loc[i,'River']=='ROP2':
			if data.loc[i,'Position']=='op5m' or data.loc[i,'Position']=='op15m' or data.loc[i,'Position']=='op25m':
				data.loc[i,'LandUseBins']='RR=0'
		elif data.loc[i,'LandUse']!='RR':
			data.loc[i,'LandUseBins']=data.loc[i,'LandUse']


		else:
			if data.loc[i, 'Distance_from_edge']<20:
				data.loc[i,'LandUseBins']='RR<20m'
			elif data.loc[i, 'Distance_from_edge']<40:
				data.loc[i,'LandUseBins']='RR<40m'
			elif data.loc[i, 'Distance_from_edge']<80:
				data.loc[i,'LandUseBins']='RR<80m'
			elif data.loc[i, 'Distance_from_edge']>=80:
				data.loc[i,'LandUseBins']='RR80m+'

		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(data.index))+' widthbins processed.')

append_width_and_elevation_data(root+'/Final/merge2.csv',root+'/Vegetation/allpoints.xlsx',root+'/Final/merge2.csv')