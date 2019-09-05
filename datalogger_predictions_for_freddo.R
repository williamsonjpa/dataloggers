#### This script takes the datalogger data and microclimate raster predictions to predict temperatures for sites without lidar

library(raster)
library(rgdal)
library(openxlsx)

setwd('/home/joe/Documents/Dataloggers/Data/Final/')

#read in the combined dataframe with a 12.5m scale resolution
coords <- read.csv('Combined_Point_scale_12.5.csv')
str(coords)

#read in the 4 raster files
max_T <- raster('../../../Thermal/TJ_Projections/T_max_raster.tif')
mean_T <- raster('../../../Thermal/TJ_Projections/T_mean_raster.tif')
max_VPD <- raster('../../../Thermal/TJ_Projections/VPD_max_raster.tif')
mean_VPD <- raster('../../../Thermal/TJ_Projections/VPD_mean_raster.tif')


###################
# DATA PROCESSING #
###################

#remove rows where data
coords = coords[!is.na(coords$long),]
coords = coords[coords$Position!='cavity',]

#set the coordinates to a coordinates object
coords.col = SpatialPoints(cbind(coords$long,coords$lat), proj4string = CRS("+proj=longlat"))

#convert to UTM
coords.UTM <- spTransform(coords.col, CRS(projection(max_T)))

#save a new file of converted GPS points
coord_export <- data.frame(coords$River, coords$Point, coords$Position, coords.UTM)
write.csv(coord_export, 'Datalogger_Coordinates_UTM.csv')

#check the coordinates match up in plots
par(mfrow=c(1,2))
plot(coords.UTM,axes=T, pch=2, cex.axis=0.95)
plot(coords.col,axes=T, pch=2, col='red', cex.axis=0.95)

#stack them to extract from all 4 at once
microclimate_stack<-stack(max_T,mean_T,max_VPD,mean_VPD)
microclimate_values<-extract(microclimate_stack, coords.UTM)

#add the extracted data to the coords dataframe
coords_aligned<-data.frame(coords,microclimate_values)
write.csv(coords_aligned, '../../../Fredie/microclimate_match_up_fredie.csv')
