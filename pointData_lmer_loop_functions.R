## Function 1: Clean up dataframe and return simplified version for use in lmer tests
##Arguments:
##   df: Data frame with your data
clean_df <- function( df ){
  
  #set some of the variables as the correct type
  df$Point<-as.factor(df$Point)
  df$loggerID<-as.factor(df$loggerID)
  df$setup_date<-as.Date(df$setup_date)
  df<-subset(df,df$Position!='cavity')
  df$Position<-factor(df$Position, levels = c('buffer5m','buffer15m','bufferedge','buffer25m',
                                              'buffer35m','buffer45m','op5m','op15m','op25m',
                                              'op35m','op45m'),ordered=TRUE)
  
  #unique variable for every point, can test how many datapoints have been dropped by removing outliers
  df$riv_poi_pos<-as.factor(paste(df$River,df$Point,df$Position))
  
  df<-subset(df,df$riv_poi_pos!='RR8 5 op25m' & df$riv_poi_pos!='RR2 8 buffer15m' & df$riv_poi_pos!='RR14 8 op5m'& df$riv_poi_pos!='SJI1 8 buffer5m' &
               df$riv_poi_pos!='RR12 2 op25m' & df$riv_poi_pos!='RR3 8 bufferedge')
  
  #unique variable for every point, can test how many datapoints have been dropped by removing outliers
  df$riv_poi<-as.factor(paste(df$River,df$Point))
  
  #get rid of one RVJR with an edge dist of 0
  for(i in 1:nrow(df)){
    if(as.character(df$LandUse[i])==as.character('CF')){
      df$dist_dge[i] <- NA
    }
  }
  df$LandUse2 <- 'x'
  
  #change landuse for RR with position = bufferedge
  for(i in 1:nrow(df)){
    df$LandUse2[i] <- as.character(df$LandUse[i])
    if(as.character(df$LandUse[i])==as.character('RR')){
      if(as.character(df$Position[i])==as.character('bufferedge')){
        df$LandUse2[i] <- 'x_Edge' 
      } else {
        df$LandUse2[i] <- as.character(df$LandUse[i])
      }
    } 
  }
  
  df$LandUse <- as.factor(df$LandUse2)
  
  #subset dataframe to relevant columns
  df_lmer <- with(df, data.frame(maxTemp, meanTemp, maxVPD, meanVPD, canopy_height_mean, SAFE_TPI_r4_mean, SAFE_slope_r4_mean, SAFE_aspect_r4_mean, pai_mean, dist_dge, LandUse, riv_poi))
  df_lmer <- na.omit(df_lmer)
  
  #change column names 
  df_lmer$aspect <- sin(df_lmer$SAFE_aspect_r4_mean)
  df_lmer$slope <- df_lmer$SAFE_slope_r4_mean
  df_lmer$TPI <- df_lmer$SAFE_TPI_r4_mean
  df_lmer$Hmean_log <- log(df_lmer$canopy_height_mean)
  df_lmer$PAI_log <- log(df_lmer$pai_mean)
  df_lmer$dist_edge <- df_lmer$dist_dge
  
  return( df_lmer )
  
}

## Function 2: Subset the pointData variable combinations to remove those that
##             break the rules of interactions
##Arguments:
##   var_list: list with all the possible variable combinations in it

var_subset <- function( var_list ){
   
  #iterate over var_list
  for( i in 1:length( var_list )){          
    
    # scan values for the variables of interest
    find.hmeanlog <- which( var_combs_list[[ i ]] == "Hmean_log" )
    find.aspect <- which( var_combs_list[[ i ]] == "aspect" )
    find.interaction <- which( var_combs_list[[ i ]] == "Hmean_log:aspect" )
    # if statements whereby if the interaction term is peresent and the 
    # constituent variables are not
    if( length(find.interaction) > 0 &
        length(find.hmeanlog) < 1 |
        length(find.interaction) > 0 &
        length(find.aspect) < 1
        ){
      
      # add row to those to be dropped 
      if( exists( 'drop_rows' ) == FALSE){
        drop_rows <- i
      } else {
        drop_rows <- c( drop_rows, i )
      }
    }
  }
  #return the subsetted var_list, or if no subsets to make return original list
  if( exists( 'drop_rows' ) == TRUE){
    return( var_list[-c(drop_rows)] )
  }else{
    return( var_list )
  }
}
