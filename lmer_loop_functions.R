#------------------#
# Create functions #
#------------------#
library(lme4)
library(bbmle)
library(broom)

## Function 1: Function to create the combinations of vectors looping through
## the variables.
## Arguments
##   all_vars: Character vector with all the vars run subsets of
create_var_combs_list <- function( all_vars ){
  # creates a list of all the combinations of all the variables
  var_combs_list <- unlist(lapply( 1:length( all_vars ), 
                              combn, 
                              x = all_vars, 
                              simplify = FALSE),
                      recursive = FALSE)
  
  return( var_combs_list )
}

## Function 2: Loop through the vectors to be tested, returns a vector of models
## Arguments:
##   vec_tests: Character vector with all character vectors that you have generated
##              using "create_my_vec" function.
##   df: Data frame with your data  
##   response_vec: Character vector of response variables
##   rand_eff: Character vector of length 1 (random effect)

iterate_lmer <- function( response_vec , rand_eff , vec_tests ,  df ){
  
  tmp.all.models <- vector( mode = "list", length( response_vec ))
  
  for( j in 1:length( response_vec )){
    # Create tmp vector to store models 
    tmp.models <- vector( mode = "list", length( vec_tests ) )
    # This for loop goes through all the elements in vector
    # "vec_tests", which contain the variables to test for
    for( i in 1:length( vec_tests ) ){
  
      #paste response and explanatory variables together
      model_terms <- c( response_vec[j] , vec_tests[i] )
      model <- paste0( model_terms, collapse = " ~ " )
      
      #paste the random effects onto the model
      model <- c( model , rand_eff )
      model <- paste0( model , collapse = " + " )
      
      cat( "This lmer is gonna take place with vector ", i, "\n",
           "which is: ", model, "\n")
      
      # Run function lme4::lmer with corresponding element
      # in vector "vec_tests"
      tmp.models[[ i ]] <- lme4::lmer( formula = model , data = df )
      names( tmp.models )[[i]] <- paste( response_vec[j] , i , sep='' )
    }
    
    #save models to list of all models
    tmp.all.models[[ j ]] <- tmp.models
    
  }
  
  
  names( tmp.all.models ) <- response_vec
  
  return( tmp.all.models )
  
}



## Function 3: iterate AICtable for the model list
## Arguments:
##   model_list: list of the models outputted by function 2 
# iterate_AICtab <- function( all_model_list ){
#   
#   table_list <- vector( mode='list' , length( all_model_list ))
#   
#   #iterate over each response model lisdt
#   for( i in 1:length( all_model_list ) ){
#     cat( 'Generating AIC tables for ', names( all_model_list )[i] , ' models.' , '\n' )
#     
#     # generate main AIC table 
#     single_model_list <- copy(all_model_list[[ names( all_model_list )[i] ]])
#     
#     AICtable <- bbmle::AICtab( single_model_list , weights = TRUE , sort = T )
#     AICtable <- as.data.frame.ICtab(AICtable)
#     
#     summ_table <- do.call( rbind, lapply( single_model_list , broom::glance ))
#     AICtable[[ "Resid.Dev" ]] <- summ_table[[ "deviance" ]]
#     AICtable <- as.data.frame.ICtab(AICtable)
#     
#     # row names all come out as name of first response variable so heres a fix
#     response_char <- names( all_model_list )[i]
#     row_name_subs <- rep( '' , length(all_model_list[i]))
# 
#     
#     for(j in 1:length(row.names(AICtable))){
#       row_name_subs[j] <- paste0(c(response_char,gsub("[^0-9\\.]", "", x = row.names(AICtable[j,]))),
#                                         collapse = '') 
#     }
#     row.names(AICtable) <- row_name_subs
#     
#     
#     # add AICtable to table_list
#     table_list[[ i ]] <- AICtable
#     
#   }
#   
#   names( table_list ) <- names( all_model_list )
#   return( table_list )
#   
# }

## Function 4: subset the AICtable list based on weight cumulative count
## Arguments:
##   cutoff: weight cumulative count cutoff (class num, range 0-1)
##   table_list: list of ICtab class AICtables
subset_AICtables <- function( table_list , cutoff ){
  # for each AICtable
  for( i in 1:length( table_list )){
    # uses the function below by BB to change ICtab class to df
    df <- as.data.frame.ICtab( table_list[[ i ]] )
    df$cum_weight <- cumsum( df$weight )
    df <- subset( df , cum_weight <= cutoff )
    print(df)
    table_list[[ i ]] <- df
  }
  return( table_list )
}

## Function 5: subset the AICtable list based on weight cumulative count
## Arguments:
##   AICtable_list:list of ICtab class AIC tables that have been subsetted by func 4
##   var_combs_vec: character vector with model combinations
match_AICtabs_with_exp_vars <- function( AICtable_list , var_combs_vec , exp_vars ){
  
  # looop over AIC tables
  for( i in 1:length( AICtable_list )){
    
    # save dataframe as new object
    df <- AICtable_list[[ i ]]
    
    # loop over explanatory variables to make new cols of 0s in df
    for( j in 1:length( exp_vars )){
      df[ , exp_vars[ j ] ] <- 0  
    }
    
    for( j in 1:length( df )){
      # get the model number for each row
      model_number <- as.integer( gsub( "[^0-9\\.]", "", x = row.names( df[ j , ] ) ) )
      
      # add model number to dataframe
      for( k in 1:length( exp_vars )){
        
        # if the model contains a term, change the column in df to 1 on model row
        if( grepl( exp_vars[ k ] , var_combs_vec[ model_number ] ) == TRUE ){
          df[ j , exp_vars[ k ] ] <- 1
          
        }
        
      }
      
    }
    print(df)
  }
  return( AICtable_list )
}

# Ben Bolker's AIC table to dataframe function
as.data.frame.ICtab <- function(x, row.names = NULL, optional = FALSE, ...){
  attr(x,"class") <- "data.frame"
  as.data.frame(x, row.names = row.names, optional = optional)
}
