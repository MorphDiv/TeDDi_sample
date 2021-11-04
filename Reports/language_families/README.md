Get language family counts for various multilingual resources
================
Steven Moran
(04 November, 2021)

``` r
library(tidyverse)
```

Get counts of families and area coverage for 100LC. This is easy because
we have already combined the 100LC data with Glottolog.

Number of language families.

``` r
df <- read_csv('../../LangInfo/langInfo_100LC.csv')
nrow(df %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct())
```

    ## [1] 60

Distribution of languages by area.

``` r
table(df$macroarea_glotto)
```

    ## 
    ##        Africa     Australia       Eurasia North America     Papunesia 
    ##            17             7            28            18            17 
    ## South America 
    ##            13

For the other resources, we’ll need the
[Glottolog](https://glottolog.org) data.

``` r
glottolog <- read_csv('glottolog_languoid/languoid.csv')
glottolog_areas <- read_csv('https://cdstar.eva.mpg.de/bitstreams/EAEA0-E62D-ED67-FD05-0/languages_and_dialects_geo.csv')
```

Get [UD language](https://universaldependencies.org) family counts.
Language codes are encoded in filenames. They can be two or three letter
ISO 639 codes, so we’ll need a mapping table to convert them all to
3-letter codes.

``` r
iso <- read_csv('language-codes-3b2_csv.csv')
```

Create the table.

``` r
ud <- read_csv('UD_fileprefixes.txt', col_names=F)
ud_split <- as.data.frame(str_split_fixed(ud$X1, "_", n=2))
ud <- cbind(ud, ud_split)
ud <- left_join(ud, iso, by=c("V1"="alpha2"))
ud <- ud %>% mutate(`alpha3-b` = coalesce(`alpha3-b`, V1))
ud <- ud %>% select(X1, V1, `alpha3-b`) %>% rename(file_prefix=X1, ISO6391 = V1, iso639P3code = `alpha3-b`)
ud <- left_join(ud, glottolog)
```

How many language families are present?

``` r
nrow(ud %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct())
```

    ## [1] 20

Let’s get the areas. UD is *heavily* Eurasian-centric.

``` r
ud <- left_join(ud, glottolog_areas, by=c("iso639P3code"="isocodes"))
table(ud$macroarea)
```

    ## 
    ##        Africa     Australia       Eurasia North America     Papunesia 
    ##             8             1            70             1             2 
    ## South America 
    ##             8

Next, let’s get the language family coverage for
[mBERT](https://github.com/google-research/bert/blob/master/multilingual.md).
We copy and paste the list of language names from
[here](https://github.com/google-research/bert/blob/master/multilingual.md)
and as it as [this csv file](mBert.csv).

``` r
mbert <- read_csv('mBERT.csv', col_names=F)
```

Now we can get some of the ISO 639-3 codes by language name look up.

``` r
library(lingtypology)
mbert_iso <- as.data.frame(iso.lang(mbert$X1))
mbert_iso <- mbert_iso %>% rownames_to_column(var="Name") %>% rename(iso639P3code = `iso.lang(mbert$X1)`)
```

But doesn’t get all of them, so we will have to fill in some by hand,
which we do by first writing the data to disk and then manually adding
the missing codes.

``` r
write_csv(mbert_iso, 'mBERT_iso.csv')
```

Going through by hand, I randomly chose certain codes, e.g. Colloquiual
Malay for “Malay”, so that they could be linked easily to Glottlog. Note
also, that mBERT languages include things like: Serbian, Bosnian,
Croatian, Serbo-Croatian – which by language code is simply “hbs”. So
the “language” coverage is actually less than what is reported.

Let’s reload the by hand data.

``` r
mbert_iso <- read_csv('mBERT_iso_updated_by_hand.csv')

library(testthat)
expect_false(any(is.na(mbert_iso$iso639P3code)))
```

And calculate how many “true” languages the sample has.

``` r
nrow(mbert_iso %>% select(iso639P3code) %>% distinct())
```

    ## [1] 97

Now we merge in Glottolog data and calculate how many language families
are present. Not many and less than UD.

``` r
mbert_iso <- left_join(mbert_iso, glottolog)
```

    ## Joining, by = "iso639P3code"

``` r
nrow(mbert_iso %>% select(family_id) %>% distinct())
```

    ## [1] 15

How about the areas? mBERT languages are also heavily Eurasian-centric
and it completely lacks any native South American languages.

``` r
mbert_iso <- left_join(mbert_iso, glottolog_areas, by=c("iso639P3code"="isocodes"))
table(mbert_iso$macroarea)
```

    ## 
    ##        Africa       Eurasia North America     Papunesia 
    ##             4            86             1             7

By comparison here are the macroarea coverage in all of Glottolog.

``` r
table(glottolog_areas$macroarea)
```

    ## 
    ##        Africa     Australia       Eurasia North America     Papunesia 
    ##          6471           665          6665          1336          4943 
    ## South America 
    ##          1146
