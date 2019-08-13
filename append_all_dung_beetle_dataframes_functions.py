import pandas as pd

'''
functions to append all the dung beetle data together from the SAFE fragments, rivers and the Newton rivers
'''


def generate_matching_point_codes_rivers(data_rivers,point_col):
	'''
	input safe river dataset and  and the point column titles and generate point codes that match the SAFE universal point codes
	'''

	#adds 0s before numbers that aren't 10, also changes hyphen to underscore
	rivers = add_in_zeros_to_sites(data_rivers, point_col)

	#change rvjr to vjr
	rivers = fix_vjr_code(rivers, point_col)

	#remove the m from those the experimental riparian buffers
	rivers = remove_m(rivers, point_col)

	#change to the safe format with L for lombok and RT for riparian transect
	rivers = convert_to_safe_codes(rivers,point_col)

	return rivers

	
def add_in_zeros_to_sites(data, point_col):

	'''
	separates the point codes with hyphens and adds a 0 if they are not point ten.
	Also changes hyphen to an underscore
	ie. VJR-9 becomes VJR_09
	'''

	for i in data.index:
		split_point = data.loc[i,point_col].split('-')
		if split_point[1] != '10':
			data.loc[i,point_col] = str(split_point[0] + '_0' + split_point[1])
		else:
			data.loc[i,point_col] = str(split_point[0] + '_' + split_point[1])



	return data


def fix_vjr_code(data, point_col):
	'''
	changes rvjr river code to vjr in the column point_col
	i.e. RVJR_01 becomes VJR_01
	'''
	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		if split_point[0] == 'RVJR':
			data.loc[i,point_col] = data.loc[i,point_col][1:]

	return data

def remove_m(data, point_col):
	'''
	removes the m (metre) from after the river codes for the column point_col
	i.e 120m_09 becomes 120_09
	'''
	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		if split_point[0][-1].lower() == 'm':
			data.loc[i,point_col] = str(split_point[0][:-1]+'_'+split_point[1])

	return data

def convert_to_safe_codes(data, point_col):
	'''
	change to the safe format with L for lombok and RT for riparian transect
	i.e. VJR_01 becomes RT_VJR_L_01
	'''
	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		data.loc[i,point_col] = str('RT_'+split_point[0]+'_L_'+split_point[1])

	return data

def generate_matching_point_codes_newton(data, point_cols):
	'''
	generate point codes for the newton data to match up with the newton coordinate file
	'''
	#adds in zeros before the numbers unless 10, combines both columns into one 'Site' column e.g. RVJR-01
	newton = add_in_zeros_to_sites_multiple_columns(data, point_cols)

	#removes r from vjr
	newton =  fix_vjr_code(newton, 'Site')

	#removes r from rlfe
	newton = fix_lfe_code(newton, 'Site')

	#change to the safe format with L for lombok and RT for riparian transect
	newton = convert_to_safe_codes(newton, 'Site')

	#removes the rr from riparian buffer codes and changes RT to RR as prefix of code
	newton = remove_rr(newton, 'Site')

	#removes the rop from riparian buffer codes and changes RT to ROP as prefix of code
	newton = remove_rop(newton, 'Site')

	return newton


def add_in_zeros_to_sites_multiple_columns(data, point_cols):
	'''
	combines the river and the point columns with a underscore, and adds a 0 if they are not point ten.
	ie. VJR 9 becomes VJR_09
	'''

	for i in data.index:
		if str(data.loc[i,point_cols[1]])!='10':
			data.loc[i,'Site']=str(data.loc[i,point_cols[0]]).upper()+'_0'+str(data.loc[i,point_cols[1]])
		else:
			data.loc[i,'Site']=data.loc[i,point_cols[0]].upper()+'_'+str(data.loc[i,point_cols[1]])

	return data


def fix_lfe_code(data, point_col):
	'''
	changes rlfe river code to vjr in the column point_col
	i.e. RLFE-01 becomes LFE-01
	'''
	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		if split_point[0] == 'RLFE':
			data.loc[i,point_col] = data.loc[i,point_col][1:]

	return data

def remove_rr(data, point_col):
	'''
	removes the rr tag from the river codes and changes RT to RR for riparian buffers
	i.e. RT_RR12_L_01 becomes RR_12_L_01 
	'''

	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		if split_point[1][:2] == 'RR':
			data.loc[i,point_col] = str('RR_' + split_point[1][2:] + '_L_' + split_point[3])
		elif split_point[1][:3].upper() == 'SJI':
			data.loc[i,point_col] = str('RR_' + split_point[1] + '_L_' + split_point[3])
	return data

def remove_rop(data, point_col):
	'''
	removes the rr tag from the river codes and changes RT to RR for riparian buffers
	i.e. RT_ROP2_L_01 becomes ROP_2_L_01 and 
	'''

	for i in data.index:
		split_point = data.loc[i,point_col].split('_')
		if split_point[1][:2] == 'ROP':
			data.loc[i,point_col] = str('ROP_' + split_point[1][3:] + '_L_' + split_point[3])

	return data

def generate_matching_point_codes_simon(data, point_col):
	'''
	change the point codes in simon's dataset to match the safe project universal point code system
	'''

	#removes PC at start of point number and changes hyphen to underscore
	simon_data = remove_pc_add_underscore(data, point_col)

	#change to the safe format with L for lombok and RT for riparian transect
	simon_data = convert_to_safe_codes(simon_data, 'Site')

	#removes the rr from riparian buffer codes and changes RT to RR as prefix of code
	simon_data = remove_rr(simon_data, 'Site')

	#removes the rop from riparian buffer codes and changes RT to ROP as prefix of code
	simon_data = remove_rop(simon_data, 'Site')

	return simon_data


def remove_pc_add_underscore(data, point_col):
	'''
	removes PC at start of point number and changes hyphen to underscore
	e.g. RR12-PC01 becomes RR12_01
	'''
	for i in data.index:
		split_point = data.loc[i,point_col].split('-')
		if split_point[1][:1] == 'PC':
			data.loc[i,'Site'] = str(split_point[0] + '_' + split_point[3][2:])
		else:
			data.loc[i,'Site'] = str(split_point[0] + '_' + split_point[1])
	return data

def combine_abundance_matrices(rivers, fragments, newton_2015, newton_2017):
	'''
	combines all three of the datasets to make one master sheet of all dung beetle abundance data from SAFE and the surrounding landscapes
	'''

	#create new dataframe for everything to go in 
	combined = rivers.append(newton_2017, ignore_index = True, sort = False)
	combined = combined.append(newton_2015, ignore_index = True, sort = False)
	combined = combined.append(fragments, ignore_index = True, sort = False)

	return combined


def combine_all_points(simon, safe):
	'''
	combines the two datasets into one dataframe of all the SAFE points with correct SAFE codes
	'''

	#new column with matching name to other datasets
	safe['Site'] = safe['name']

	simon['lat'] = simon['Lat']
	simon['lon'] = simon['Lon']
	simon['ele'] = simon['GPS-ele']


	combined = pd.concat([safe,simon], ignore_index = True, sort = False)

	return combined

def match_gps_to_abundance(abundance, gps):
	'''
	takes the combined dung beetle dataframe and searches against the gps dataframe for a match
	'''

	matched = pd.merge(abundance, gps, on='Site')

	return matched