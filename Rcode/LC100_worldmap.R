##############################################################################################
##################################### 100LC: WORLDMAP ########################################
##############################################################################################

# Author: Chris
# Date: 28/02/2019
# R version: 
# Linux version: 18.04 LTS

#LOAD LIBRARIES
library(sf)
library(mapview)
library(tmap)

#READ DATA
lang.info <- read.csv(file.choose()) #progress_100LC.csv

#SIMPLE STATS
nrow(lang.info)#100
sum(lang.info$number_of_tokens, na.rm = T)# overall number of estimated tokens

#transform data frame to simple features object with point coordinates
lang.info.sf <- st_as_sf(lang.info, coords = c("longitude", "latitude"), crs = 4326)

#simple map view with locations
mapview(lang.info.sf)

data(World, lang.info.sf)
#flexible tmap 
tmap_mode("view")
tm_shape(World) +
tm_text(text = "iso_a3", size = 0) +
tm_shape(lang.info.sf) +
tm_dots(col = "status", 
        popup.vars = c("name_wals", "status", 
                      "number_of_texts", "number_of_genera", "number_of_tokens"),
        legend.format = list(format = "f", digits = 0),
        size = 0.1)
