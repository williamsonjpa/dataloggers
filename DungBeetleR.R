setwd('C:/Users/hp/Documents/2018/Dataloggers/Data/Final')
df=read.csv('DBVegDataloggers.csv')

with(df,plot(meanTemp, O.borneensis))

str(df)

