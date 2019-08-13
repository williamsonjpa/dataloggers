import pandas as pd
import numpy as np
import openpyxl
import math

root=('C:/Users/hp/Documents/Leeches/')

def reorder_leech_mammal_columns(infile,outfile):
	'''
	reorders the leech mammal dataframe so that the leeches, dates and efforts are side by side
	'''
	leech=pd.read_csv(infile)
	non_survey_columns=leech.columns[:59].tolist()

	col_list=['a','b']
	col_types=['b','t','e','date.','second.']
	year=['.15','.16']

	for i in year:
		for j in range(1,21):
			for k in col_types:
				col_list.append(str(k)+str(j)+i)

	col_list=col_list[2:]

	col_list=non_survey_columns+col_list

	col_list=col_list+['NumberOfSites']

	leech=leech[col_list]

	leech.to_csv(outfile)




reorder_leech_mammal_columns(root+'Mammal_Leech_Combined.csv',root+'Mammal_Leech_Combined_Sorted.csv')