#!/home/joe/miniconda3/bin/python3

from create_required_directories import create_directories
from conversion2 import run_conversion2_script
from addinfo2 import iterate_addinfo2
from edit2 import iterate_edit2
from merge2 import merge
from append2 import iterate_append
from VPD import iterate_VPD_script
from SummarisePointData import pointSummaryData
from SummariseDailyData import dailySummaryData
'''
one script that will run all the other python scripts until you have your output 
datalogger documents. This should be useful for future use or for others to also
run this code

for this to work you must edit the root and non-datalogger filenames below
be sure to include a / at the start of the filenames

the Dataloggers folder should have a /Code folder with the python scripts already 
inside it and a Data/Raw/ folder with the raw data folders within it

'''

####################################
###GENERATE THE MASTER MERGE FILE###
####################################

###change this to the location of the Dataloggers file
###note that this should contain the setup and collection files
root = ('/home/joe/Documents/Dataloggers')

##change these names to match the non-datalogger filenames placed within the datalogger file
setup = '/Datalogger set-up data.csv'
collection = '/DataloggerCollectionData_JW.csv'
site_data = '/Data/Vegetation/allpoints.xlsx'
veg_plot_data = '/Data/Final/vegplotData.csv'
lidar_data = '/Data/Final/lidar.csv'

#create directories for all subsequent scripts
#create_directories(root)

# #converts scripts to nonascii files
# run_conversion2_script(root, setup, collection)

#strips info from the title to allow removal of incorrect/irrelevant data
#iterate_addinfo2(root)

#removes incorrect and irrelevant data from the datalogger files, 
#also sorts files that dont work into folders within the Data/ProblemFiles directory
# iterate_edit2(root, setup, collection)

# #adds in the width and elevation and distance from edge/river data to the logger files
# #eventually this should also append lidar and vegplot data probably...
#iterate_append(root, root + site_data, root + veg_plot_data, root + lidar_data)


# #merges all the files into one file named merge.csv
# merge(root)

#adds VPD column to dataset
#iterate_VPD_script(root+'/Data/Final/merge.csv',root+'/Data/Final/merge2.csv')

# generate average data by point
pointSummaryData(root+'/Data/Final/merge2.csv',root+'/Data/Final/PointData.csv')

# generate average data by day
dailySummaryData(root+'/Data/Final/merge2.csv',root+'/Data/Final/DailyData.csv')