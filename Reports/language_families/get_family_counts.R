library(tidyverse)

# Get counts of families for 100LC
df <- read_csv('/Users/stiv/GitHub/100LC/LangInfo/langInfo_100LC.csv')
df %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct()

# get the number of families from Glottolog

# get the number of areas

# Load the Glottolog family data
glottolog <- read_csv('glottolog_languoid/languoid.csv')

# Load the Glottolog geo data
glottolog_areas <- read_csv('https://cdstar.eva.mpg.de/bitstreams/EAEA0-E62D-ED67-FD05-0/languages_and_dialects_geo.csv')

# Load ISO 639-1 and 2 mappings
iso <- read_csv('language-codes-3b2_csv.csv')

# Get UD language family counts
ud <- read_csv('UD_fileprefixes.txt', col_names=F)
ud_split <- as.data.frame(str_split_fixed(ud$X1, "_", n=2))
ud <- cbind(ud, ud_split)
ud <- left_join(ud, iso, by=c("V1"="alpha2"))
ud <- ud %>% mutate(`alpha3-b` = coalesce(`alpha3-b`, V1))
ud <- ud %>% select(X1, V1, `alpha3-b`) %>% rename(file_prefix=X1, ISO6391 = V1, iso639P3code = `alpha3-b`)
ud <- left_join(ud, glottolog)
ud %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct()




# mBert


