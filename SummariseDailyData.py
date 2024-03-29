###This code is designed to pull daily max, min and means out of the temperatures and also the humidity and dew points###

from __future__ import print_function
import csv
import os
import ntpath
import pandas as pd

def dailySummaryData(infile,outfile):
    merged = pd.read_csv(infile)
    print('Dataframe loaded.')

    location=['Point','Position','loggerID','River','Date','LandUse','lat','long']
    #,'width','GPS_ele',\
    # 'Distance_from_edge','Distance_from_river','LandUseBins'

    microclimate=['Celsius(C)','Humidity(%rh)','Dew Point(C)','VPD']

    mean_df=pd.DataFrame(merged.groupby(location)[microclimate].mean())
    mean_df.columns=['meanTemp','meanHum','meanDew','meanVPD']
    min_df=pd.DataFrame(merged.groupby(location)[microclimate].min())
    min_df.columns=['minTemp','minHum','minDew','minVPD']
    max_df=pd.DataFrame(merged.groupby(location)[microclimate].max())
    max_df.columns=['maxTemp','maxHum','maxDew','maxVPD']

    concat_df=pd.concat([mean_df, max_df,min_df], axis=1, join='inner')

    concat_df.to_csv(outfile)

    print('Dataframe summarised by day.')
