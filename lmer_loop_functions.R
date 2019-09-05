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
##   response: Character vector of length 1 (response variable)
##   rand_eff: Character vector of length 1 (random effect)

iterate_lmer <- function( response , rand_eff , vec_tests ,  df ){
  
  # Create tmp vector to store models 
  tmp.models <- vector( mode = "list", length( vec_tests ) )
  # This for loop goes through all the elements in vector
  # "vec_tests", which contain the variables to test for
  for( i in 1:length( vec_tests ) ){

    #paste response and explanatory variables together
    model_terms <- c( response , vec_tests[i] )
    model <- paste0( model_terms, collapse = " ~ " )
    
    #paste the random effects onto the model
    model <- c( model , rand_eff )
    model <- paste0( model , collapse = " + " )
    
    cat( "This lmer is gonna take place with vector ", i, "\n",
         "which is: ", model, "\n")
    
    # Run function lme4::lmer with corresponding element
    # in vector "vec_tests"
    tmp.models[[ i ]] <- lme4::lmer( formula = model , data = df )
    names( tmp.models )[[i]] <- paste( response , i , sep='' )
    
  }
  
  return( tmp.models )

}

## Function 3: generate AICtable for the model list
## Arguments:
##   model_list: list of the models outputted by function 2 
generate_AICtab <- function( model_list ){
  
  # generate main AIC table 
  AICtable <- bbmle::AICtab( model_list )
  summ_table <- do.call( rbind, lapply(model_list, broom::glance))
  AICtable[["Resid.Dev"]] <- summ_table[["deviance"]]

  return( AICtable )
}