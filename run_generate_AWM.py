import pandas as pd
from generate_AWM_functions import *

root = 'C:/Users/hp/Documents/2018/Dataloggers/Data/'
root_dung = 'C:/Users/hp/Documents/Dung_Beetles/'
root_thermal = 'C:/Users/hp/Documents/2018/Thermal/'

def trait_and_abundance_append(abundance_microclimate_data,first_species_col,last_species_col,\
  traitData, trait_cols, species_col,outfile):
	'''
	takes the microclimate data and adds the dung beetle data to it.
	then using the ctmax and body size data it makes assemblage weighted averages of these traits
	trait_cols is a string of the trait data columns separated by ;
	first_species_col & last_species_col are the names of the first and last species cols in the db abundance data
	'''
	print('Reading in dataframes.')
	#load microclimate data
	df=pd.read_csv(abundance_microclimate_data)

	#load dung beetle trait data
	xl=pd.ExcelFile(traitData)
	traits=xl.parse(xl.sheet_names[0]) 

	#generate a dataframe of the mean traits for each species
	mean_traits=generate_mean_traits(traits,trait_cols,species_col)

	#generate assemblage weighted means for the different points
	df=generate_AWMs(df,first_species_col,last_species_col,mean_traits,trait_cols)

	#save to csv file
	df.to_csv(outfile, sep = ',')

	print('Output saved as ' + outfile + '.')

trait_and_abundance_append(root_dung + 'Abundance_Datasets_Combined_Manually_Edited.csv',\
	'Caccobius bawangensis','Panelus sp. 2',\
	root_thermal + 'thermal.data.2018.processed.xlsx',\
	['ctmax','length','pro.width'],\
	'new_binomial_name',\
	root_thermal + 'all_abundance_microclimate_traits.csv'\
	)
