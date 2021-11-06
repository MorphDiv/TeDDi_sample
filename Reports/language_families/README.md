Get language family counts for various multilingual resources
================
Steven Moran
(06 November, 2021)

``` r
library(tidyverse)
library(lingtypology)
library(testthat)
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

Some of the mappings from ISO639-1 to ISO639-3 are wrong. Note the NAs
in the `family_id`. We need to fix these by hand.

``` r
ud %>% select(file_prefix, ISO6391, iso639P3code, family_id) %>% head()
```

    ##    file_prefix ISO6391 iso639P3code family_id
    ## 1 af_afribooms      af          afr  indo1319
    ## 2     akk_riao     akk          akk  afro1255
    ## 3    aqz_tudet     aqz          aqz  tupi1275
    ## 4       sq_tsa      sq          alb      <NA>
    ## 5       am_att      am          amh  afro1255
    ## 6   grc_proiel     grc          grc  indo1319

``` r
ud <- ud %>% select(file_prefix, ISO6391, iso639P3code, family_id)
write_csv(ud, 'ud.csv')
```

Relaod and remerge.

``` r
ud <- read_csv('ud_by_hand.csv')
```

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   file_prefix = col_character(),
    ##   ISO6391 = col_character(),
    ##   iso639P3code = col_character()
    ## )

``` r
ud <- left_join(ud, glottolog)
```

    ## Joining, by = "iso639P3code"

``` r
ud <- left_join(ud, glottolog_areas, by=c("iso639P3code"="isocodes"))
```

We note that languagae isolates do not have a `family_id` in Glottolog,
like Basque. This potentially throws our language family counts off,
i.e. when there are two language isolates, counting them both as family
`NA` would group them into the same “family”. If thre is just one, then
the counts are still correct (as in the case of UD).

``` r
ud %>% filter(is.na(family_id))
```

    ## # A tibble: 1 × 23
    ##   file_prefix ISO6391 iso639P3code id       family_id parent_id name.x bookkeeping
    ##   <chr>       <chr>   <chr>        <chr>    <chr>     <chr>     <chr>  <lgl>      
    ## 1 eu_bdt      eu      eus          basq1248 <NA>      <NA>      Basque FALSE      
    ## # … with 15 more variables: level.x <chr>, latitude.x <dbl>, longitude.x <dbl>,
    ## #   description <lgl>, markup_description <lgl>, child_family_count <dbl>,
    ## #   child_language_count <dbl>, child_dialect_count <dbl>, country_ids <chr>,
    ## #   glottocode <chr>, name.y <chr>, level.y <chr>, macroarea <chr>,
    ## #   latitude.y <dbl>, longitude.y <dbl>

How many language families are present?

``` r
nrow(ud %>% filter(!is.na(family_id)) %>% select(family_id) %>% distinct())
```

    ## [1] 20

Let’s get the areas. UD is *heavily* Eurasian-centric.

``` r
table(ud$macroarea)
```

    ## 
    ##        Africa     Australia       Eurasia North America     Papunesia 
    ##             8             1            86             1             2 
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

Now we can get some of the ISO 639-3 codes by language name look up. For
this we can use the `lingtypology` library.

``` r
mbert_iso <- as.data.frame(lingtypology::iso.lang(mbert$X1))
mbert_iso <- mbert_iso %>% rownames_to_column(var="Name") %>% rename(iso639P3code = `lingtypology::iso.lang(mbert$X1)`)
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
mbert_iso <- read_csv('mBERT_iso_by_hand.csv')
expect_false(any(is.na(mbert_iso$iso639P3code)))
```

And calculate how many “true” languages the sample has.

``` r
nrow(mbert_iso %>% select(iso639P3code) %>% distinct())
```

    ## [1] 97

Now we merge in Glottolog data and calculate how many language families
are present. Not many and less than UD. (Once again Basque is `NA` for
`family_id`, but it’s the only language isolate in the sample, so the
counts are correct for language family.)

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

Now for the bibles data.

``` r
bibles <- read_csv('bibles100codes.csv')
```

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   Filename = col_character(),
    ##   iso639P3code = col_character()
    ## )

``` r
bibles <- left_join(bibles, glottolog)
```

    ## Joining, by = "iso639P3code"

``` r
bibles <- left_join(bibles, glottolog_areas)
```

    ## Joining, by = c("name", "level", "latitude", "longitude")

How many languages according to ISO 639-3 codes?

``` r
nrow(bibles %>% select(iso639P3code) %>% distinct())
```

    ## [1] 103

How many language families? Since there are two islates in the sample,
we need to add by one to account for the two `NA` in the `family_id`.

``` r
nrow(bibles %>% select(family_id) %>% distinct()) + 1
```

    ## [1] 30

Areal distribution? Note no data points in Australia.

``` r
table(bibles$macroarea)
```

    ## 
    ##        Africa       Eurasia North America     Papunesia South America 
    ##            17            56            14             7             9

Now for XGLUE.

``` r
xglue <- read_csv('xglue_languagecodes.txt', col_names = FALSE)
```

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   X1 = col_character()
    ## )

``` r
xglue <- xglue %>% rename(alpha2 = X1)
xglue <- left_join(xglue, iso)
```

    ## Joining, by = "alpha2"

``` r
xglue <- xglue %>% rename(iso639P3code = `alpha3-b`)
xglue <- left_join(xglue, glottolog)
```

    ## Joining, by = "iso639P3code"

Some of the XLGUE mappings are wrong. Note the NAs. We fix these by
hand.

``` r
xglue %>% select(family_id) %>% distinct()
```

    ## # A tibble: 5 × 1
    ##   family_id
    ##   <chr>    
    ## 1 <NA>     
    ## 2 indo1319 
    ## 3 taik1256 
    ## 4 turk1311 
    ## 5 aust1305

``` r
tmp <- xglue %>% select(alpha2, iso639P3code, English, family_id)
# write_csv(tmp, 'xglue.csv')
tmp
```

    ## # A tibble: 19 × 4
    ##    alpha2 iso639P3code English               family_id
    ##    <chr>  <chr>        <chr>                 <chr>    
    ##  1 ar     ara          Arabic                <NA>     
    ##  2 bg     bul          Bulgarian             indo1319 
    ##  3 de     ger          German                <NA>     
    ##  4 el     gre          Greek, Modern (1453-) <NA>     
    ##  5 en     eng          English               indo1319 
    ##  6 es     spa          Spanish; Castilian    indo1319 
    ##  7 fr     fre          French                <NA>     
    ##  8 hi     hin          Hindi                 indo1319 
    ##  9 it     ita          Italian               indo1319 
    ## 10 nl     dut          Dutch; Flemish        <NA>     
    ## 11 pl     pol          Polish                indo1319 
    ## 12 pt     por          Portuguese            indo1319 
    ## 13 ru     rus          Russian               indo1319 
    ## 14 sw     swa          Swahili               <NA>     
    ## 15 th     tha          Thai                  taik1256 
    ## 16 tr     tur          Turkish               turk1311 
    ## 17 ur     urd          Urdu                  indo1319 
    ## 18 vi     vie          Vietnamese            aust1305 
    ## 19 zh     chi          Chinese               <NA>

Load the hand corrected XGLUE data.

``` r
xglue <- read_csv('xglue_by_hand.csv')
```

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   alpha2 = col_character(),
    ##   iso639P3code = col_character(),
    ##   LanguageName = col_character()
    ## )

Merge in Glottolog.

``` r
xglue <- left_join(xglue, glottolog)
```

    ## Joining, by = "iso639P3code"

``` r
xglue <- left_join(xglue, glottolog_areas)
```

    ## Joining, by = c("name", "level", "latitude", "longitude")

How many languages according to ISO 639-3 codes?

``` r
nrow(xglue %>% select(iso639P3code) %>% distinct())
```

    ## [1] 19

How many language families?

``` r
expect_false(any(is.na(xglue %>% select(family_id) %>% distinct())))
nrow(xglue %>% select(family_id) %>% distinct())
```

    ## [1] 7

Areal distribution? Note no data points in Australia. Most XGLUE
languages are Eurasian. No Americas, Papunesia or Australia coverage.

``` r
table(xglue$macroarea)
```

    ## 
    ##  Africa Eurasia 
    ##       1      18
