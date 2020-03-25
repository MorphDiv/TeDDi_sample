Merge language information for 100LC sources
================
Chris Bentz, Steven Moran
25 March, 2020

``` r
library(dplyr)
library(tidyr)
library(knitr)
```

Load and process the data
=========================

``` r
wals <- read.csv("Sources/WALS/WALS_languages.csv", header = T)
glotto.languages <- read.csv("Sources/Glottolog3.3/languages_and_dialects_geo.csv", header = T)
glotto.languoids <- read.csv("Sources/Glottolog3.3/languoid.csv", header = T)

# Select languages of the 100 language sample
wals.100 <- wals[wals$sample.100 == "True", ]

# Select columns with language information in WALS file
wals.100.short <- wals.100[, 1:8]

# Rename columns
colnames(wals.100.short) <- c("wals.code", "glottocode", "name_wals", "latitude_wals", "longitude_wals", "macroarea_wals", "genus_wals", "family_wals")

# Select languages in the 100 language sample by glottocode
glotto.lang.100 <- glotto.languages[glotto.languages$glottocode %in% wals.100.short$glottocode, ]

# Glottolog languoid information (to get top level families)
glotto.languoids.100 <- glotto.languoids[glotto.languoids$id %in% wals.100.short$glottocode, ]

# Select particular columns of languoid data frame
keeps <- c("id", "family_id", "status")
glotto.languoids.100.short <- glotto.languoids.100[keeps]

# Merge language information and languoid information
glotto.lang.languoids.100 <- merge(glotto.lang.100, glotto.languoids.100.short, by.x = "glottocode", by.y = "id")

# Select only families from languoid information to get family names per language
# NOTE: family_id has to be empty in order to find macrofamilies! (for whatever reason)
glotto.families <- glotto.languoids[glotto.languoids$level == "family" & glotto.languoids$family_id == "",]
keeps <- c("id", "name")
glotto.families.short <- glotto.families[keeps]

# Rename column "name"
colnames(glotto.families.short) <- c("id", "top_level_family")

# Separate earlier dataset by languages with and without family_id. This is necessary to merge with top_level_family names
glotto.langInfo.withFamID <- glotto.lang.languoids.100[glotto.lang.languoids.100$family_id != "",]
glotto.langInfo.noFamID <- glotto.lang.languoids.100[glotto.lang.languoids.100$family_id == "",]

# Merge language info with family names only for subset with family ids
glotto.langInfo.fam <- merge(glotto.langInfo.withFamID, glotto.families.short, by.x = "family_id", by.y ="id")

# Add NA column "top_level_family" to languages without family_id
glotto.langInfo.noFamID$top_level_family <- rep("NA", nrow(glotto.langInfo.noFamID))

# Create dataset with all 100 languages and language info from glottolog
glotto.langInfo.100 <- rbind(glotto.langInfo.fam, glotto.langInfo.noFamID)

# Rename columns
colnames(glotto.langInfo.100) <- c("family_id", "glottocode", "name_glotto", "iso_639_3", "level", "macroarea_glotto", "latitude_glotto", "longitude_glotto", "status", "top_level_family")
```

Get folders from Corpus directory
=================================

``` r
# This is pretty ugly, but it works
fils <- tibble(folder=list.dirs(path = "../Corpus", full.names = FALSE, recursive = FALSE))
folders <- fils %>% separate(folder, c("folder_language_name", "iso_639_3"), sep="_(?=[a-z]{3}$)")
folders$folder_name <- paste(folders$folder_language_name, folders$iso_639_3, sep="_")
kable(head(folders))
```

| folder\_language\_name | iso\_639\_3 | folder\_name          |
|:-----------------------|:------------|:----------------------|
| Abkhaz                 | abk         | Abkhaz\_abk           |
| Acoma                  | kjq         | Acoma\_kjq            |
| Alamblak               | amp         | Alamblak\_amp         |
| Amele                  | aey         | Amele\_aey            |
| Apurina                | apu         | Apurina\_apu          |
| Arabic\_Egyptian       | arz         | Arabic\_Egyptian\_arz |

Combine the various information sources
=======================================

``` r
# Merge
langInfo.100 <- merge(wals.100.short, glotto.langInfo.100, by = "glottocode")

# Reorder columns
langInfo.100 <- langInfo.100[ , c(11, 1, 2, 10, 3, 12, 16, 9, 17, 7, 8, 13, 6, 14, 15, 4, 5)]

# Merge in folder names
langInfo.100 <- left_join(langInfo.100, folders)
```

    ## Joining, by = "iso_639_3"

    ## Warning: Column `iso_639_3` joining factor and character vector, coercing into
    ## character vector

``` r
# Write to file
write.csv(file = "langInfo_100LC.csv", langInfo.100, row.names = F, quote=FALSE)
```

Which rows do not (yet) have file folders?
==========================================

``` r
kable(langInfo.100 %>% filter(is.na(folder_name)) %>% select(iso_639_3, glottocode, name_glotto, name_wals))
```

| iso\_639\_3 | glottocode | name\_glotto            | name\_wals      |
|:------------|:-----------|:------------------------|:----------------|
| gry         | barc1235   | Barclayville Grebo      | Grebo           |
| cku         | koas1236   | Koasati                 | Koasati         |
| ses         | koyr1242   | Koyraboro Senni Songhai | Koyraboro Senni |
| kgo         | kron1241   | Krongo                  | Krongo          |
| lkt         | lako1247   | Lakota                  | Lakhota         |
| lez         | lezg1247   | Lezgian                 | Lezgian         |
| mpc         | mang1381   | Mangarrayi              | Mangarrayi      |
| mni         | mani1292   | Manipuri                | Meithei         |
| mrc         | mari1440   | Maricopa                | Maricopa        |
| scs         | nort2942   | North Slavey            | Slave           |
| one         | onei1249   | Oneida                  | Oneida          |
| pwn         | paiw1248   | Paiwan                  | Paiwan          |
| myp         | pira1253   | Pirahã                  | Pirahã          |
| spp         | supy1237   | Supyire Senoufo         | Supyire         |
| tiw         | tiwi1244   | Tiwi                    | Tiwi            |
| bhq         | tuka1249   | Tukang Besi South       | Tukang Besi     |
| pav         | wari1268   | Wari'                   | Wari'           |

``` r
# Clean up
rm(list = ls())
```
