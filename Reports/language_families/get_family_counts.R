---
title: "Get language family counts for various multilingual resources"
author: "Steven Moran"
date: "(`r format(Sys.time(), '%d %B, %Y')`)"
output:
  github_document
---

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
nrow(ud %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct())

# Get mBERT language family counts
mbert <- read_csv('mBERT.csv', col_names=F)

# This gets ISO codes by language name
library(lingtypology)
mbert_iso <- as.data.frame(iso.lang(mbert$X1))

# Reformat the rownames
mbert_iso <- mbert_iso %>% rownames_to_column(var="Name") %>% rename(iso639P3code = `iso.lang(mbert$X1)`)

# But doesn't get all of them, so we will have to fill in some by hand...
write_csv(mbert_iso, 'mBERT_iso.csv')

# Going through by hand, I randomly chose certain codes, e.g. Colloquiual Malay for "Malay", so that 
# they could be linked easily to Glottlog. Note also, that mBERT languages include things like: 
# Serbian, Bosnian, Croatian, Serbo-Croatian -- which by language code is simply "hbs". So the 
# "language" coverage is actually less than what is reported.

# Let's reload the by hand data
mbert_iso <- read_csv('mBERT_iso_updated_by_hand.csv')

library(testthat)
expect_false(any(is.na(mbert_iso$iso639P3code)))

# How many true languages?
nrow(mbert_iso %>% select(iso639P3code) %>% distinct())







