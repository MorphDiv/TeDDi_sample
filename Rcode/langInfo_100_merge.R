#####################################################################################
###################### 100LC MERGE LANGUAGE INFORMATION #############################
#####################################################################################

#Author(s): Chris Bentz
#Latest change: 11/10/2018 (day/month/year)
#R version 3.2.3 "Wooden Christmas-Tree"
#Operating System: Ubuntu 14.04.3 LTS
#Kernel: Linux 3.13.0-74-generic
#Architecture: i686


### LOAD DATA FILES ###

#WALS information
wals <- read.csv("/home/chris/Dropbox/100LC/LangData/WALS/WALS_languages.csv", header = T)
#Glottolog information
glotto.languages <- read.csv("/home/chris/Dropbox/100LC/LangData/Glottolog3.3/glottolog3.3_languages_and_dialects_geo.csv", header = T)
glotto.languoids <- read.csv("/home/chris/Dropbox/100LC/LangData/Glottolog3.3/glottolog3.3_languoid.csv", header = T)

### WALS INFO ###

#select languages of the 100 language sample
wals.100 <- wals[wals$sample.100 == "True", ]

#select columns with language information in WALS file
wals.100.short <- wals.100[, 1:8]

#rename columns
colnames(wals.100.short) <- c("wals.code", "glottocode", "name_wals", "latitude_wals", "longitude_wals", 
                              "macroarea_wals", "genus_wals", "family_wals")


### GLOTTOLOG INFO ###

#Glottolog language information
#select languages in the 100 language sample by glottocode
glotto.lang.100 <- glotto.languages[glotto.languages$glottocode %in% wals.100.short$glottocode, ]

#Glottolog languoid information (to get top level families)
glotto.languoids.100 <- glotto.languoids[glotto.languoids$id %in% wals.100.short$glottocode, ]
#select particular columns of languoid data frame
keeps <- c("id", "family_id", "status")
glotto.languoids.100.short <- glotto.languoids.100[keeps]

#merge language information and languoid information
glotto.lang.languoids.100 <- merge(glotto.lang.100, glotto.languoids.100.short, by.x = "glottocode", by.y = "id")

#select only families from languoid information to get family names per language
#NOTE: family_id has to be empty in order to find macrofamilies! (for whatever reason)
glotto.families <- glotto.languoids[glotto.languoids$level == "family" & glotto.languoids$family_id == "",]
keeps <- c("id", "name")
glotto.families.short <- glotto.families[keeps]
#rename column "name" 
colnames(glotto.families.short) <- c("id", "top_level_family")

#separate earlier dataset by languages with and without family_id. This is necessary to merge 
#with top_level_family names
glotto.langInfo.withFamID <- glotto.lang.languoids.100[glotto.lang.languoids.100$family_id != "",]
glotto.langInfo.noFamID <- glotto.lang.languoids.100[glotto.lang.languoids.100$family_id == "",]

#merge language info with family names only for subset with family ids
glotto.langInfo.fam <- merge(glotto.langInfo.withFamID, glotto.families.short, by.x = "family_id", by.y ="id")

#add NA column "top_level_family" to languages without family_id
glotto.langInfo.noFamID$top_level_family <- rep("NA", nrow(glotto.langInfo.noFamID))

#create dataset with all 100 languages and language info from glottolog
glotto.langInfo.100 <- rbind(glotto.langInfo.fam, glotto.langInfo.noFamID)

#rename columns
colnames(glotto.langInfo.100) <- c("family_id", "glottocode", "name_glotto", "iso_639_3", "level", 
                                   "macroarea_glotto", "latitude_glotto", "longitude_glotto", "status", "top_level_family")


#### COMBINE WALS AND GLOTTOLOG INFORMATION ####

#merge
langInfo.100 <- merge(wals.100.short, glotto.langInfo.100, by = "glottocode")

#reorder columns
#reorder columns
langInfo.100 <- langInfo.100[ , c(11, 1, 2, 10, 3, 12, 16, 9, 17, 7, 8, 13, 6, 14, 15, 4, 5)]

#write to file
write.csv(file = "~/Dropbox/100LC/LangData/langInfo_100.csv", langInfo.100, row.names = F)


