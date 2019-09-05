#stats script for the datalogger data summarised by day

setwd('/home/joe/Documents/Dataloggers/Data/Final')
library(ggplot2)
library(gridExtra)
library(lme4)
library(anytime)
library(mgcv)

df<-read.csv('Combined_Daily_scale_12.5.csv')
str(df)

#set some of the variables as the correct type
df$Point<-as.factor(df$Point)
df$loggerID<-as.factor(df$loggerID)
str(df$Date)
df$Date<-as.Date(df$Date,format="%d/%m/%Y")
df<-subset(df,df$Position!='cavity')
df$Position<-factor(df$Position, levels = c('buffer5m','buffer15m','bufferedge','buffer25m',
                                             'buffer35m','buffer45m','op5m','op15m','op25m',
                                             'op35m','op45m'),ordered=TRUE)



#unique variable for every point, can test how many datapoints have been dropped by removing outliers
df$combo<-as.factor(paste(df$River,df$Point,df$Position))

#lets get rid of outliers and look at the histogram for max temp
#par(mfrow=c(1,3))
#hist(df$maxTemp)
df1<-subset(df,df$combo!='RR8 5 op25m')
#hist(df1$maxTemp)
df2<-subset(df1,df1$combo!='RR2 8 buffer15m')
#hist(df2$maxTemp)

df1<-df2
df2<-subset(df1,df1$combo!='RR14 8 op5m')
#hist(df$maxTemp)
#hist(df1$maxTemp)
#hist(df2$maxTemp)

df1<-df2
df2<-subset(df1,df1$combo!='SJI1 8 buffer5m')
#hist(df$maxTemp)
#hist(df1$maxTemp)
#hist(df2$maxTemp)

df1<-df2
df2<-subset(df1,df1$combo!='RR12 2 op25m')
#hist(df$maxTemp)
#hist(df1$maxTemp)
#hist(df2$maxTemp)

df1<-df2
df2<-subset(df1,df1$combo!='RR3 8 bufferedge')
#hist(df$maxTemp)
#hist(df1$maxTemp)
#hist(df2$maxTemp)
df<-df2

###now lets do some models
###some code for a GAMM
df$RiverPoint<-as.factor(paste(df$River,df$Point))
df$RiverPointPosition<-as.factor(paste(df$River,df$Point,df$Position))


maxTempGAMM1<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   family=gaussian(link=identity),data=df)

summary(maxTempGAMM1$gam)

plot(maxTempGAMM1$gam, scale = 0)
#overfitted

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM1$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM1$lme), lag.max = 36, main = "pACF")
layout(1)
#quite high autocorrelation

#lets add in year
maxTempGAMM2<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 1),
                   family=gaussian(link=identity),data=df)
summary(maxTempGAMM2$gam)

plot(maxTempGAMM2$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)


maxTempGAMM3<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 2),
                   family=gaussian(link=identity),data=df)
summary(maxTempGAMM3$gam)

plot(maxTempGAMM3$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM3$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM3$lme), lag.max = 36, main = "pACF")
layout(1)

maxTempGAMM4<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 3),
                   family=gaussian(link=identity),data=df)
summary(maxTempGAMM4$gam)

plot(maxTempGAMM4$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM4$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM4$lme), lag.max = 36, main = "pACF")
layout(1)

maxTempGAMM5<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 4),
                   family=gaussian(link=identity),data=df)
summary(maxTempGAMM5$gam)

plot(maxTempGAMM5$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM5$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM5$lme), lag.max = 36, main = "pACF")
layout(1)

#fails to converge once p = 5
maxTempGAMM6<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 1),
                   family=gaussian(link=identity),data=df)
summary(maxTempGAMM6$gam)

anova(maxTempGAMM1$lme,maxTempGAMM2$lme,maxTempGAMM3$lme,maxTempGAMM4$lme,maxTempGAMM5$lme)
anova(maxTempGAMM2$lme,maxTempGAMM3$lme,maxTempGAMM4$lme,maxTempGAMM5$lme)
anova(maxTempGAMM3$lme,maxTempGAMM4$lme,maxTempGAMM5$lme)
anova(maxTempGAMM4$lme,maxTempGAMM5$lme)

#maxTempGAMM5 is our winner, this is our maximal model for land use
#lets start trying to remove random factors

maxTempGAMM8<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                        random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                                 correlation = corARMA(form = ~ 1|year, p = 1),
                                 family=gaussian(link=identity),data=df)
summary(maxTempGAMM8$gam)
#alot worse

#cant remove random effects
anova(maxTempGAMM5$lme,maxTempGAMM8$lme)

#GAMM5 our best model.
#generate GAMM5.1 to also look at diff between RR and OP 
df$LandUse<-relevel(df$LandUse,ref='RR')
maxTempGAMM5.1<-gamm(maxTemp~LandUse+s(date_minus_year, bs = "cc"),
                       random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                       correlation = corARMA(form = ~ 1|year, p = 4),
                       family=gaussian(link=identity),data=df)
summary(maxTempGAMM5.1$gam)
df$LandUse<-relevel(df$LandUse,ref='CF')

#check 5 and 5.1 are the same model
anova(maxTempGAMM5.1$lme,maxTempGAMM5$lme)
#they are so lets get the summary stats up for both
summary(maxTempGAMM5$gam)
summary(maxTempGAMM5.1$gam)

###lets do meanTemp

meanTempGAMM1<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   family=gaussian(link=identity),data=df)

summary(meanTempGAMM1$gam)

plot(meanTempGAMM1$gam, scale = 0)
#overfitted

layout(matrix(1:2, ncol = 2))
acf(resid(meanTempGAMM1$lme), lag.max = 36, main = "ACF")
pacf(resid(meanTempGAMM1$lme), lag.max = 36, main = "pACF")
layout(1)
#quite high autocorrelation

#lets add in year
meanTempGAMM2<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 1),
                   family=gaussian(link=identity),data=df)
summary(meanTempGAMM2$gam)

plot(meanTempGAMM2$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(meanTempGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(meanTempGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)


meanTempGAMM3<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 2),
                   family=gaussian(link=identity),data=df)
summary(meanTempGAMM3$gam)

plot(meanTempGAMM3$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(meanTempGAMM3$lme), lag.max = 36, main = "ACF")
pacf(resid(meanTempGAMM3$lme), lag.max = 36, main = "pACF")
layout(1)

meanTempGAMM4<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 3),
                   family=gaussian(link=identity),data=df)
summary(meanTempGAMM4$gam)

plot(meanTempGAMM4$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(meanTempGAMM4$lme), lag.max = 36, main = "ACF")
pacf(resid(meanTempGAMM4$lme), lag.max = 36, main = "pACF")
layout(1)

meanTempGAMM5<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   correlation = corARMA(form = ~ 1|year, p = 4),
                   family=gaussian(link=identity),data=df)
summary(meanTempGAMM5$gam)

meanTempGAMM6<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 5),
                  family=gaussian(link=identity),data=df)
summary(meanTempGAMM6$gam)


anova(meanTempGAMM1$lme,meanTempGAMM2$lme,meanTempGAMM3$lme,meanTempGAMM4$lme,
      meanTempGAMM5$lme,meanTempGAMM6$lme)

#meantemp5 is our goer, lets try taking out terms

meanTempGAMM7<-gamm(meanTemp~LandUse,
                    random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                    correlation = corARMA(form = ~ 1|year, p = 5),
                    family=gaussian(link=identity),data=df)
summary(meanTempGAMM7$gam)
#nope
anova(meanTempGAMM6$lme,meanTempGAMM7$lme)

meanTempGAMM8<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                    random=list(River = ~1,RiverPoint=~1),
                    correlation = corARMA(form = ~ 1|year, p = 5),
                    family=gaussian(link=identity),data=df)
summary(meanTempGAMM8$gam)
#nope
anova(meanTempGAMM6$lme,meanTempGAMM8$lme)


#GAMM5 our best model.
#generate GAMM5.1 to also look at diff between RR and OP 
df$LandUse<-relevel(df$LandUse,ref='RR')
meanTempGAMM5.1<-gamm(meanTemp~LandUse+s(date_minus_year, bs = "cc"),
                     random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                     correlation = corARMA(form = ~ 1|year, p = 4),
                     family=gaussian(link=identity),data=df)
summary(meanTempGAMM5.1$gam)
df$LandUse<-relevel(df$LandUse,ref='CF')

#check 5 and 5.1 are the same model
anova(meanTempGAMM5.1$lme,meanTempGAMM5$lme)
#they are so lets get the summary stats up for both
summary(meanTempGAMM5$gam)
summary(meanTempGAMM5.1$gam)



#lets go for some maxVPD

maxVPDGAMM1<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                   family=gaussian(link=identity),data=df)

summary(maxVPDGAMM1$gam)

plot(maxVPDGAMM1$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxVPDGAMM1$lme), lag.max = 36, main = "ACF")
pacf(resid(maxVPDGAMM1$lme), lag.max = 36, main = "pACF")
layout(1)


maxVPDGAMM2<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 1),
                  family=gaussian(link=identity),data=df)

summary(maxVPDGAMM2$gam)

plot(maxVPDGAMM2$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(maxVPDGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(maxVPDGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)

maxVPDGAMM3<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 2),
                  family=gaussian(link=identity),data=df)
summary(maxVPDGAMM3$gam)

maxVPDGAMM4<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p =3),
                  family=gaussian(link=identity),data=df)
summary(maxVPDGAMM4$gam)

maxVPDGAMM5<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 4),
                  family=gaussian(link=identity),data=df)
summary(maxVPDGAMM5$gam)

maxVPDGAMM6<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 5),
                  family=gaussian(link=identity),data=df)
summary(maxVPDGAMM6$gam)

maxVPDGAMM7<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 6),
                  family=gaussian(link=identity),data=df)
summary(maxVPDGAMM7$gam)


anova(maxVPDGAMM1$lme,maxVPDGAMM2$lme,maxVPDGAMM3$lme,maxVPDGAMM4$lme,
      maxVPDGAMM5$lme,maxVPDGAMM6$lme)

#5 is just about significant, lets stick with 4

df$LandUse<-relevel(df$LandUse,ref='RR')
maxVPDGAMM4.1<-gamm(maxVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 3),
                  family=gaussian(link=identity),data=df)
df$LandUse<-relevel(df$LandUse,ref='CF')
summary(maxVPDGAMM4$gam)
summary(maxVPDGAMM4.1$gam)

###lets have a look at meanVPD

meanVPDGAMM1<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  family=negative.binomial(p=2),data=df)

summary(meanVPDGAMM1$gam)

plot(meanVPDGAMM1$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(meanVPDGAMM1$lme), lag.max = 36, main = "ACF")
pacf(resid(meanVPDGAMM1$lme), lag.max = 36, main = "pACF")
layout(1)


meanVPDGAMM2<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 1),
                  family=gaussian(link=identity),data=df)

summary(meanVPDGAMM2$gam)

plot(meanVPDGAMM2$gam, scale = 0)

layout(matrix(1:2, ncol = 2))
acf(resid(meanVPDGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(meanVPDGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)

meanVPDGAMM3<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 2),
                  family=gaussian(link=identity),data=df)
summary(meanVPDGAMM3$gam)

meanVPDGAMM4<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p =3),
                  family=gaussian(link=identity),data=df)
summary(meanVPDGAMM4$gam)

meanVPDGAMM5<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 4),
                  family=gaussian(link=identity),data=df)
summary(meanVPDGAMM5$gam)

meanVPDGAMM6<-gamm(meanVPD~LandUse+s(date_minus_year, bs = "cc"),
                  random=list(River = ~1,RiverPoint=~1,RiverPointPosition=~1),
                  correlation = corARMA(form = ~ 1|year, p = 5),
                  family=gaussian(link=identity),data=df)
summary(meanVPDGAMM6$gam)




#lets do 15m and buffer datasets only
df15m<-subset(df,df$Position=='buffer15m'|df2$Position=='op15m')
dfrr<-subset(df,df$LandUse!='CF' & df2$River!='ROP2' & df2$River!='ROP10')
dfrr$LUPos<-as.factor(paste(dfrr$LandUse,dfrr$Position))
dfrr<-subset(dfrr,dfrr$LUPos!='OP buffer5m' & dfrr$LUPos!='OP buffer15m' & dfrr$LUPos!='OP bufferedge')
str(dfrr$LUPos)

###what makes buffers good?
dfrr_lidar<-subset(dfrr,is.na(dfrr$canopy_height_mean)==F)

###########
###########
LIDAR DATA JUST LOOKING AT THE RIPARIAN BUFFERS
###########
###########

lidarmaxTempGAMM1<-gamm(maxTemp~canopy_height_mean+kurt_mean+pai_mean+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1, RiverPoint=~1),
                   family=gaussian(link=identity),data=dfrr)
summary(lidarmaxTempGAMM1$gam)

plot(lidarmaxTempGAMM1$gam)
layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)

lm1=lmer(maxTemp~canopy_height_mean+kurt_mean+pai_mean+(1|River)+
       (1|RiverPoint),data=dfrr)
summary(lm1)
anova(lm1)




maxTempGAMM1<-gamm(maxTemp~Distance_from_edge+s(date_minus_year, bs = "cc"),
                   random=list(River = ~1,RiverPoint=~1),
                   family=gaussian(link=identity),data=dfrr_lidar)
summary(maxTempGAMM2$gam)

layout(matrix(1:2, ncol = 2))
acf(resid(maxTempGAMM2$lme), lag.max = 36, main = "ACF")
pacf(resid(maxTempGAMM2$lme), lag.max = 36, main = "pACF")
layout(1)


bufferwidth1<-lmer(minTemp~width+(1|River)+(1|PointCombo), data=subset(dfrr,df$Position=='buffer5m')) 
bw1_summary=summary(bufferwidth1)
bw1_summary
bw1_summary$coefficients
CI <- bw1_summary$coefficient[,"Std. Error"]*1.96
print(CI)
par(mfrow=c(1,1))
plot(fitted(maxTemp1), residuals(maxTemp1))

par(mfrow=c(1,1))
plot(df$Distance_from_river,df$maxTemp)
lm1<-lm(minVPD~Distance_from_river, data=subset(df2, df2$Distance_from_river<200))
summary(lm1)

df3<-subset(df2,df2$Position=='buffer5m'|df2$Position=='op5m')

dfrr$LandUse <- factor(dfrr$LandUse,levels = c('RR', 'OP'),ordered = TRUE)
df$LandUse <- factor(df$LandUse,levels = c('CF','RR', 'OP'),ordered = TRUE)

#### violin plots by landuse 

viol <- ggplot(df, aes(LandUse, maxTemp))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot1<-viol + scale_fill_manual(values=alpha(c("forestgreen",'olivedrab3',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'olivedrab3',"saddlebrown")) + theme_bw() +
  labs(y = expression(paste('Max Daily Temperature (',degree,"C)"))) + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol2 <- ggplot(df, aes(LandUse, meanTemp))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot2<-viol2 + scale_fill_manual(values=alpha(c("forestgreen",'olivedrab3',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'olivedrab3',"saddlebrown")) + theme_bw() +
  labs(y = expression(paste('Mean Daily Temperature (',degree,"C)"))) + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol3 <- ggplot(df, aes(LandUse, maxVPD))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot3<-viol3 + scale_fill_manual(values=alpha(c("forestgreen",'olivedrab3',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'olivedrab3',"saddlebrown")) + theme_bw() +
  labs(y = 'Max VPD (hPA)') + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol4 <- ggplot(df, aes(LandUse, meanVPD))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot4<-viol4 + scale_fill_manual(values=alpha(c( "forestgreen",'olivedrab3',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'olivedrab3',"saddlebrown")) + theme_bw() +
  labs(y = 'Mean VPD (hPA)') + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

grid.arrange(plot1, plot2, plot3,plot4, nrow = 2)

####daily bins graphs

viol <- ggplot(df3, aes(LandUseBins, maxTemp))+ geom_violin(aes(fill=LandUseBins),lwd=0.7,width=0.5)
plot1<-viol + scale_fill_manual(values=alpha(c("forestgreen",'green',"saddlebrown",'yellow','grey','pink'),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'green',"saddlebrown",'red','yellow','blue')) + theme_bw() +
  labs(y = expression(paste('Max Daily Temperature (',degree,"C)"))) + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol2 <- ggplot(df2, aes(LandUseBins, meanTemp))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot2<-viol2 + scale_fill_manual(values=alpha(c("forestgreen",'green',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'green',"saddlebrown")) + theme_bw() +
  labs(y = expression(paste('Mean Daily Temperature (',degree,"C)"))) + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol3 <- ggplot(df2, aes(LandUseBins, maxVPD))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot3<-viol3 + scale_fill_manual(values=alpha(c("forestgreen",'green',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'green',"saddlebrown")) + theme_bw() +
  labs(y = 'Max VPD (hPA)') + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

viol4 <- ggplot(df2, aes(LandUseBins, meanVPD))+ geom_violin(aes(fill=LandUse),lwd=0.7,width=0.5)
plot4<-viol4 + scale_fill_manual(values=alpha(c( "forestgreen",'olivedrab3',"saddlebrown"),0.5)) + geom_boxplot(width=0.01,lwd=1,colour=c("forestgreen",'olivedrab3',"saddlebrown")) + theme_bw() +
  labs(y = 'Mean VPD (hPA)') + theme(legend.position="none")+ 
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

grid.arrange(plot1, plot2, plot3,plot4, nrow = 2)
  
distance1<- ggplot(dfrr, aes(Position, maxTemp))+ geom_violin(aes(fill=dfrr$LandUse),lwd=0.7,width=0.5)+
  scale_fill_manual(values=alpha(c("saddlebrown",'olivedrab3'),0.5))+
  geom_boxplot(width=0.01,lwd=1, colour=c('olivedrab3','olivedrab3','olivedrab3',"saddlebrown","saddlebrown"))+
  theme_bw() +
  theme(legend.position="none")+
  labs(y = expression(paste('Max Daily Temperature (',degree,"C)")))+
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+ 
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+ 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

distance2<- ggplot(dfrr, aes(Position, meanTemp))+ geom_violin(aes(fill=dfrr$LandUse),lwd=0.7,width=0.5)+
  scale_fill_manual(values=alpha(c("saddlebrown",'olivedrab3'),0.5))+
  geom_boxplot(width=0.01,lwd=1, colour=c('olivedrab3','olivedrab3','olivedrab3',"saddlebrown","saddlebrown"))+
  theme_bw() +
  theme(legend.position="none")+ 
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+
  labs(y = expression(paste('Mean Daily Temperature (',degree,"C)")))+
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+ 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

distance3<- ggplot(dfrr, aes(Position, maxVPD))+ geom_violin(aes(fill=dfrr$LandUse),lwd=0.7,width=0.5)+
  scale_fill_manual(values=alpha(c("saddlebrown",'olivedrab3'),0.5))+
  geom_boxplot(width=0.01,lwd=1, colour=c('olivedrab3','olivedrab3','olivedrab3',"saddlebrown","saddlebrown"))+
  theme_bw() +
  theme(legend.position="none")+ 
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+
  labs(y = 'Mean Daily VPD (hPa)')+
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+ 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

distance4 <- ggplot(dfrr, aes(Position, meanVPD))+ geom_violin(aes(fill=dfrr$LandUse),lwd=0.7,width=0.5)+
  scale_fill_manual(values=alpha(c("saddlebrown",'olivedrab3'),0.5))+
  geom_boxplot(width=0.01,lwd=1, colour=c('olivedrab3','olivedrab3','olivedrab3',"saddlebrown","saddlebrown"))+
  theme_bw() + 
  theme(legend.position="none")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))+
  labs(y = 'Max Daily VPD (hPa)')+
  labs(x='Land Use')+
  theme( axis.line = element_line(size = 0.5, linetype = "solid"))+ 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank()) +
  stat_summary(fun.y=median, geom="point", size=2, color="white")

grid.arrange(distance1, distance2, distance4,distance3, nrow = 2)

distance1

dfsubset<-subset(df,df$LandUse!='CF'&df$LandUse!='OP')
df$River<-as.factor(df$River)
tapply(dfsubset$maxTemp,INDEX=dfsubset$River,FUN="mean")
tapply(dfsubset$width,INDEX=dfsubset$River,FUN='mean')
