###This code is designed to pull daily max, min and means out of the temperatures and also the humidity and dew points###

from __future__ import print_function
import csv
import os
import ntpath
import pandas as pd
import math
import numpy as np


root=('C:/Users/hp/Documents/2018/Dataloggers/Data') 

def VegPlotData(infile,outfile):
	df = pd.read_csv(infile)
	print('Dataframe loaded.')
	meanDBH=df.groupby('Plot #')[['DBH (cm)']].mean()
	minDBH=df.groupby('Plot #')[['DBH (cm)']].min()
	maxDBH=df.groupby('Plot #')[['DBH (cm)']].max()
	varDBH=df.groupby('Plot #')[['DBH (cm)']].var()

	summaryDF=meanDBH #new dataframe
	summaryDF.columns=['meanDBH(cm)'] #change column header to be correct
	summaryDF['minDBH(cm)']=minDBH
	summaryDF['maxDBH(cm)']=maxDBH
	summaryDF['varDBH(cm)']=varDBH

	meanPOM=df.groupby('Plot #')[['POM (m)']].mean()
	minPOM=df.groupby('Plot #')[['POM (m)']].min()
	maxPOM=df.groupby('Plot #')[['POM (m)']].max()
	varPOM=df.groupby('Plot #')[['POM (m)']].var()

	summaryDF['meanPOM(m)']=meanPOM
	summaryDF['minPOM(m)']=minPOM
	summaryDF['maxPOM(m)']=maxPOM
	summaryDF['varPOM(m)']=varPOM


	def treeHeight(distance,angle,eyeheight):
		height=distance*np.tan((np.deg2rad(angle)))-eyeheight
		return height


	df['Height(m)']=treeHeight(df['Distance (m)'],df['Angle (degrees)'],df['Eye height (m)']/100)

	meanHeight=df.groupby('Plot #')[['Height(m)']].mean()
	minHeight=df.groupby('Plot #')[['Height(m)']].min()
	maxHeight=df.groupby('Plot #')[['Height(m)']].max()
	varHeight=df.groupby('Plot #')[['Height(m)']].var()

	summaryDF['meanHeight(m)']=meanHeight
	summaryDF['minHeight(m)']=minHeight
	summaryDF['maxHeight(m)']=maxHeight
	summaryDF['varHeight(m)']=varHeight


	meanClimberlow=df.groupby('Plot #')[['Climber (lower)']].mean()
	minClimberlow=df.groupby('Plot #')[['Climber (lower)']].min()
	maxClimberlow=df.groupby('Plot #')[['Climber (lower)']].max()
	varClimberlow=df.groupby('Plot #')[['Climber (lower)']].var()

	summaryDF['meanClimber(lower)']=meanClimberlow
	summaryDF['minClimber(lower)']=minClimberlow
	summaryDF['maxClimber(lower)']=maxClimberlow
	summaryDF['varClimber(lower)']=varClimberlow


	meanClimberup=df.groupby('Plot #')[['Climber (upper)']].mean()
	minClimberup=df.groupby('Plot #')[['Climber (upper)']].min()
	maxClimberup=df.groupby('Plot #')[['Climber (upper)']].max()
	varClimberup=df.groupby('Plot #')[['Climber (upper)']].var()

	summaryDF['meanClimber(upper)']=meanClimberup
	summaryDF['minClimber(upper)']=minClimberup
	summaryDF['maxClimber(upper)']=maxClimberup
	summaryDF['varClimber(upper)']=varClimberup


	medianEpi=df.groupby('Plot #')[['Epiphyte score']].median()
	minEpi=df.groupby('Plot #')[['Epiphyte score']].min()
	maxEpi=df.groupby('Plot #')[['Epiphyte score']].max()

	summaryDF['medianEpiphyteScore']=medianEpi
	summaryDF['minEpiphyteScore']=minEpi
	summaryDF['maxEpiphyteScore']=maxEpi


	medianFruit=df.groupby('Plot #')[['Fruiting score']].median()
	minFruit=df.groupby('Plot #')[['Fruiting score']].min()
	maxFruit=df.groupby('Plot #')[['Fruiting score']].max()

	summaryDF['medianFruitingScore']=medianFruit
	summaryDF['minFruitingScore']=minFruit
	summaryDF['maxFruitingScore']=maxFruit


	medianFlower=df.groupby('Plot #')[['Flowering score']].median()
	minFlower=df.groupby('Plot #')[['Flowering score']].min()
	maxFlower=df.groupby('Plot #')[['Flowering score']].max()

	summaryDF['medianFloweringScore']=medianFlower
	summaryDF['minFloweringScore']=minFlower
	summaryDF['maxFloweringScore']=maxFlower


	medianCrown=df.groupby('Plot #')[['Crown illumination']].median()
	minCrown=df.groupby('Plot #')[['Crown illumination']].min()
	maxCrown=df.groupby('Plot #')[['Crown illumination']].max()

	summaryDF['medianFloweringScore']=medianCrown
	summaryDF['minFloweringScore']=minCrown
	summaryDF['maxFloweringScore']=maxCrown


	meanBat=df.groupby('Plot #')[['Bat cavities']].mean()
	minBat=df.groupby('Plot #')[['Bat cavities']].min()
	maxBat=df.groupby('Plot #')[['Bat cavities']].max()
	varBat=df.groupby('Plot #')[['Bat cavities']].var()

	summaryDF['meanBatCavities']=meanBat
	summaryDF['minBatCavities']=minBat
	summaryDF['maxBatCavities']=maxBat
	summaryDF['varBatCavities']=varBat


	meanTreeCover=df.groupby('Plot #')[['% cover trees']].mean()
	summaryDF['TreeCover%']=meanTreeCover
	meanGinCover=df.groupby('Plot #')[['% cover ginger']].mean()
	summaryDF['GingerCover%']=meanGinCover
	meanShrubCover=df.groupby('Plot #')[['% cover shrub']].mean()
	summaryDF['ShrubCover%']=meanShrubCover
	meanLianaCover=df.groupby('Plot #')[['% cover lianas']].mean()
	summaryDF['LianasCover%']=meanLianaCover
	meanFernCover=df.groupby('Plot #')[['% cover fern']].mean()
	summaryDF['FernCover%']=meanFernCover
	meanGrassCover=df.groupby('Plot #')[['% cover grass']].mean()
	summaryDF['GrassCover%']=meanGrassCover
	meanOtherCover=df.groupby('Plot #')[['% cover other']].mean()
	summaryDF['OtherCover%']=meanOtherCover
	SpecificOtherCover=df.groupby('Plot #')[['Details of other']].first()
	summaryDF['SpecificOtherCover']=SpecificOtherCover

	longitude=df.groupby('Plot #')[['Longitude (Eastings)']].first()
	summaryDF['VegPlotLongitude(Eastings)']=longitude

	latitude=df.groupby('Plot #')[['Latitude (Northings)']].first()
	summaryDF['VegPlotLatitude(Northings)']=latitude


	summaryDF.reset_index(inplace=True)

	for i in summaryDF.index: #change the plot code to match the lidar and datalogger coding system
		summaryDF.loc[i,'Plot #']=str(summaryDF.loc[i,'Plot #'][:-1])+'0'+str(summaryDF.loc[i,'Plot #'][-1])


	print('Summary statistics generated.')
	summaryDF.to_csv(outfile, sep=',')
	print('File saved as Data/Final/vegplotData.csv')


VegPlotData(root+'/Vegetation/VegetationCSV.csv',root+'/Final/vegplotData.csv')
