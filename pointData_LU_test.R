#stats script for the datalogger data summarised by point

setwd('/home/joe/Documents/Dataloggers/Data/Final')

library(bbmle)
library(broom)
library(corrplot)
library(ggplot2)
library(gridExtra)
library(lme4)
library(lmerTest)

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
df_lmer <- corr_mat_df <- with(df, data.frame(maxTemp, meanTemp, maxVPD, meanVPD, canopy_height_mean, SAFE_TPI_r4_mean, SAFE_slope_r4_mean, SAFE_aspect_r4_mean, pai_mean, dist_dge, LandUse, riv_poi))
df_lmer <- na.omit(df_lmer)

#change column names 
df_lmer$aspect <- sin(df_lmer$SAFE_aspect_r4_mean)
df_lmer$slope <- df_lmer$SAFE_slope_r4_mean
df_lmer$TPI <- df_lmer$SAFE_TPI_r4_mean
df_lmer$Hmean_log <- log(df_lmer$canopy_height_mean)
df_lmer$PAI_log <- log(df_lmer$pai_mean)
df_lmer$dist_edge <- df_lmer$dist_dge



#lets see how the explanatory variables are correlated
corr_df <- with(df_lmer, cbind(aspect, dist_edge, slope, TPI, Hmean_log, PAI_log, LandUse))
corr_table <- cor(corr_df)
p_table <- cor.mtest(corr_df)
corrplot(corr_table, type = "upper", order = "hclust", tl.col = "black", tl.srt = 45, 
         p.mat = p_table[["p"]], sig.level = 0.05, insig = 'blank')


#############
### LMERs ###
#############

##############
## maxT LME ##
##############

mxt_lm1 <- lmer(maxTemp ~ TPI + slope + aspect + PAI_log + Hmean_log + LandUse + Hmean_log:aspect + (1|riv_poi), data=df_lmer)

drop1(mxt_lm1, test='Chisq')
mxt_lm2 <- update(mxt_lm1, ~.-slope)

drop1(mxt_lm2, test='Chisq')
mxt_lm3 <- update(mxt_lm2, ~.-aspect:Hmean_log)

drop1(mxt_lm3, test='Chisq')
mxt_lm4 <- update(mxt_lm3, ~.-Hmean_log)

drop1(mxt_lm4, test='Chisq')
mxt_lm5 <-update(mxt_lm4, ~.-aspect)

drop1(mxt_lm5, test='Chisq')
mxt_lm6 <-update(mxt_lm5, ~.-TPI)

#no more dropable terms
drop1(mxt_lm6, test='Chisq')

mxt_null <- lmer(maxTemp ~ 1 + (1|riv_poi), data=df_lmer)

#now lets make some AIC tables for model selection  
# model table with bbmle/broom package
mxt_AICtab <- AICtab(mxt_lm1, mxt_lm2, mxt_lm3, mxt_lm4, mxt_lm5, mxt_lm6, mxt_null,
                     weights = TRUE, sort = T)
mxt_summ_table <- do.call(rbind, lapply(list(mxt_lm1, mxt_lm2, mxt_lm3, mxt_lm4, mxt_lm5,
                                             mxt_lm6, mxt_null), broom::glance))
mxt_AICtab[["Resid.Dev"]] <- mxt_summ_table[["deviance"]]
mxt_AICtab

## all 7 the same

# # without Hmean_log
# mxt_lm1 <- lmer(maxTemp ~ TPI + slope + aspect + PAI_log + LandUse + (1|riv_poi), data=df_lmer)
# 
# drop1(mxt_lm1, test='Chisq')
# mxt_lm2 <- update(mxt_lm1, ~.-slope)
# 
# drop1(mxt_lm2, test='Chisq')
# mxt_lm3 <- update(mxt_lm2, ~.-aspect)
# 
# drop1(mxt_lm3, test='Chisq')
# mxt_lm4 <- update(mxt_lm3, ~.-TPI)
# 
# drop1(mxt_lm4, test='Chisq')
# 
# mxt_null <- lmer(maxTemp ~ 1 + (1|riv_poi), data=df_lmer)
# 
# mxt_AICtab <- AICtab(mxt_lm1, mxt_lm2, mxt_lm3, mxt_lm4, mxt_null,
#                      weights = TRUE, sort = T)
# mxt_summ_table <- do.call(rbind, lapply(list(mxt_lm1, mxt_lm2, mxt_lm3, mxt_lm4, mxt_null), broom::glance))
# mxt_AICtab[["Resid.Dev"]] <- mxt_summ_table[["deviance"]]
# mxt_AICtab
# 
# # all equivalent

###############
## meanT LME ##
###############

mnt_lm1 <- lmer(meanTemp ~ TPI + slope + aspect + PAI_log + Hmean_log + LandUse + Hmean_log:aspect + (1|riv_poi), data=df_lmer)

drop1(mnt_lm1, test='Chisq')
mnt_lm2 <- update(mnt_lm1, ~.-Hmean_log:aspect)

drop1(mnt_lm2, test='Chisq')
mnt_lm3 <- update(mnt_lm2, ~.-slope)

drop1(mnt_lm3, test='Chisq')
mnt_lm4 <- update(mnt_lm3, ~.-aspect)

drop1(mnt_lm4, test='Chisq')
mnt_lm5 <- update(mnt_lm4, ~.-TPI)

#no more terms to drop
drop1(mnt_lm5, test='Chisq')

#null model
mnt_null <- lmer(meanTemp ~ 1 + (1|riv_poi), data=df_lmer)

#now lets make some AIC tables for model selection  
# model table with bbmle/broom package
mnt_AICtab <- AICtab(mnt_lm1, mnt_lm2, mnt_lm3, mnt_lm4, mnt_lm5, mnt_null,
                     weights = TRUE, sort = T)
mnt_summ_table <- do.call(rbind, lapply(list(mnt_lm1, mnt_lm2, mnt_lm3, mnt_lm4, mnt_lm5, mnt_null), broom::glance))
mnt_AICtab[["Resid.Dev"]] <- mnt_summ_table[["deviance"]]
mnt_AICtab

##model 5 highly significant
summary(mnt_lm5)
# 
# #this is with Hmean_log removed
# mnt_lm1 <- lmer(meanTemp ~ TPI + slope + aspect + PAI_log + LandUse + (1|riv_poi), data=df_lmer)
# 
# drop1(mnt_lm1, test='Chisq')
# mnt_lm2 <- update(mnt_lm1, ~.-slope)
# 
# #no more terms to drop
# drop1(mnt_lm2, test='Chisq')
# 
# #null model
# mnt_null <- lmer(meanTemp ~ 1 + (1|riv_poi), data=df_lmer)
# 
# #now lets make some AIC tables for model selection
# # model table with bbmle/broom package
# mnt_AICtab <- AICtab(mnt_lm1, mnt_lm2, mnt_null,
#                      weights = TRUE, sort = T)
# mnt_summ_table <- do.call(rbind, lapply(list(mnt_lm1, mnt_lm2, mnt_null), broom::glance))
# mnt_AICtab[["Resid.Dev"]] <- mnt_summ_table[["deviance"]]
# mnt_AICtab
# 
# # both models equivalent

### max VPD ###

mxv_lm1 <- lmer(maxVPD ~ TPI + slope + aspect + PAI_log + Hmean_log + LandUse + Hmean_log:aspect + (1|riv_poi), data=df_lmer)

drop1(mxv_lm1, test='Chisq')
mxv_lm2 <- update(mxv_lm1, ~.-slope)

drop1(mxv_lm2, test='Chisq')
mxv_lm3 <- update(mxv_lm2, ~.-aspect:Hmean_log)

drop1(mxv_lm3, test='Chisq')
mxv_lm4 <- update(mxv_lm3, ~.-aspect)

drop1(mxv_lm4, test='Chisq')
mxv_lm5 <- update(mxv_lm4, ~.-Hmean_log)

drop1(mxv_lm5, test='Chisq')
mxv_lm6 <- update(mxv_lm5, ~.-TPI)

#no more drops
drop1(mxv_lm6, test='Chisq')

#null model
mxv_null <- lmer(maxVPD ~ 1 + (1|riv_poi), data = df_lmer)

#AIC tables
mxv_AICtab <- AICtab(mxv_lm1, mxv_lm2, mxv_lm3, mxv_lm4, mxv_lm5, mxv_lm6, mxv_null,
                     weights = TRUE, sort = T)
mxv_summ_table <- do.call(rbind, lapply(list(mxv_lm1, mxv_lm2, mxv_lm3, mxv_lm4, mxv_lm5, mxv_lm6, mxv_null), broom::glance))
mxv_AICtab[["Resid.Dev"]] <- mxv_summ_table[["deviance"]]
mxv_AICtab

# full model best

# # without Hmean
# mxv_lm1 <- lmer(maxVPD ~ TPI + slope + aspect + PAI_log + LandUse + (1|riv_poi), data=df_lmer)
# 
# drop1(mxv_lm1, test='Chisq')
# mxv_lm2 <- update(mxv_lm1, ~.-aspect)
# 
# drop1(mxv_lm2, test='Chisq')
# mxv_lm3 <- update(mxv_lm2, ~.-slope)
# 
# drop1(mxv_lm3, test='Chisq')
# mxv_lm4 <- update(mxv_lm3, ~.-TPI)
# 
# drop1(mxv_lm4, test='Chisq')
# 
# 
# #null model
# mxv_null <- lmer(maxVPD ~ 1 + (1|riv_poi), data = df_lmer)
# 
# #AIC tables
# mxv_AICtab <- AICtab(mxv_lm1, mxv_lm2, mxv_lm3, mxv_lm4, mxv_null,
#                      weights = TRUE, sort = T)
# mxv_summ_table <- do.call(rbind, lapply(list(mxv_lm1, mxv_lm2, mxv_lm3, mxv_lm4, mxv_null), broom::glance))
# mxv_AICtab[["Resid.Dev"]] <- mxv_summ_table[["deviance"]]
# mxv_AICtab
# 
# # 1 and 2 equivalent

### mean VPD ###

mnv_lm1 <- lmer(meanVPD ~ TPI + slope + aspect + PAI_log + Hmean_log + LandUse + Hmean_log:aspect + (1|riv_poi), data=df_lmer)

drop1(mnv_lm1, test='Chisq')
mnv_lm2 <- update(mnv_lm1, ~.-slope)

drop1(mnv_lm2, test='Chisq')
mnv_lm3 <- update(mnv_lm2, ~.-aspect:Hmean_log)

drop1(mnv_lm3, test='Chisq')
mnv_lm4 <- update(mnv_lm3, ~.-aspect)

drop1(mnv_lm4, test='Chisq')
mnv_lm5 <- update(mnv_lm4, ~.-TPI)

drop1(mnv_lm5, test='Chisq')
mnv_lm6 <- update(mnv_lm5, ~.-Hmean_log)

#no more variables to drop
drop1(mnv_lm6, test='Chisq')

#null model
mnv_null <- lmer(meanVPD ~ 1 + (1|riv_poi), data=df_lmer)

#AIC tables
mnv_AICtab <- AICtab(mnv_lm1, mnv_lm2, mnv_lm3, mnv_lm4, mnv_lm5, mnv_lm6, mnv_null,
                     weights = TRUE, sort = T)
mnv_summ_table <- do.call(rbind, lapply(list(mnv_lm1, mnv_lm2, mnv_lm3, mnv_lm4, mnv_lm5, mnv_lm6, mnv_null),
                                        broom::glance))
mnv_AICtab[["Resid.Dev"]] <- mnv_summ_table[["deviance"]]
mnv_AICtab

#models 5 and 6 best
summary(mnv_lm5)
summary(mnv_lm6)

#now with no Hmean
# 
# mnv_lm1 <- lmer(meanVPD ~ TPI + slope + aspect + PAI_log + LandUse + (1|riv_poi), data=df_lmer)
# 
# drop1(mnv_lm1, test='Chisq')
# mnv_lm2 <- update(mnv_lm1, ~.-slope)
# 
# drop1(mnv_lm2, test='Chisq')
# mnv_lm3 <- update(mnv_lm2, ~.-aspect)
# 
# drop1(mnv_lm3, test='Chisq')
# mnv_lm4 <- update(mnv_lm3, ~.-TPI)
# 
# #no more variables to drop
# drop1(mnv_lm4, test='Chisq')
# 
# #null model
# mnv_null <- lmer(meanVPD ~ 1 + (1|riv_poi), data=df_lmer)
# 
# #AIC tables
# mnv_AICtab <- AICtab(mnv_lm1, mnv_lm2, mnv_lm3, mnv_lm4, mnv_null,
#                      weights = TRUE, sort = T)
# mnv_summ_table <- do.call(rbind, lapply(list(mnv_lm1, mnv_lm2, mnv_lm3, mnv_lm4, mnv_null),
#                                         broom::glance))
# mnv_AICtab[["Resid.Dev"]] <- mnv_summ_table[["deviance"]]
# mnv_AICtab
# 
# #models 4 and 3 top 
# summary(mnv_lm3)
# summary(mnv_lm4)

######################
######################
##### GRAPH TIME #####
######################
######################

#graphs of all variables for maxTemp

mxt_TPI <- ggplot(df_lmer, aes(x = TPI, y = maxTemp)) +
  labs(x = 'Topographic Position Index', y = expression(paste('Max Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  geom_abline(aes(intercept=`(Intercept)`, slope=TPI), as.data.frame(t(fixef(mxt_lm1))))

mxt_Hmean_log<- ggplot(df_lmer, aes(x = Hmean_log, y = maxTemp)) +
  labs(x = 'log(Mean Canopy Height)', y = expression(paste('Max Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  geom_abline(aes(intercept=`(Intercept)`, slope=Hmean_log), as.data.frame(t(fixef(mxt_lm1))))

mxt_PAI_log <- ggplot(df_lmer, aes(x = PAI_log, y = maxTemp)) +
  labs(x = 'log(Mean Plant Area Index)', y = expression(paste('Max Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  geom_abline(aes(intercept=`(Intercept)`, slope=PAI_log), as.data.frame(t(fixef(mxt_lm1))))

mxt_aspect <- ggplot(df_lmer, aes(x = aspect, y = maxTemp)) +
  labs(x = 'Aspect', y = expression(paste('Max Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  geom_abline(aes(intercept=`(Intercept)`, slope=aspect), as.data.frame(t(fixef(mxt_lm1))))

mxt_slope <- ggplot(df_lmer, aes(x = slope, y = maxTemp)) +
  labs(x = 'Slope', y = expression(paste('Max Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  geom_abline(aes(intercept=`(Intercept)`, slope=slope), as.data.frame(t(fixef(mxt_lm1))))

mxt_LandUse <- ggplot(df_lmer, aes(x = LandUse, y = maxTemp)) +
  geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5) +
  geom_boxplot(aes(fill=LandUse),width=0.01,lwd=1) + 
  theme_bw() +
  labs(y = expression(paste('Max Temperature (',degree,"C)"))) + 
  labs(x='Land Use')+
  theme(axis.line = element_line(size = 0.5, linetype = "solid")) +
  theme(legend.position="none") + 
  scale_fill_manual(values=alpha(c("gray","gray","gray"),0.8)) +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

grid.arrange(mxt_TPI, mxt_PAI_log, mxt_Hmean_log, mxt_slope, mxt_aspect, mxt_LandUse, nrow = 2)

### meanTemp ###

mnt_Hmean<- ggplot(df_lmer, aes(x = Hmean_log, y = meanTemp)) +
  labs(x = 'Maximum Canopy Height', y = expression(paste('Mean Temperature (',degree,"C)"))) +
  geom_point() +
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) 
