import pandas as pd
import math

def iterate_VPD_script(infile,outfile):

	df=pd.read_csv(infile)

	for i in df.index:
		if df.loc[i,'Humidity(%rh)']>100:
			df.loc[i,'Humidity(%rh)']=100
		if str(str(i)[-3:])=='000':
			print(str(i)+' out of '+str(len(df.index))+' lines processed.')

	df.to_csv(outfile)

	for i in df.index:
		df.loc[i,'VPD'] = convert_RH_to_VPD(df.loc[i,'Celsius(C)'],df.loc[i,'Humidity(%rh)'])
		if str(str(i)[-3:]) == '000' or str(i) == str(len(df.index)):
			print(str(i) + ' out of ' + str(len(df.index)) + ' humidities converted to VPD.')

	df.to_csv(outfile)

def convert_RH_to_VPD(Temp,RH):

	# VPD=((100-RH)/100)*6.112*math.exp((17.67*Temp)/(Temp+243.5))
	VPD=((100-RH)/100)*6.112*math.exp((17.67*Temp)/(Temp+243.5))

	return VPD

