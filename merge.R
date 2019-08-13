setwd('C:/Users/hp/Documents/2018/Dataloggers/Data/Final')
library(lme4)
library(hms)
library(scales)
library(ggplot2)

df<-read.csv('merge2.csv')
str(df$width)

#set some of the variables as the correct type
df$Point<-as.factor(df$Point)
df$loggerID<-as.factor(df$loggerID)
df$LandUse <- factor(df$LandUse,levels = c('CF','RR', 'OP'),ordered = TRUE)
df$Date<-as.Date(df$DateTime)
df$Time<-as.POSIXct(strptime(df$Time, format="%H:%M:%S"))
df$Temp<-df$Celsius.C.


#unique variable for every point, can test how many datapoints have been dropped by removing outliers
df$combo<-as.factor(paste(df$River,df$Point,df$Position))

#lets get rid of outliers that we did from the daily data
df1<-subset(df,df$combo!='RR8 5 op25m')
df2<-subset(df1,df1$combo!='RR2 8 buffer15m')
df1<-df2
df2<-subset(df1,df1$combo!='RR14 8 op5m')
df1<-df2
df2<-subset(df1,df1$combo!='SJI1 8 buffer5m')
df1<-df2
df2<-subset(df1,df1$combo!='RR12 2 op25m')
df1<-df2
df2<-subset(df1,df1$combo!='RR3 8 bufferedge')
df<-df2



plot1<-ggplot(data = df,aes(x = Time, y = Celsius.C., colour = LandUse)) + geom_smooth()+
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_x_datetime(labels = date_format("%H:%M:%S"))+
  labs(y = expression(paste('Temperature (',degree,"C)")))+
  scale_fill_manual(values=alpha(c( "forestgreen",'green',"saddlebrown"),0.5)) 

plot1

plot2<-ggplot(data = df,aes(x = Time, y = VPD, colour = LandUse)) + geom_smooth()+
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_x_datetime(labels = date_format("%H:%M:%S")) +labs(y = 'VPD (hPA)')+
  scale_fill_manual(values=alpha(c( "forestgreen",'green',"saddlebrown"),0.5)) 

grid.arrange(plot1, plot2, nrow = 2)

dfsubset<-subset(df,df$LandUse!='CF'&df$LandUse!='OP')

dfsubset<-subset(df,df$LandUse!='CF'&df$LandUse!='OP')


plot3<-ggplot(data = dfsubset,aes(x = Time, y = VPD, colour = River)) + geom_smooth()+
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  scale_x_datetime(labels = date_format("%H:%M:%S")) +labs(y = 'VPD (hPA)')

plot3
