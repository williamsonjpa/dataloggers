from append_all_dung_beetle_dataframes_functions import *
from open_xlsx import *

root = 'C:/Users/hp/Documents/'
root_dung = root + 'Dung_Beetles/'
root_dataloggers = root + '2018/Dataloggers/Data/'
root_safe = root + 'Safe_Project/'

#open the three dung beetle abundance files as pandas dataframes
[rivers, newton_2015, newton_2017, fragments] = open_xlsxs([root_dung + 'safe_rivers_transposed.processed.xlsx',
	root_dung + 'DungBeetleData2015_JW.processed.xlsx',
	root_dung + 'DungBeetleData2017-18_JW.processed.xlsx',
	root_dung + 'safe.fragments.2011.processed.xlsx'])
 
#generate SAFE point codes for the SAFE rivers data
rivers = generate_matching_point_codes_rivers(rivers,'Site')

#generate SAFE point codes for the Newton rivers data
newton_2015 = generate_matching_point_codes_newton(newton_2015,['river','point'])
newton_2017 = generate_matching_point_codes_newton(newton_2017,['river','point'])

#combine all the abundance matrices into one data sheet (rivers, fragments and newton datasets)
combined_abundances = combine_abundance_matrices(rivers, fragments, newton_2015, newton_2017)

combined_abundances.to_csv(root_dung + 'Abundance_Datasets_Combined.csv')

#open the two files with coordinates in for the points 
[simon_points,safe_points] = open_xlsxs([root_dataloggers + 'Vegetation/allpoints_subsetted.xlsx',
	root_safe + 'all_safe_points.xlsx'])

#change the code of simons points to match the SAFE universal coding system
simon_points = generate_matching_point_codes_simon(simon_points, 'name')

#combines the two datasets into one dataframe of all the SAFE points with correct SAFE codes
all_points = combine_all_points(simon_points, safe_points)

all_points.to_csv(root_dataloggers + 'Vegetation/All_coordinates.csv')



#match latlong gps coordinates for sites with the dung beetle abundance dataframe
#gps_data_abundance = match_gps_to_abundance(combined_abundances, all_points)

#print('Combined data sets saved as ' + root_dung + 'Abundance_Datasets_Combined.csv')

#gps_data_abundance.to_csv(root_dung + 'Abundance_Datasets_Combined.csv')