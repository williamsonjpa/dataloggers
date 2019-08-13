import pandas as pd

'''
runs through a list of .xlsx files and returns as a list of pandas dataframes
'''


def open_xlsx(xlsx_file):

	#fill empty list with dataframes generated from first sheet of xlsx files
	xl = pd.ExcelFile(xlsx_file)
	dataframe = xl.parse(xl.sheet_names[0])

	return dataframe


def open_xlsxs(list_of_xlsx_files):

	#create empty list to fill with dataframes
	list_of_dataframes = ['empty'] * len(list_of_xlsx_files)

	#fill empty list with dataframes generated from first sheet of xlsx files
	x=0
	for i in list_of_xlsx_files:
		xl = pd.ExcelFile(i)
		list_of_dataframes[x] = xl.parse(xl.sheet_names[0])
		x=x+1

	return list_of_dataframes

