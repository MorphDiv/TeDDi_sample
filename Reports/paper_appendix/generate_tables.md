Generate tables for the database paper
================
Steven Moran
29 October, 2020

    library(readr)
    library(dplyr)
    library(knitr)
    library(xtable)

# Overview

Generate descriptive stats and plots for the 100LC database paper
submission.

# Corpus overview

Load the 100 LC index file.

    index <- read_csv('../../LangInfo/langInfo_100LC.csv')

Let’s add in the corpus sizes by word counts (as suggested
[here](https://github.com/uzling/100LC/pull/193)).

    word_counts <- read_csv('../ttr/word_ttr.csv')

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   name = col_character(),
    ##   genre_broad = col_character(),
    ##   types = col_double(),
    ##   tokens = col_double(),
    ##   ttr = col_double()
    ## )

The output from the [word ttr
script](https://github.com/uzling/100LC/blob/master/Reports/ttr/word_ttr.csv)
is broken down by genre.

    word_counts %>% head(n=15) %>% kable()

| name                     | genre\_broad |  types |  tokens |       ttr |
|:-------------------------|:-------------|-------:|--------:|----------:|
| Abkhaz\_abk              | professional |    787 |    1332 | 0.5908408 |
| Acoma\_kjq               | non-fiction  |    849 |    3341 | 0.2541155 |
| Alamblak\_amp            | non-fiction  |  25322 |  229160 | 0.1104992 |
| Amele\_aey               | non-fiction  |  14139 |  233776 | 0.0604810 |
| Apurina\_apu             | non-fiction  |  14699 |  159164 | 0.0923513 |
| Arabic\_Egyptian\_arz    | non-fiction  |  74262 |  434040 | 0.1710948 |
| Arapesh\_Mountain\_ape   | non-fiction  |  14890 |  270754 | 0.0549946 |
| Asmat\_tml               | conversation |     99 |     141 | 0.7021277 |
| Bagirmi\_bmi             | grammar      |     53 |      71 | 0.7464789 |
| Barasano\_bsn            | non-fiction  |  17089 |  221691 | 0.0770848 |
| Basque\_eus              | non-fiction  | 126640 | 2715508 | 0.0466358 |
| Basque\_eus              | professional |    707 |    1407 | 0.5024876 |
| Berber\_MiddleAtlas\_tzm | professional |    670 |    1869 | 0.3584805 |
| Burmese\_mya             | non-fiction  |   6381 |  908516 | 0.0070235 |
| Burmese\_mya             | professional |    665 |    2966 | 0.2242077 |

So let’s first get the full counts.

    word_totals <- word_counts %>% group_by(name) %>% summarize(corpus_size=sum(tokens))

    ## `summarise()` ungrouping output (override with `.groups` argument)

Next we can merge the counts into the 100LC index.

    index <- left_join(index, word_totals)

    ## Joining, by = "name"

Decide what we want to keep from the language index and create a LaTeX
(long) table for the paper submission.

    df <- index %>% select(name_glotto, glottocode, iso639_3, status, genus_wals, macroarea_glotto, corpus_size) %>% arrange(name_glotto)

Rename the columns.

    df <- df %>% rename('Language name' = name_glotto, 'Glottocode' = glottocode, 'ISO 630-3' = iso639_3, 'Endangerment' = status, 'Genus' = genus_wals, 'Area' = macroarea_glotto, 'Size' = corpus_size)

How about this for a descriptive table of the languages in the 100LC
sample?

    df %>% head(n=30) %>% kable()

| Language name           | Glottocode | ISO 630-3 | Endangerment          | Genus                        | Area          |     Size |
|:------------------------|:-----------|:----------|:----------------------|:-----------------------------|:--------------|---------:|
| Abkhazian               | abkh1244   | abk       | vulnerable            | Northwest Caucasian          | Eurasia       |     1332 |
| Alamblak                | alam1246   | amp       | definitely endangered | Sepik Hill                   | Papunesia     |   229160 |
| Amele                   | amel1241   | aey       | vulnerable            | Madang                       | Papunesia     |   233776 |
| Apurinã                 | apur1254   | apu       | definitely endangered | Purus                        | South America |   159164 |
| Bagirmi                 | bagi1246   | bmi       | safe                  | Bongo-Bagirmi                | Africa        |       71 |
| Barasana-Eduria         | bara1380   | bsn       | definitely endangered | Tucanoan                     | South America |   221691 |
| Barclayville Grebo      | barc1235   | gry       | safe                  | Kru                          | Africa        |       NA |
| Basque                  | basq1248   | eus       | vulnerable            | Basque                       | Eurasia       |  2716915 |
| Bukiyip                 | buki1249   | ape       | definitely endangered | Kombio-Arapesh               | Papunesia     |   270754 |
| Burmese                 | nucl1310   | mya       | definitely endangered | Burmese-Lolo                 | Eurasia       |   911482 |
| Burushaski              | buru1296   | bsk       | definitely endangered | Burushaski                   | Eurasia       |      198 |
| Canela-Krahô            | cane1242   | ram       | definitely endangered | Ge-Kaingang                  | South America |    51061 |
| Central Moroccan Berber | cent2194   | tzm       | safe                  | Berber                       | Africa        |     1869 |
| Chamorro                | cham1312   | cha       | vulnerable            | Chamorro                     | Papunesia     |   200474 |
| Chukchi                 | chuk1273   | ckt       | definitely endangered | Northern Chukotko-Kamchatkan | Eurasia       |    16442 |
| Copainalá Zoque         | copa1236   | zoc       | definitely endangered | Mixe-Zoque                   | North America |      839 |
| Daga                    | daga1275   | dgz       | safe                  | Dagan                        | Papunesia     |   214348 |
| Eastern Oromo           | east2652   | hae       | safe                  | Lowland East Cushitic        | Africa        |   163318 |
| Egyptian Arabic         | egyp1253   | arz       | safe                  | Semitic                      | Africa        |   434040 |
| English                 | stan1293   | eng       | safe                  | Germanic                     | Eurasia       | 10786117 |
| Fijian                  | fiji1243   | fij       | safe                  | Oceanic                      | Papunesia     |   229639 |
| Finnish                 | finn1318   | fin       | safe                  | Finnic                       | Eurasia       | 10572389 |
| French                  | stan1290   | fra       | safe                  | Romance                      | Eurasia       | 10253170 |
| Georgian                | nucl1302   | kat       | safe                  | Kartvelian                   | Eurasia       |   829375 |
| German                  | stan1295   | deu       | safe                  | Germanic                     | Eurasia       | 10772059 |
| Gooniyandi              | goon1238   | gni       | severely endangered   | Bunuban                      | Australia     |       79 |
| Halh Mongolian          | halh1238   | khk       | definitely endangered | Mongolic                     | Eurasia       |   140291 |
| Hausa                   | haus1257   | hau       | safe                  | West Chadic                  | Africa        |   182998 |
| Hindi                   | hind1269   | hin       | safe                  | Indic                        | Eurasia       |  2047151 |
| Hixkaryána              | hixk1239   | hix       | definitely endangered | Cariban                      | South America |    43568 |

Dump an xtable (`longtable` in latex) for the paper. Currently, I just
copy and paste the table into the Overleaf document.

    add.to.row <- list(pos = list(0), command = NULL)
    command <- paste0("\\hline\n\\endhead\n",
                    "\\hline\n",
                    "\\multicolumn{", dim(df)[2], "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(df), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE, file = "100LC_index.tex")

    ## Warning in print.xtable(xtable(df), hline.after = c(-1), add.to.row =
    ## add.to.row, : Attempt to use "longtable" with floating = TRUE. Changing to
    ## FALSE.

# Word TTR

Now which stats for the paper (see:
<a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>)?

Counts for both words and characters:

-   number of types per genre and language
-   number of tokens per genre and language

Calculations (per language and per genre and language):

-   word TTR
-   character TTR
-   median word length (in characters)

Genres are represented by corpus IDs in the database (see:
<a href="https://github.com/uzling/100LC/blob/master/Reports/genres/get_genres.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/genres/get_genres.md</a>).
This makes it easy to extract the pertinent file(s) per genre and to do
the various type / token counts.

However, the 100 LC corpus contains multiple writing scripts in files
within the same language and genre (see:
<a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>).
This issue is discussed in this report on getting word types and tokens:

-   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/get_word_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/get_word_ttr.md</a>

Let’s load the results from that report.

    word_ttr <- read_csv('../ttr/word_ttr.csv')

And have a look:

    word_ttr %>% head() %>% kable()

| name                  | genre\_broad | types | tokens |       ttr |
|:----------------------|:-------------|------:|-------:|----------:|
| Abkhaz\_abk           | professional |   787 |   1332 | 0.5908408 |
| Acoma\_kjq            | non-fiction  |   849 |   3341 | 0.2541155 |
| Alamblak\_amp         | non-fiction  | 25322 | 229160 | 0.1104992 |
| Amele\_aey            | non-fiction  | 14139 | 233776 | 0.0604810 |
| Apurina\_apu          | non-fiction  | 14699 | 159164 | 0.0923513 |
| Arabic\_Egyptian\_arz | non-fiction  | 74262 | 434040 | 0.1710948 |

Rename the columns to match in the paper.

    word_ttr <- word_ttr %>% rename('Language' = name, 'Genre' = genre_broad, 'Word types' = types, 'Word tokens' = tokens, 'Type-token ratio' = ttr)
    word_ttr %>% head() %>% kable()

| Language              | Genre        | Word types | Word tokens | Type-token ratio |
|:----------------------|:-------------|-----------:|------------:|-----------------:|
| Abkhaz\_abk           | professional |        787 |        1332 |        0.5908408 |
| Acoma\_kjq            | non-fiction  |        849 |        3341 |        0.2541155 |
| Alamblak\_amp         | non-fiction  |      25322 |      229160 |        0.1104992 |
| Amele\_aey            | non-fiction  |      14139 |      233776 |        0.0604810 |
| Apurina\_apu          | non-fiction  |      14699 |      159164 |        0.0923513 |
| Arabic\_Egyptian\_arz | non-fiction  |      74262 |      434040 |        0.1710948 |

    add.to.row <- list(pos = list(0), command = NULL)
    command <- paste0("\\hline\n\\endhead\n",
                    "\\hline\n",
                    "\\multicolumn{", dim(word_ttr)[2], "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(word_ttr, digits = c(0,0,0,0,0,2)), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE, file="word_ttr.tex")

    ## Warning in print.xtable(xtable(word_ttr, digits = c(0, 0, 0, 0, 0, 2)), :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

# Grapheme TTR

We generate the grapheme TTR figures here:

-   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/get_grapheme_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/get_grapheme_ttr.md</a>

Let’s load the results from that report.

    grapheme_ttr <- read_csv('../ttr/grapheme_ttr.csv')

And have a look:

    grapheme_ttr %>% head() %>% kable()

| name                  | genre\_broad | types |  tokens |       ttr |
|:----------------------|:-------------|------:|--------:|----------:|
| Abkhaz\_abk           | professional |    64 |   10003 | 0.0063981 |
| Acoma\_kjq            | non-fiction  |    43 |   15893 | 0.0027056 |
| Alamblak\_amp         | non-fiction  |    66 | 1290455 | 0.0000511 |
| Amele\_aey            | non-fiction  |    68 | 1160739 | 0.0000586 |
| Apurina\_apu          | non-fiction  |    59 | 1247091 | 0.0000473 |
| Arabic\_Egyptian\_arz | non-fiction  |   426 | 1961436 | 0.0002172 |

Rename the columns to match in the paper.

    grapheme_ttr <- grapheme_ttr %>% rename('Language' = name, 'Genre' = genre_broad, 'Grapheme types' = types, 'Grapheme tokens' = tokens, 'Type-token ratio' = ttr)
    grapheme_ttr %>% head() %>% kable()

| Language              | Genre        | Grapheme types | Grapheme tokens | Type-token ratio |
|:----------------------|:-------------|---------------:|----------------:|-----------------:|
| Abkhaz\_abk           | professional |             64 |           10003 |        0.0063981 |
| Acoma\_kjq            | non-fiction  |             43 |           15893 |        0.0027056 |
| Alamblak\_amp         | non-fiction  |             66 |         1290455 |        0.0000511 |
| Amele\_aey            | non-fiction  |             68 |         1160739 |        0.0000586 |
| Apurina\_apu          | non-fiction  |             59 |         1247091 |        0.0000473 |
| Arabic\_Egyptian\_arz | non-fiction  |            426 |         1961436 |        0.0002172 |

    add.to.row <- list(pos = list(0), command = NULL)
    command <- paste0("\\hline\n\\endhead\n",
                    "\\hline\n",
                    "\\multicolumn{", dim(grapheme_ttr)[2], "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(grapheme_ttr, digits = c(0, 0, 0, 0, 0, 2)), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE, file="grapheme_ttr.tex")

    ## Warning in print.xtable(xtable(grapheme_ttr, digits = c(0, 0, 0, 0, 0, 2)), :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

# Plots

For a [histrograph plot](https://github.com/uzling/100LC/pull/193) of
word ttr, see [plot\_ttr.md](../ttr/plot_ttr.md).

# TODO

-   Generate median word length (in characters) (see:
    <a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>)
