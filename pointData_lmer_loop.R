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

# see this location for functions 
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

# 5. Call function with vector "vector_test_pars" plus your data 
#    in the second argument of the function
maxTemp_models <- iterate_lmer(response = 'maxTemp',
                               rand_eff = '(1|riv_poi)',
                               vec_tests = var_combs_vec,
                               df = df_lmer )

# 6. Generate AIC table for the models
source('lmer_loop_functions.R')
maxTemp_AICtab <- generate_AICtab( maxTemp_models )

summary(maxTemp_models$maxTemp58)
summary(maxTemp_models$maxTemp36)


