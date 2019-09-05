from append_all_dung_beetle_dataframes_functions import *
from open_xlsx import *

root = '/home/joe/Documents/'
root_dung = root + 'Dung_Beetles/'
root_dataloggers = root + 'Dataloggers/Data/'
root_safe = root + 'Safe_Project/'

#open the dung beetle abundance files as pandas dataframes
print('Opening abundance dataframes to be appended.')
[rivers, newton_2015, newton_2017, fragments] = open_xlsxs([root_dung + 'safe_rivers_transposed.processed.xlsx',
	root_dung + 'DungBeetleData2015_JW.processed.xlsx',
	root_dung + 'DungBeetleData2017-18_JW.processed.xlsx',
	root_dung + 'safe.fragments.2011.processed.xlsx'])
print('Dataframes appended.')

#generate SAFE point codes for the SAFE rivers data
print('Generating SAFE point codes for all points across all dataframes.')
rivers = generate_matching_point_codes_rivers(rivers,'Site')

#generate SAFE point codes for the Newton rivers data
newton_2015 = generate_matching_point_codes_newton(newton_2015,['river','point'])
newton_2017 = generate_matching_point_codes_newton(newton_2017,['river','point'])
print('SAFE point codes generated.')

#drop na rows from dataframes
print('Dropping NAs from dataframes.')
rivers = remove_na_rows(rivers)
newton_2015 = remove_na_rows(newton_2015)
newton_2017 = remove_na_rows(newton_2017)
fragments = remove_na_rows(fragments)
print('NAs dropped.')

#remove all columns that aren't date, site or species
print('Removing all columns other than abundances, date and site.')
rivers = drop_cols(rivers, 'Caccobius bawangensis', 'Onthophagus johkii')
newton_2015 = drop_cols(newton_2015, 'Caccobius bawangensis', 'Yvescamberfortius sarawacus')
newton_2017 = drop_cols(newton_2017, 'Caccobius bawangensis', 'Yvescamberfortius sarawacus')
fragments = drop_cols(fragments, 'Caccobius bawangensis', 'Onthophagus (aff) phanaeides')
print('Columns removed.')

#combine all the abundance matrices into one data sheet (rivers, fragments and newton datasets)
print('Combining abundance dataframes.')
combined_abundances = combine_abundance_matrices(rivers, fragments, newton_2015, newton_2017)
print('Dataframes combined.')

print('Change NAs to zeroes.')
combined_abundances = combined_abundances.fillna(0)
print('NAs changed to zeroes.')

#open the two files with coordinates in for the points
print('Open coordinates files.')
[simon_points,safe_points] = open_xlsxs([root_dataloggers + 'Vegetation/allpoints_subsetted.xlsx',
	root_safe + 'all_safe_points.xlsx'])
print('Coordinate files opened.')

#change the code of simons points to match the SAFE universal coding system
print('Convert  coordinate dataframe point codes to SAFE point codes.')
simon_points = generate_matching_point_codes_simon(simon_points, 'name')
print('SAFE point codes generated.')

#combines the two datasets into one dataframe of all the SAFE points with correct SAFE codes
print('Combine coordinate dataframes.')
all_points = combine_all_points(simon_points, safe_points)
all_points.to_csv(root_dataloggers + 'Vegetation/All_coordinates.csv')
print('Dataframes combined and saved as ' + root_dataloggers + 'Vegetation/All_coordinates.csv')


#match latlong gps coordinates for sites with the dung beetle abundance dataframe
print('Matching abundances and GPS coordinates.')
gps_data_abundance = match_gps_to_abundance(combined_abundances, all_points)
gps_data_abundance.to_csv(root_dung + 'Abundance_Datasets_Combined_gps.csv')
print('Coordinates and abundances matched and saved as' + root_dung + 'Abundance_Datasets_Combined_gps.csv')
