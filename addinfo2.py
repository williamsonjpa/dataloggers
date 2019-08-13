import os
import os.path
import glob
import pandas as pd

def iterate_addinfo2(root):

	in_folder = root + '/Data/Converted'
	out_folder = root + '/Data/AddedInfo'

	# start off by emptying the addinfo file of csv files previously generated
	clear_directory_csv(out_folder)

	###glob loop function with a printing of the numbers if statement
	infilelist = glob.glob(os.path.join(in_folder, "*.csv"))
	filenumber = 0
	for f in infilelist:
		f = remove_glob_filepath(f)
		add_information_from_filename(out_folder, f)
		filenumber += 1
		infile_length = len(infilelist)

		#only prints the progess message every 10th file or for the last file
		if str(filenumber)[-1] == '0' or filenumber == infile_length:
			print('Added information to ' + str(filenumber) + ' of ' + str(infile_length) + ' files!')

def remove_glob_filepath(file_with_path):
	'''
	gets rid of weird backspaces generated by glob
	'''
	nopath = file_with_path.split('\\')
	return nopath[-1]

def generate_infile_name(infile):
	filename = infile.split('/')[-1]
	return filename

def clear_directory_csv(directory):
	'''
	function to clear a directory of all csv files
	'''

	filelist = glob.glob(os.path.join(directory, "*.csv"))
	for f in filelist:
	    os.remove(f)

def add_information_from_filename(out_folder, infile):
	'''
	function to add information from the filename to the actual file
	also change the date time into the same format as the set up and collection files
	'''

	#open the infile
	df = pd.read_csv(infile)

	#strip the data out of the title 
	additional_data = strip_data_from_title(infile)

	# append data to dataframe
	df = append_additional_data_to_dataframe(additional_data,df)

	# change the date time column into a date and a time column that match the setup and collection files
	df = change_date_time_columns(df)

	outfile = generate_infile_name(infile)

	#save the file to the AddedInfo folder
	df.to_csv(out_folder + '/' + outfile)



def strip_data_from_title(infile):
	'''
	takes useful information from the filename and append it to the dataframe
	'''
	#get the filename
	filename = generate_infile_name(infile)
	#remove the extension
	filename = filename[:-4]

	#return a list of the title split by '-'
	return filename.split('-')

def append_additional_data_to_dataframe(additional_data,dataframe):
	'''
	takes the loggerID, river, point and position from the dataframe title and appends them
	using the title, generate landuse
	'''

	dataframe['loggerID'] = ('00' + additional_data[1])[-3:] #makes sure it is in the right format .e.g 001
	dataframe['River']=additional_data[2]
	dataframe['Point']=additional_data[3]
	dataframe['Position']=additional_data[4]
	for i in dataframe.index:
		dataframe.loc[i,'Position']=dataframe.loc[i,'Position'].lower().replace(' ','')

	#generates land use and appends
	position=additional_data[4]
	river=additional_data[2]

	if position.lower()[:2]=='op':
		landuse='OP'
	elif river.lower()=='rlfe':
		landuse='CF'
	elif river.lower()=='rvjr':
		landuse='CF'
	elif river.lower()[:2]=='rr':
		landuse='RR'
	elif river.lower()[:2]=='sj':
		landuse='RR'
	else:
		landuse='error'

	dataframe['LandUse']=landuse

	return dataframe

def change_date_time_columns(df):
	for i in df.index:
		#get the date sorted into a column called 'Date'
		df.loc[i,'Date']=df.loc[i,'Time'][:10]
		split_date=df.loc[i,'Date'].split('-')
		df.loc[i,'Date']=split_date[2]+'/'+split_date[1]+'/'+split_date[0]


		#reassign the column 'Time' to just be the time
		df.loc[i,'Time']=df.loc[i,'Time'][11:]
		#change the times so all times are on the hour instead of some being at 1 second past the hour
		df.loc[i,'Time']=df.loc[i,'Time'][:-2]+'00'

	return df