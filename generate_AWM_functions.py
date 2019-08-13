import pandas as pd


def generate_mean_traits(df,trait_cols,species_col):
	'''
	for each of the trait columns generate a mean trait for every species listed in the trait data frame
	'''
	print('Generating mean traits for each species.')

	mean_traits = pd.DataFrame(df.groupby([species_col])[trait_cols].mean())

	return mean_traits

def generate_AWMs(df,first_species_col,last_species_col,mean_traits,trait_cols):
	'''
	generates a assemblage weighted means for the dung beetle community data
	'''

	#get list of species columns
	species_cols = df.loc[:,first_species_col:last_species_col].columns

	#create an empty total abundance column 
	df['Total_Abundance'] = 0

	#generate total abundance for each point
	print('Generating total abundances for each point.')

	#loop over each trait 
	for trait in trait_cols:
		#loop over each abundance and microclimate row
		for i in df.index:
			#reset total abundance tracker
			total_abundance = 0
			# loop over species columns
			for j in species_cols:
				if df.loc[i,j] != 0:
					#loop over traits dataframe to check for a match
					for k in mean_traits.index:
						#if match found
						if j == k:
							if mean_traits.loc[j,trait] != '':
								#if there is a trait mean present
								total_abundance = total_abundance + df.loc[i,j]
							
			df.loc[i,'total_abundance_'+trait] = total_abundance


	print('Generating AWMs.')


	#loop for each trait
	for trait in trait_cols:
		#set trait average at 0
		df[trait + '_AWM'] = 0
		#loop over abundance and microclimate dataframe
		for i in df.index:
			#reset AWM column
			df.loc[ i , trait + '_AWM' ] = 0
			#loop over the species columns
			for j in species_cols:
				#check the abundance isn't zero
				if df.loc[ i , j ] != 0:
				#check the species is in the traits data set
					for k in mean_traits.index:
							#if match found
						if j == k:
							#check there are trait data available for the match
							if mean_traits.loc[ j , trait ] != '':
								#calculate the proportion of the assemblage comprised by that species
								assemblage_proportion = df.loc[ i , j ] / df.loc[ i , 'total_abundance_' + trait ]
								#add the running total AWM to the proportion of the assemblage timesed by the mean trait
								df.loc[ i , trait + '_AWM' ] = df.loc[ i , trait + '_AWM' ] + assemblage_proportion * mean_traits.loc[ j , trait ]	

	return df


