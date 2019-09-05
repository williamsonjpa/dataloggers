#-------------------#
# Clean environment #
#-------------------#
rm( list = ls( ) )

#-----------------------#
# SET WORKING DIRECTORY #
#-----------------------#
library( rstudioapi ) 
# Get the path to current open R script and find main dir
path_to_file <- getActiveDocumentContext()$path
wd <- paste( dirname( path_to_file ), "/", sep = "" )
setwd( wd )

#---------------------------------#
# import dataframe and clean data #
#---------------------------------#
library(bbmle)
library(broom)
library(corrplot)
library(ggplot2)
library(gridExtra)
library(lme4)
library(lmerTest)

df<-read.csv('../Data/Final/Combined_Point_scale_12.5.csv')
source( "pointData_lmer_loop_functions.R" )
df_lmer <- clean_df( df )

#-------#
# TASKS #
#-------#

# see these locations for functions 
source( "lmer_loop_functions.R" )
source( "pointData_lmer_loop_functions.R" )

# 1. Create character vectors with variables to test
vars <- c( "TPI", "slope", "aspect", "PAI_log", "Hmean_log", 
           "LandUse", "Hmean_log:aspect" )

# 2. Now create all possible combinations of vectors in a list
var_combs_list <- create_var_combs_list( all_vars = vars )

# 3. Subset the vector combinations to remove those that are not possible with interaction rules
var_combs_list <- var_subset( var_combs_list )

# 4. Convert list to vector
# make empty vector to fill
var_combs_vec <- rep( '' , length(var_combs_list))

# fill vector with variable combination strings
for(i in 1:length( var_combs_list )){
  var_combs_vec[i] <- paste(var_combs_list[[i]], collapse = (' + '))
}

# 5. Create a vector of response variables to give to the iterate_lmer function
resp_var_vec <- c( 'maxTemp' , 'meanTemp' , 'maxVPD' , 'meanVPD' )

# 6. Call function with vector "vector_test_pars" plus your data 
#    in the second argument of the function
all_model_list <- iterate_lmer(response_vec = resp_var_vec,
                               rand_eff = '(1|riv_poi)',
                               vec_tests = var_combs_vec,
                               df = df_lmer )

# 7. Generate AIC table for the models
# cannot get this to run, will have to return to it at some point
# all_models_AICtabs <- iterate_AICtab( all_model_list = all_models )

#for now do it all here
# make an output list of the tables
AICtable_list <- vector( mode='list' , length( all_model_list ))
  
#iterate over each response model lisdt
for( i in 1:length( all_model_list ) ){
  cat( 'Generating AIC tables for ', names( all_model_list )[i] , ' models.' , '\n' )
  
  # save the single model list as an object so AICtab doesnt freak out
  single_model_list <- all_model_list[[ i ]]
  AICtable <- bbmle::AICtab( single_model_list , weights = TRUE , sort = T )

  # add deviances to AIC tables
  summ_table <- do.call( rbind, lapply( single_model_list , broom::glance ))
  AICtable[[ "Resid.Dev" ]] <- summ_table[[ "deviance" ]]
  
  # add AIC table to list
  AICtable_list[[ i ]] <- AICtable
  
}

#give the AICtables names in the list
names( AICtable_list ) <- names( all_model_list )

# 8. subset AICtabs so that only models representing 95% of weight are shown
AICtable_list <- subset_AICtables( table_list = AICtable_list , cutoff = 0.95 )

# 9. match up the models with their constituent terms 
AICtable_list <- match_AICtabs_with_exp_vars( AICtable_list = AICtable_list , var_combs_vec = var_combs_vec , 
                                              exp_vars = vars )


# 10. model ouput table.
source( "lmer_loop_functions.R" )
all_models_output_table <- generate_output_table( AICtable_list = AICtable_list , exp_vars = vars )
