#stats script for the datalogger data summarised by point

setwd('/home/joe/Documents/Dataloggers/Data/Final')
library(lme4)
library(semPlot)
library(lavaan)
library(corrplot)

df<-read.csv('Combined_Point_scale_12.5.csv')

#set some of the variables as the correct type
df$Point<-as.factor(df$Point)
df$loggerID<-as.factor(df$loggerID)
df$setup_date<-as.Date(df$setup_date)
df<-subset(df,df$Position!='cavity')
df$Position<-factor(df$Position, levels = c('buffer5m','buffer15m','bufferedge','buffer25m',
                                            'buffer35m','buffer45m','op5m','op15m','op25m',
                                            'op35m','op45m'),ordered=TRUE)


#unique variable for every point, can test how many datapoints have been dropped by removing outliers
df$combo<-as.factor(paste(df$River,df$Point,df$Position))


#lets get rid of outliers that were eliminated in dailyData.R

df<-subset(df,df$combo!='RR8 5 op25m' & df$combo!='RR2 8 buffer15m' & df$combo!='RR14 8 op5m'& df$combo!='SJI1 8 buffer5m' &
             df$combo!='RR12 2 op25m' & df$combo!='RR3 8 bufferedge')

#get rid of one RVJR with an edge dist of 0
for(i in 1:nrow(df)){
  if(as.character(df$LandUse[i])==as.character('CF')){
      df$dist_dge[i] <- NA
  }
}


############
### SEMs ###
############

#lets make a correlation matrix 

#subset dataframe to only contain variables of interest
corr_mat_df <- with(df, cbind(maxTemp, maxVPD, SAFE_aspect_r4_mean, 
                              SAFE_slope_r4_mean, SAFE_TPI_r4_mean, 
                              canopy_height_mean, pai_mean))

#simplify names of corr_mat_df
colnames(corr_mat_df) <- c('maxTemp','maxVPD','aspect','slope','TPI','Hmax','PAI')

#remove any rows containing NAs
corr_mat_df <- as.data.frame(na.omit(corr_mat_df))

#generate standard deviations for each variable
sds <- c(sd(corr_mat_df$maxTemp), sd(corr_mat_df$maxVPD), sd(corr_mat_df$aspect),
         sd(corr_mat_df$slope), sd(corr_mat_df$TPI), sd(corr_mat_df$Hmax), sd(corr_mat_df$PAI))

#generate correlation table
corr_table <- cor(corr_mat_df)

#show correlation table in a correlation plot
corrplot(corr_table, type = "upper", order = "hclust", tl.col = "black", tl.srt = 45)


#name the sd names as the  rownames of the correlation table
names(sds) <- rownames(corr_table)
                       
#generate covariance table 
cov_table <- cor2cov(corr_table, sds)

#lets try to recreate TJ model
tj <- '
  maxVPD ~ maxTemp + TPI
  maxTemp ~ TPI + slope + aspect * Hmax + PAI
  Hmax ~ slope
  
'
tj_fit <- sem(tj, data=corr_mat_df)
summary(tj_fit)
semPaths(tj_fit, curvePivot=T)

###########################################
###now lets include dist_edge + land_use###
###########################################

corr_mat_df_new <- with(df, data.frame(maxTemp, maxVPD, SAFE_aspect_r4_mean, 
                              SAFE_slope_r4_mean, SAFE_TPI_r4_mean, 
                              canopy_height_mean, pai_mean, dist_dge, 
                              as.character(LandUse)))

#simplify names of corr_mat_df
colnames(corr_mat_df_new) <- c('maxTemp','maxVPD','aspect','slope','TPI','Hmax','PAI','dist_edge', 'landuse')
  
#remove any rows containing NAs
corr_mat_df_new <- as.data.frame(na.omit(corr_mat_df_new))

#change land use to dummy variable of 1 for RR and 0 for OP
corr_mat_df_new$landuse <- as.character(corr_mat_df_new$landuse)
corr_mat_df_new$landuse[corr_mat_df_new$landuse=='OP'] <- 0
corr_mat_df_new$landuse[corr_mat_df_new$landuse=='RR'] <- 1

#change column classes to numeric 
corr_mat_df_new$dist_edge <- as.numeric(corr_mat_df_new$dist_edge)
corr_mat_df_new$landuse <- as.numeric(corr_mat_df_new$landuse)

#generate standard deviations for each variable
sds_new <- c(sd(corr_mat_df_new$maxTemp), sd(corr_mat_df_new$maxVPD), sd(corr_mat_df_new$aspect),
         sd(corr_mat_df_new$slope), sd(corr_mat_df_new$TPI), sd(corr_mat_df_new$Hmax), 
         sd(corr_mat_df_new$PAI), sd(corr_mat_df_new$dist_edge), sd(corr_mat_df_new$landuse))


#generate correlation table
corr_table_new <- cor(corr_mat_df_new)

#show correlation table in a correlation plot
corrplot(corr_table_new, type = "upper", order = "hclust", tl.col = "black", tl.srt = 45)

#name the sd names as the  rownames of the correlation table
names(sds_new) <- rownames(corr_table_new)

#generate covariance table 
cov_table_new <- cor2cov(corr_table_new, sds_new)

#lets try to recreate TJ model
jw <- '
  maxVPD ~ maxTemp + TPI + dist_edge
  maxTemp ~ TPI + slope + aspect * Hmax + PAI + dist_edge + landuse
  Hmax ~ slope + dist_edge + landuse
  
'
jw_fit <- sem(jw, data=corr_mat_df_new)
summary(jw_fit)
semPaths(jw_fit, curvePivot=T)


