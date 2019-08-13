import pandas as pd

root='C:/Users/hp/Documents/2018/Dataloggers/Data'
root_dung='C:/Users/hp/Documents/Dung_Beetles'
root_thermal='C:/Users/hp/Documents/2018/Thermal'



def trait_and_abundance_append(abundance_data,first_species_col,last_species_col,\
 microclimate_data,outfile):
	'''
	takes the microclimate data and adds the dung beetle data to it.
	then using the ctmax and body size data it makes assemblage weighted averages of these traits
	trait_cols is a string of the trait data columns separated by ;
	first_species_col & last_species_col are the names of the first and last species cols in the db abundance data
	'''
	#load microclimate data
	df=pd.read_csv(microclimate_data)

	#load dung beetle abundance data
	xl=pd.ExcelFile(abundance_data)
	db=xl.parse(xl.sheet_names[0])

	#change the dung beetle point codes to match against the lidar ones
	db=generate_point_codes(db,'river','point')

	#match the lidar up with the abundance data
	df=append_abundance_data(db,first_species_col,last_species_col, df)

	#save to csv file
	df.to_csv(outfile, sep = ',')

	print('Output saved as ' + outfile + '.')

def generate_point_codes(df,river,point):
	'''
	generates matching point codes to the lidar datsets
	'''
	print('Generating matching point codes for lidar and abundance files.')
	for i in df.index:
		if str(df.loc[i,'point']) != '10':
			df.loc[i,'RiverPointCode'] = df.loc[i,river] + '-0' + str(df.loc[i,point])
		else:
			df.loc[i,'RiverPointCode'] = df.loc[i,river] + str(df.loc[i,point])

	return df

def append_abundance_data(db,first_species_col,last_species_col,df):
	'''
	matches up the dung beetle abundance data to the dung beetle 
	db = dung beetle data
	df = microclimate
	''' 
	print('Matching and appending dung beetle abundance data with microclimate and lidar datasets.')

	dbCols = db.loc[:,first_species_col:last_species_col].columns

	for i in dbCols:
		df[i] = ''

	for i in db.index:
		for j in df.index:
			if db.loc[i, 'RiverPointCode'] == df.loc[j,'RiverPointCode']:
				for k in dbCols:
					df.loc[j,k] = db.loc[i,k]

	#subset the dataframe to remove rows with no dung beetle data
	df = df[df[first_species_col] != '']

	return df


trait_and_abundance_append(root_dung+'/DungBeetleData_2015_2017_2018_JW.processed.xlsx',\
	'Caccobius bawangensis','Yvescamberfortius sarawacus',\
	root+'/Final/Combined_Point.csv',\
	root_thermal+'/abundance_microclimate.csv'\
	)
