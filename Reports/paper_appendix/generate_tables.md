Generate tables for the 100LC database paper
================
Steven Moran

31 October, 2020

    library(readr)
    library(dplyr)
    library(knitr)
    library(xtable)

# Overview

Generate descriptive stats and plots for the 100LC database paper
submission.

# Corpus overview

Load the 100LC index file.

    index <- read_csv("../../LangInfo/langInfo_100LC.csv")

Let’s add in the corpus sizes by word counts (as suggested
[here](https://github.com/uzling/100LC/pull/193)).

    word_counts <- read_csv("../ttr/word_ttr.csv")

    ## 
    ## ── Column specification ────────────────────────────────────────────────────────
    ## cols(
    ##   name = col_character(),
    ##   genre_broad = col_character(),
    ##   writing_system = col_character(),
    ##   types = col_double(),
    ##   tokens = col_double(),
    ##   mean_word_length = col_double(),
    ##   ttr = col_double()
    ## )

The output from the [word ttr
script](https://github.com/uzling/100LC/blob/master/Reports/ttr/word_ttr.csv)
is broken down by genre and writing systems when there are multiple
scripts for the same corpus and genre, e.g. Vietnamese.

    word_counts %>%
      head(n = 15) %>%
      kable()

| name                     | genre\_broad | writing\_system |  types |  tokens | mean\_word\_length |       ttr |
|:-------------------------|:-------------|:----------------|-------:|--------:|-------------------:|----------:|
| Abkhaz\_abk              | professional | Cyrl            |    787 |    1332 |           7.936468 | 0.5908408 |
| Acoma\_kjq               | non-fiction  | Latn            |    849 |    3341 |           5.361602 | 0.2541155 |
| Alamblak\_amp            | non-fiction  | Latn            |  25322 |  229160 |           8.520930 | 0.1104992 |
| Amele\_aey               | non-fiction  | Latn            |  14139 |  233776 |           7.803027 | 0.0604810 |
| Apurina\_apu             | non-fiction  | Latn            |  14699 |  159164 |          11.055038 | 0.0923513 |
| Arabic\_Egyptian\_arz    | non-fiction  | Arab            |  74262 |  434040 |          10.090800 | 0.1710948 |
| Arapesh\_Mountain\_ape   | non-fiction  | Latn            |  14890 |  270754 |           8.194023 | 0.0549946 |
| Asmat\_tml               | conversation | Latn            |    105 |     153 |           6.352381 | 0.6862745 |
| Bagirmi\_bmi             | grammar      | Latn            |     59 |      79 |           3.067797 | 0.7468354 |
| Barasano\_bsn            | non-fiction  | Latn            |  17089 |  221691 |          10.554567 | 0.0770848 |
| Basque\_eus              | non-fiction  | Latn            | 126640 | 2715508 |           8.990461 | 0.0466358 |
| Basque\_eus              | professional | Latn            |    707 |    1407 |           7.776521 | 0.5024876 |
| Berber\_MiddleAtlas\_tzm | professional | Latn            |    670 |    1869 |           6.325373 | 0.3584805 |
| Burmese\_mya             | non-fiction  | Mymr            |   6381 |  908516 |           6.412945 | 0.0070235 |
| Burmese\_mya             | professional | Mymr            |    665 |    2966 |           5.863158 | 0.2242077 |

So let’s first get the full counts.

    word_totals <- word_counts %>%
      group_by(name) %>%
      summarize(corpus_size = sum(tokens))

    ## `summarise()` ungrouping output (override with `.groups` argument)

Next we can merge the counts into the 100LC index.

    index <- left_join(index, word_totals)

    ## Joining, by = "name"

Decide what we want to keep from the language index and create a LaTeX
(long) table for the paper submission.

    df <- index %>%
      select(name_glotto,
             glottocode,
             iso639_3,
             status,
             genus_wals,
             macroarea_glotto,
             corpus_size) %>%
      arrange(name_glotto)

Rename the columns.

    df <- df %>% rename("Language name" = name_glotto,
                        "Glottocode" = glottocode,
                        "ISO 630-3" = iso639_3,
                        "Endangerment" = status,
                        "Genus" = genus_wals,
                        "Area" = macroarea_glotto,
                        "Size (in words)" = corpus_size)

How about this for a descriptive table of the languages in the 100LC
sample?

    df %>%
      head(n = 30) %>%
      kable()

| Language name           | Glottocode | ISO 630-3 | Endangerment          | Genus                        | Area          | Size (in words) |
|:------------------------|:-----------|:----------|:----------------------|:-----------------------------|:--------------|----------------:|
| Abkhazian               | abkh1244   | abk       | vulnerable            | Northwest Caucasian          | Eurasia       |            1332 |
| Alamblak                | alam1246   | amp       | definitely endangered | Sepik Hill                   | Papunesia     |          229160 |
| Amele                   | amel1241   | aey       | vulnerable            | Madang                       | Papunesia     |          233776 |
| Apurinã                 | apur1254   | apu       | definitely endangered | Purus                        | South America |          159164 |
| Bagirmi                 | bagi1246   | bmi       | safe                  | Bongo-Bagirmi                | Africa        |              79 |
| Barasana-Eduria         | bara1380   | bsn       | definitely endangered | Tucanoan                     | South America |          221691 |
| Barclayville Grebo      | barc1235   | gry       | safe                  | Kru                          | Africa        |          143350 |
| Basque                  | basq1248   | eus       | vulnerable            | Basque                       | Eurasia       |         2716915 |
| Bukiyip                 | buki1249   | ape       | definitely endangered | Kombio-Arapesh               | Papunesia     |          270754 |
| Burmese                 | nucl1310   | mya       | definitely endangered | Burmese-Lolo                 | Eurasia       |          911482 |
| Burushaski              | buru1296   | bsk       | definitely endangered | Burushaski                   | Eurasia       |             203 |
| Canela-Krahô            | cane1242   | ram       | definitely endangered | Ge-Kaingang                  | South America |           51061 |
| Central Moroccan Berber | cent2194   | tzm       | safe                  | Berber                       | Africa        |            1869 |
| Chamorro                | cham1312   | cha       | vulnerable            | Chamorro                     | Papunesia     |          200474 |
| Chukchi                 | chuk1273   | ckt       | definitely endangered | Northern Chukotko-Kamchatkan | Eurasia       |           16442 |
| Copainalá Zoque         | copa1236   | zoc       | definitely endangered | Mixe-Zoque                   | North America |             846 |
| Daga                    | daga1275   | dgz       | safe                  | Dagan                        | Papunesia     |          214348 |
| Eastern Oromo           | east2652   | hae       | safe                  | Lowland East Cushitic        | Africa        |          163318 |
| Egyptian Arabic         | egyp1253   | arz       | safe                  | Semitic                      | Africa        |          434040 |
| English                 | stan1293   | eng       | safe                  | Germanic                     | Eurasia       |        10786117 |
| Fijian                  | fiji1243   | fij       | safe                  | Oceanic                      | Papunesia     |          229639 |
| Finnish                 | finn1318   | fin       | safe                  | Finnic                       | Eurasia       |        10572389 |
| French                  | stan1290   | fra       | safe                  | Romance                      | Eurasia       |        10253170 |
| Georgian                | nucl1302   | kat       | safe                  | Kartvelian                   | Eurasia       |          829375 |
| German                  | stan1295   | deu       | safe                  | Germanic                     | Eurasia       |        10772059 |
| Gooniyandi              | goon1238   | gni       | severely endangered   | Bunuban                      | Australia     |              84 |
| Halh Mongolian          | halh1238   | khk       | definitely endangered | Mongolic                     | Eurasia       |          140291 |
| Hausa                   | haus1257   | hau       | safe                  | West Chadic                  | Africa        |          182998 |
| Hindi                   | hind1269   | hin       | safe                  | Indic                        | Eurasia       |         2047151 |
| Hixkaryána              | hixk1239   | hix       | definitely endangered | Cariban                      | South America |           43568 |

Dump an xtable (`longtable` in latex) for the paper. Currently, I just
copy and paste the table into the Overleaf document.

    add_to_row <- list(pos = list(0), command = NULL)
    command <- paste0(
      "\\hline\n\\endhead\n",
      "\\hline\n",
      "\\multicolumn{", dim(df)[2], "}{l}",
      "{\\footnotesize Continued on next page}\n",
      "\\endfoot\n",
      "\\endlastfoot\n"
    )
    add_to_row$command <- command

    print(xtable(df,
          digits = c(0, 0, 0, 0, 0, 0, 0, 0)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE,
          file = "100LC_index.tex")

    ## Warning in print.xtable(xtable(df, digits = c(0, 0, 0, 0, 0, 0, 0, 0)), :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

    print(xtable(df,
          digits = c(0, 0, 0, 0, 0, 0, 0, 0)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE)

    ## Warning in print.xtable(xtable(df, digits = c(0, 0, 0, 0, 0, 0, 0, 0)), :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

    ## % latex table generated in R 4.0.3 by xtable 1.8-4 package
    ## % Sat Oct 31 13:12:15 2020
    ## \begin{longtable}{llllllr}
    ##   \hline
    ## Language name & Glottocode & ISO 630-3 & Endangerment & Genus & Area & Size (in words) \\ 
    ##  Abkhazian & abkh1244 & abk & vulnerable & Northwest Caucasian & Eurasia & 1332 \\ 
    ##   Alamblak & alam1246 & amp & definitely endangered & Sepik Hill & Papunesia & 229160 \\ 
    ##   Amele & amel1241 & aey & vulnerable & Madang & Papunesia & 233776 \\ 
    ##   Apurinã & apur1254 & apu & definitely endangered & Purus & South America & 159164 \\ 
    ##   Bagirmi & bagi1246 & bmi & safe & Bongo-Bagirmi & Africa & 79 \\ 
    ##   Barasana-Eduria & bara1380 & bsn & definitely endangered & Tucanoan & South America & 221691 \\ 
    ##   Barclayville Grebo & barc1235 & gry & safe & Kru & Africa & 143350 \\ 
    ##   Basque & basq1248 & eus & vulnerable & Basque & Eurasia & 2716915 \\ 
    ##   Bukiyip & buki1249 & ape & definitely endangered & Kombio-Arapesh & Papunesia & 270754 \\ 
    ##   Burmese & nucl1310 & mya & definitely endangered & Burmese-Lolo & Eurasia & 911482 \\ 
    ##   Burushaski & buru1296 & bsk & definitely endangered & Burushaski & Eurasia & 203 \\ 
    ##   Canela-Krahô & cane1242 & ram & definitely endangered & Ge-Kaingang & South America & 51061 \\ 
    ##   Central Moroccan Berber & cent2194 & tzm & safe & Berber & Africa & 1869 \\ 
    ##   Chamorro & cham1312 & cha & vulnerable & Chamorro & Papunesia & 200474 \\ 
    ##   Chukchi & chuk1273 & ckt & definitely endangered & Northern Chukotko-Kamchatkan & Eurasia & 16442 \\ 
    ##   Copainalá Zoque & copa1236 & zoc & definitely endangered & Mixe-Zoque & North America & 846 \\ 
    ##   Daga & daga1275 & dgz & safe & Dagan & Papunesia & 214348 \\ 
    ##   Eastern Oromo & east2652 & hae & safe & Lowland East Cushitic & Africa & 163318 \\ 
    ##   Egyptian Arabic & egyp1253 & arz & safe & Semitic & Africa & 434040 \\ 
    ##   English & stan1293 & eng & safe & Germanic & Eurasia & 10786117 \\ 
    ##   Fijian & fiji1243 & fij & safe & Oceanic & Papunesia & 229639 \\ 
    ##   Finnish & finn1318 & fin & safe & Finnic & Eurasia & 10572389 \\ 
    ##   French & stan1290 & fra & safe & Romance & Eurasia & 10253170 \\ 
    ##   Georgian & nucl1302 & kat & safe & Kartvelian & Eurasia & 829375 \\ 
    ##   German & stan1295 & deu & safe & Germanic & Eurasia & 10772059 \\ 
    ##   Gooniyandi & goon1238 & gni & severely endangered & Bunuban & Australia & 84 \\ 
    ##   Halh Mongolian & halh1238 & khk & definitely endangered & Mongolic & Eurasia & 140291 \\ 
    ##   Hausa & haus1257 & hau & safe & West Chadic & Africa & 182998 \\ 
    ##   Hindi & hind1269 & hin & safe & Indic & Eurasia & 2047151 \\ 
    ##   Hixkaryána & hixk1239 & hix & definitely endangered & Cariban & South America & 43568 \\ 
    ##   Hmong Njua & hmon1264 & hnj & safe & Hmong-Mien & Eurasia & 2801 \\ 
    ##   Imbabura Highland Quichua & imba1240 & qvi & vulnerable & Quechuan & South America & 142011 \\ 
    ##   Imonda & imon1245 & imn & definitely endangered & Border & Papunesia & 296 \\ 
    ##   Indonesian & indo1316 & ind & safe & Malayo-Sumbawan & Papunesia & 5721423 \\ 
    ##   Japanese & nucl1643 & jpn & safe & Japanese & Eurasia & 6170677 \\ 
    ##   Kalaallisut & kala1399 & kal & vulnerable & Eskimo & Eurasia & 63507 \\ 
    ##   Kannada & nucl1305 & kan & critically endangered & Southern Dravidian & Eurasia & 1081 \\ 
    ##   Karok & karo1304 & kyh & critically endangered & Karok & North America & 143350 \\ 
    ##   Kayardild & kaya1319 & gyd & critically endangered & Tangkic & Australia & 27 \\ 
    ##   Kiowa & kiow1266 & kio & critically endangered & Kiowa-Tanoan & North America & 154 \\ 
    ##   Koasati & koas1236 & cku & severely endangered & Muskogean & North America & 143350 \\ 
    ##   Korean & kore1280 & kor & safe & Korean & Eurasia & 3373531 \\ 
    ##   Koyraboro Senni Songhai & koyr1242 & ses & safe & Songhay & Africa & 143350 \\ 
    ##   Krongo & kron1241 & kgo & vulnerable & Kadugli & Africa & 143350 \\ 
    ##   Kutenai & kute1249 & kut & severely endangered & Kutenai & North America & 66 \\ 
    ##   Lakota & lako1247 & lkt & definitely endangered & Core Siouan & North America & 143350 \\ 
    ##   Lango (Uganda) & lang1324 & laj & safe & Nilotic & Africa & 174637 \\ 
    ##   Lavukaleve & lavu1241 & lvk & definitely endangered & Lavukaleve & Papunesia & 1537 \\ 
    ##   Lezgian & lezg1247 & lez & vulnerable & Lezgic & Eurasia & 143350 \\ 
    ##   Lower Grand Valley Dani & lowe1415 & dni & safe & Dani & Papunesia & 345 \\ 
    ##   Luvale & luva1239 & lue & safe & Bantoid & Africa & 1216 \\ 
    ##   Makah & maka1318 & myh & extinct & Southern Wakashan & North America & 178 \\ 
    ##   Mandarin Chinese & mand1415 & cmn & safe & Chinese & Eurasia & 9080064 \\ 
    ##   Mangarrayi & mang1381 & mpc & critically endangered & Mangarrayi & Australia & 143350 \\ 
    ##   Manipuri & mani1292 & mni & vulnerable & Kuki-Chin & Eurasia & 143350 \\ 
    ##   Mapudungun & mapu1245 & arn & definitely endangered & Araucanian & South America & 196158 \\ 
    ##   Maricopa & mari1440 & mrc & severely endangered & Yuman & North America & 143350 \\ 
    ##   Martuthunira & mart1255 & vma & critically endangered & Western Pama-Nyungan & Australia & 3157 \\ 
    ##   Mawng & maun1240 & mph & vulnerable & Iwaidjan & Australia & 22452 \\ 
    ##   Maybrat-Karon & maib1239 & ayz & safe & North-Central Bird's Head & Papunesia & 737 \\ 
    ##   Mezquital Otomi & mezq1235 & ote & safe & Otomian & North America & 26 \\ 
    ##   Modern Greek & mode1248 & ell & severely endangered & Greek & Eurasia & 10797474 \\ 
    ##   Modern Hebrew & hebr1245 & heb & safe & Semitic & Eurasia & 5136859 \\ 
    ##   Nama (Namibia) & nama1264 & naq & vulnerable & Khoe-Kwadi & Africa & 181370 \\ 
    ##   Ngiyambaa & wang1291 & wyb & critically endangered & Southeastern Pama-Nyungan & Australia & 635 \\ 
    ##   North Slavey & nort2942 & scs & definitely endangered & Athapaskan & North America & 143350 \\ 
    ##   Oneida & onei1249 & one & definitely endangered & Northern Iroquoian & North America & 143350 \\ 
    ##   Paiwan & paiw1248 & pwn & vulnerable & Paiwan & Papunesia & 143350 \\ 
    ##   Paraguayan Guaraní & para1311 & gug & safe & Tupi-Guaraní & South America & 1189 \\ 
    ##   Pirahã & pira1253 & myp & vulnerable & Mura & South America & 6300 \\ 
    ##   Plains Cree & plai1258 & crk & severely endangered & Algonquian & North America &  \\ 
    ##   Plateau Malagasy & plat1254 & plt & safe & Barito & Africa & 680922 \\ 
    ##   Popti' & popt1235 & jac & vulnerable & Mayan & North America & 220787 \\ 
    ##   Rama & rama1270 & rma & critically endangered & Rama & North America & 569 \\ 
    ##   Rapanui & rapa1244 & rap & definitely endangered & Oceanic & Papunesia & 2535 \\ 
    ##   Russian & russ1263 & rus & critically endangered & Slavic & Eurasia & 5632975 \\ 
    ##   San Miguel El Grande Mixtec & sanm1295 & mig & vulnerable & Mixtecan & North America & 226957 \\ 
    ##   Sango & sang1328 & sag & safe & Ubangi & Africa & 267559 \\ 
    ##   Sanumá & sanu1240 & xsu & definitely endangered & Yanomam & South America & 408796 \\ 
    ##   Spanish & stan1288 & spa & safe & Romance & Eurasia & 10769424 \\ 
    ##   Supyire Senoufo & supy1237 & spp & safe & Gur & Africa & 143350 \\ 
    ##   Swahili & swah1253 & swh & definitely endangered & Bantoid & Africa & 130639 \\ 
    ##   Tagalog & taga1270 & tgl & safe & Greater Central Philippine & Papunesia & 1843415 \\ 
    ##   Tamnim Citak & tamn1235 & tml & safe & Asmat-Kamoro & Papunesia & 153 \\ 
    ##   Thai & thai1261 & tha & safe & Kam-Tai & Eurasia & 6665245 \\ 
    ##   Tiwi & tiwi1244 & tiw & definitely endangered & Tiwian & Australia & 143350 \\ 
    ##   Tukang Besi South & tuka1249 & bhq & safe & Celebic & Papunesia & 143350 \\ 
    ##   Turkish & nucl1301 & tur & safe & Turkic & Eurasia & 5469424 \\ 
    ##   Vietnamese & viet1252 & vie & safe & Viet-Muong & Eurasia & 5870036 \\ 
    ##   Warao & wara1303 & wba & vulnerable & Warao & South America & 351 \\ 
    ##   Wari' & wari1268 & pav & definitely endangered & Chapacura-Wanham & South America & 143350 \\ 
    ##   West Kewa & west2599 & kew & safe & Engan & Papunesia & 272299 \\ 
    ##   Western Farsi & west2369 & pes & safe & Iranian & Eurasia & 5214466 \\ 
    ##   Western Keres & west2632 & kjq & definitely endangered & Keresan & North America & 3341 \\ 
    ##   Wichí Lhamtés Güisnay & wich1264 & mzh & vulnerable & Matacoan & South America & 720572 \\ 
    ##   Wichita & wich1260 & wic & extinct & Caddoan & North America & 529 \\ 
    ##   Yagua & yagu1244 & yad & definitely endangered & Peba-Yaguan & South America & 143481 \\ 
    ##   Yaqui & yaqu1251 & yaq & vulnerable & Cahita & North America & 240424 \\ 
    ##   Yoruba & yoru1245 & yor & safe & Defoid & Africa & 793427 \\ 
    ##   Zulu & zulu1248 & zul & safe & Bantoid & Africa & 1077 \\ 
    ##   \hline
    ## \end{longtable}

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

However, the 100LC corpus contains multiple writing scripts in files
within the same language and genre (see:
<a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>).
This issue is discussed in this report on getting word types and tokens:

-   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/get_word_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/get_word_ttr.md</a>

Let’s load the results from that report.

    word_ttr <- read_csv("../ttr/word_ttr.csv")

And have a look:

    word_ttr %>%
      head() %>%
      kable()

| name                  | genre\_broad | writing\_system | types | tokens | mean\_word\_length |       ttr |
|:----------------------|:-------------|:----------------|------:|-------:|-------------------:|----------:|
| Abkhaz\_abk           | professional | Cyrl            |   787 |   1332 |           7.936468 | 0.5908408 |
| Acoma\_kjq            | non-fiction  | Latn            |   849 |   3341 |           5.361602 | 0.2541155 |
| Alamblak\_amp         | non-fiction  | Latn            | 25322 | 229160 |           8.520930 | 0.1104992 |
| Amele\_aey            | non-fiction  | Latn            | 14139 | 233776 |           7.803027 | 0.0604810 |
| Apurina\_apu          | non-fiction  | Latn            | 14699 | 159164 |          11.055038 | 0.0923513 |
| Arabic\_Egyptian\_arz | non-fiction  | Arab            | 74262 | 434040 |          10.090800 | 0.1710948 |

Let’s rearrange the columns to make them more reader friendly.

    word_ttr <- word_ttr %>% select(name, genre_broad, writing_system, mean_word_length, types, tokens, ttr)

Rename the columns to match in the paper.

    word_ttr <- word_ttr %>%
      rename("Language" = name,
             "Genre" = genre_broad,
             "Writing system" = writing_system,
             "Word types" = types,
             "Word tokens" = tokens,
             "Mean word length" = mean_word_length,
             "Type-token ratio" = ttr)

    word_ttr %>%
      head() %>%
      kable()

| Language              | Genre        | Writing system | Mean word length | Word types | Word tokens | Type-token ratio |
|:----------------------|:-------------|:---------------|-----------------:|-----------:|------------:|-----------------:|
| Abkhaz\_abk           | professional | Cyrl           |         7.936468 |        787 |        1332 |        0.5908408 |
| Acoma\_kjq            | non-fiction  | Latn           |         5.361602 |        849 |        3341 |        0.2541155 |
| Alamblak\_amp         | non-fiction  | Latn           |         8.520930 |      25322 |      229160 |        0.1104992 |
| Amele\_aey            | non-fiction  | Latn           |         7.803027 |      14139 |      233776 |        0.0604810 |
| Apurina\_apu          | non-fiction  | Latn           |        11.055038 |      14699 |      159164 |        0.0923513 |
| Arabic\_Egyptian\_arz | non-fiction  | Arab           |        10.090800 |      74262 |      434040 |        0.1710948 |

    add_to_row <- list(pos = list(0), command = NULL)
    command <- paste0(
      "\\hline\n\\endhead\n",
      "\\hline\n",
      "\\multicolumn{", dim(word_ttr)[2] + 1, "}{l}",
      "{\\footnotesize Continued on next page}\n",
      "\\endfoot\n",
      "\\endlastfoot\n"
    )
    add_to_row$command <- command
    print(xtable(word_ttr,
          digits = c(0, 0, 0, 0, 2, 0, 0, 2)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE,
          file = "word_ttr.tex")

    ## Warning in print.xtable(xtable(word_ttr, digits = c(0, 0, 0, 0, 2, 0, 0, :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

    print(xtable(word_ttr,
          digits = c(0, 0, 0, 0, 2, 0, 0, 2)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE)

    ## Warning in print.xtable(xtable(word_ttr, digits = c(0, 0, 0, 0, 2, 0, 0, :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

    ## % latex table generated in R 4.0.3 by xtable 1.8-4 package
    ## % Sat Oct 31 13:12:15 2020
    ## \begin{longtable}{lllrrrr}
    ##   \hline
    ## Language & Genre & Writing system & Mean word length & Word types & Word tokens & Type-token ratio \\ 
    ##  Abkhaz\_abk & professional & Cyrl & 7.94 & 787 & 1332 & 0.59 \\ 
    ##   Acoma\_kjq & non-fiction & Latn & 5.36 & 849 & 3341 & 0.25 \\ 
    ##   Alamblak\_amp & non-fiction & Latn & 8.52 & 25322 & 229160 & 0.11 \\ 
    ##   Amele\_aey & non-fiction & Latn & 7.80 & 14139 & 233776 & 0.06 \\ 
    ##   Apurina\_apu & non-fiction & Latn & 11.06 & 14699 & 159164 & 0.09 \\ 
    ##   Arabic\_Egyptian\_arz & non-fiction & Arab & 10.09 & 74262 & 434040 & 0.17 \\ 
    ##   Arapesh\_Mountain\_ape & non-fiction & Latn & 8.19 & 14890 & 270754 & 0.05 \\ 
    ##   Asmat\_tml & conversation & Latn & 6.35 & 105 & 153 & 0.69 \\ 
    ##   Bagirmi\_bmi & grammar & Latn & 3.07 & 59 & 79 & 0.75 \\ 
    ##   Barasano\_bsn & non-fiction & Latn & 10.55 & 17089 & 221691 & 0.08 \\ 
    ##   Basque\_eus & non-fiction & Latn & 8.99 & 126640 & 2715508 & 0.05 \\ 
    ##   Basque\_eus & professional & Latn & 7.78 & 707 & 1407 & 0.50 \\ 
    ##   Berber\_MiddleAtlas\_tzm & professional & Latn & 6.33 & 670 & 1869 & 0.36 \\ 
    ##   Burmese\_mya & non-fiction & Mymr & 6.41 & 6381 & 908516 & 0.01 \\ 
    ##   Burmese\_mya & professional & Mymr & 5.86 & 665 & 2966 & 0.22 \\ 
    ##   Burushaski\_bsk & grammar & Latn & 5.63 & 123 & 203 & 0.61 \\ 
    ##   CanelaKraho\_ram & non-fiction & Latn & 6.18 & 3043 & 51061 & 0.06 \\ 
    ##   Chamorro\_cha & non-fiction & Latn & 8.46 & 9653 & 198523 & 0.05 \\ 
    ##   Chamorro\_cha & professional & Latn & 7.25 & 571 & 1951 & 0.29 \\ 
    ##   Chukchi\_ckt & non-fiction & Cyrl & 10.73 & 5192 & 16442 & 0.32 \\ 
    ##   Daga\_dgz & non-fiction & Latn & 7.21 & 7839 & 214348 & 0.04 \\ 
    ##   Dani\_LowerGrandValley\_dni & conversation & Latn & 5.73 & 164 & 345 & 0.48 \\ 
    ##   English\_eng & fiction & Latn & 7.79 & 80966 & 5073103 & 0.02 \\ 
    ##   English\_eng & non-fiction & Latn & 7.57 & 60787 & 5711261 & 0.01 \\ 
    ##   English\_eng & professional & Latn & 6.67 & 534 & 1753 & 0.30 \\ 
    ##   Fijian\_fij & non-fiction & Latn & 7.60 & 3636 & 227543 & 0.02 \\ 
    ##   Fijian\_fij & professional & Latn & 6.39 & 396 & 2096 & 0.19 \\ 
    ##   Finnish\_fin & fiction & Latn & 10.68 & 366900 & 5021399 & 0.07 \\ 
    ##   Finnish\_fin & non-fiction & Latn & 10.47 & 340673 & 5549590 & 0.06 \\ 
    ##   Finnish\_fin & professional & Latn & 8.99 & 824 & 1400 & 0.59 \\ 
    ##   French\_fra & fiction & Latn & 8.23 & 133702 & 4814508 & 0.03 \\ 
    ##   French\_fra & non-fiction & Latn & 8.12 & 97156 & 5436716 & 0.02 \\ 
    ##   French\_fra & professional & Latn & 7.21 & 647 & 1946 & 0.33 \\ 
    ##   Georgian\_kat & non-fiction & Geor & 7.57 & 81798 & 827965 & 0.10 \\ 
    ##   Georgian\_kat & professional & Geor & 8.67 & 712 & 1410 & 0.50 \\ 
    ##   German\_deu & fiction & Latn & 9.91 & 233110 & 5074046 & 0.05 \\ 
    ##   German\_deu & non-fiction & Latn & 9.68 & 135986 & 5696371 & 0.02 \\ 
    ##   German\_deu & professional & Latn & 8.25 & 642 & 1642 & 0.39 \\ 
    ##   Gooniyandi\_gni & conversation & Latn & 8.64 & 64 & 84 & 0.76 \\ 
    ##   Greek\_Modern\_ell & fiction & Grek & 8.96 & 289990 & 5054722 & 0.06 \\ 
    ##   Greek\_Modern\_ell & non-fiction & Grek & 8.47 & 174685 & 5738930 & 0.03 \\ 
    ##   Greek\_Modern\_ell & professional & Grek & 7.54 & 1394 & 3822 & 0.36 \\ 
    ##   Greenlandic\_West\_kal & non-fiction & Latn & 14.35 & 27006 & 62436 & 0.43 \\ 
    ##   Greenlandic\_West\_kal & professional & Latn & 15.78 & 714 & 1071 & 0.67 \\ 
    ##    & non-fiction & Latn & 8.58 & 12766 & 141501 & 0.09 \\ 
    ##   Guarani\_gug & professional & Latn & 7.31 & 607 & 1189 & 0.51 \\ 
    ##   Hausa\_hau & non-fiction & Latn & 6.87 & 6865 & 177554 & 0.04 \\ 
    ##   Hausa\_hau & professional & Latn & 5.57 & 602 & 5444 & 0.11 \\ 
    ##   Hebrew\_Modern\_heb & fiction & Hebr & 5.24 & 27281 & 114252 & 0.24 \\ 
    ##   Hebrew\_Modern\_heb & non-fiction & Hebr & 6.08 & 162005 & 5021329 & 0.03 \\ 
    ##   Hebrew\_Modern\_heb & professional & Hebr & 5.12 & 786 & 1278 & 0.62 \\ 
    ##   Hindi\_hin & non-fiction & Deva & 6.16 & 34985 & 1252888 & 0.03 \\ 
    ##   Hindi\_hin & non-fiction & Latn & 7.38 & 20395 & 792187 & 0.03 \\ 
    ##   Hindi\_hin & professional & Deva & 5.36 & 653 & 2076 & 0.31 \\ 
    ##   Hixkaryana\_hix & non-fiction & Latn & 9.28 & 3732 & 43568 & 0.09 \\ 
    ##   HmongNjua\_hnj & professional & Latn & 4.05 & 486 & 2801 & 0.17 \\ 
    ##   Imonda\_imn & non-fiction & Latn & 5.48 & 181 & 296 & 0.61 \\ 
    ##   Indonesian\_ind & non-fiction & Latn & 8.01 & 82826 & 5719697 & 0.01 \\ 
    ##   Indonesian\_ind & professional & Latn & 7.30 & 558 & 1726 & 0.32 \\ 
    ##   Jakaltek\_jac & non-fiction & Latn & 8.97 & 11762 & 220787 & 0.05 \\ 
    ##   Japanese\_jpn & fiction & Jpan & 2.59 & 26967 & 955184 & 0.03 \\ 
    ##   Japanese\_jpn & non-fiction & Jpan & 3.55 & 53221 & 5213332 & 0.01 \\ 
    ##   Japanese\_jpn & professional & Jpan & 2.08 & 526 & 2161 & 0.24 \\ 
    ##   Kannada\_kan & professional & Knda & 9.28 & 715 & 1081 & 0.66 \\ 
    ##   Kayardild\_gyd & grammar & Latn & 10.08 & 25 & 27 & 0.93 \\ 
    ##   Kewa\_kew & non-fiction & Latn & 7.29 & 10147 & 272299 & 0.04 \\ 
    ##   Khalkha\_khk & non-fiction & Latn & 8.10 & 15945 & 138743 & 0.11 \\ 
    ##   Khalkha\_khk & professional & Cyrl & 6.74 & 785 & 1548 & 0.51 \\ 
    ##   Khoekhoe\_naq & non-fiction & Latn & 7.20 & 10030 & 181370 & 0.06 \\ 
    ##   Kiowa\_kio & non-fiction & Latn & 3.38 & 81 & 154 & 0.53 \\ 
    ##   Korean\_kor & non-fiction & Hang & 3.82 & 62831 & 455182 & 0.14 \\ 
    ##   Korean\_kor & non-fiction & Kore & 4.28 & 379629 & 2917163 & 0.13 \\ 
    ##   Korean\_kor & professional & Hang & 3.20 & 658 & 1186 & 0.55 \\ 
    ##   Kutenai\_kut & non-fiction & Latn & 4.27 & 41 & 66 & 0.62 \\ 
    ##   Lango\_laj & non-fiction & Latn & 5.46 & 7316 & 174637 & 0.04 \\ 
    ##   Lavukaleve\_lvk & non-fiction & Latn & 5.57 & 564 & 1537 & 0.37 \\ 
    ##   Luvale\_lue & professional & Latn & 8.18 & 587 & 1216 & 0.48 \\ 
    ##   Makah\_myh & conversation & Latn & 9.93 & 120 & 145 & 0.83 \\ 
    ##   Makah\_myh & non-fiction & Latn & 8.68 & 19 & 33 & 0.58 \\ 
    ##   Malagasy\_plt & non-fiction & Latn & 8.99 & 30456 & 679065 & 0.04 \\ 
    ##   Malagasy\_plt & professional & Latn & 7.51 & 634 & 1857 & 0.34 \\ 
    ##   Mandarin\_cmn & fiction & Hans & 2.03 & 58133 & 4618542 & 0.01 \\ 
    ##   Mandarin\_cmn & non-fiction & Hans & 3.98 & 83494 & 4458428 & 0.02 \\ 
    ##   Mandarin\_cmn & professional & Hans & 1.88 & 581 & 1606 & 0.36 \\ 
    ##   Mandarin\_cmn & professional & Hant & 1.92 & 543 & 1488 & 0.36 \\ 
    ##   Mapudungun\_arn & non-fiction & Latn & 10.68 & 16630 & 193538 & 0.09 \\ 
    ##   Mapudungun\_arn & professional & Latn & 7.04 & 422 & 2620 & 0.16 \\ 
    ##   Martuthunira\_vma & conversation & Latn & 11.78 & 1162 & 3157 & 0.37 \\ 
    ##   Maung\_mph & non-fiction & Latn & 10.13 & 2540 & 22452 & 0.11 \\ 
    ##   Maybrat\_ayz & non-fiction & Latn & 3.70 & 192 & 737 & 0.26 \\ 
    ##   Mixtec\_Chalcatongo\_mig & non-fiction & Latn & 6.41 & 3988 & 226957 & 0.02 \\ 
    ##   Ngiyambaa\_wyb & conversation & Latn & 9.90 & 499 & 635 & 0.79 \\ 
    ##   Oromo\_Harar\_hae & non-fiction & Latn & 8.49 & 15944 & 163318 & 0.10 \\ 
    ##   Otomi\_Mezquital\_ote & grammar & Latn & 4.29 & 7 & 9 & 0.78 \\ 
    ##   Otomi\_Mezquital\_ote & non-fiction & Latn & 3.65 & 17 & 17 & 1.00 \\ 
    ##    & professional & Latn & 4.25 & 347 & 1849 & 0.19 \\ 
    ##   Persian\_pes & fiction & Arab & 5.27 & 6129 & 23201 & 0.26 \\ 
    ##   Persian\_pes & non-fiction & Arab & 6.85 & 166755 & 5189444 & 0.03 \\ 
    ##   Persian\_pes & professional & Arab & 5.03 & 641 & 1821 & 0.35 \\ 
    ##   Piraha\_myp & non-fiction & Latn & 4.94 & 647 & 6300 & 0.10 \\ 
    ##   Quechua\_Imbabura\_qvi & non-fiction & Latn & 11.21 & 18288 & 142011 & 0.13 \\ 
    ##   Rama\_rma & grammar & Latn & 7.12 & 271 & 400 & 0.68 \\ 
    ##   Rama\_rma & non-fiction & Latn & 6.67 & 94 & 169 & 0.56 \\ 
    ##   Rapanui\_rap & non-fiction & Latn & 4.55 & 367 & 2535 & 0.14 \\ 
    ##   Russian\_rus & fiction & Cyrl & 6.93 & 13576 & 54202 & 0.25 \\ 
    ##   Russian\_rus & non-fiction & Cyrl & 8.42 & 221031 & 5577162 & 0.04 \\ 
    ##   Russian\_rus & professional & Cyrl & 8.09 & 745 & 1611 & 0.46 \\ 
    ##   Sango\_sag & non-fiction & Latn & 5.51 & 1691 & 265302 & 0.01 \\ 
    ##   Sango\_sag & professional & Latn & 4.75 & 400 & 2257 & 0.18 \\ 
    ##   Sanuma\_xsu & non-fiction & Latn & 7.33 & 7983 & 408796 & 0.02 \\ 
    ##   Spanish\_spa & fiction & Latn & 8.34 & 141762 & 5057876 & 0.03 \\ 
    ##   Spanish\_spa & non-fiction & Latn & 8.19 & 105675 & 5709621 & 0.02 \\ 
    ##   Spanish\_spa & professional & Latn & 7.41 & 601 & 1927 & 0.31 \\ 
    ##   Swahili\_swh & non-fiction & Latn & 8.83 & 16317 & 128853 & 0.13 \\ 
    ##   Swahili\_swh & professional & Latn & 6.57 & 529 & 1786 & 0.30 \\ 
    ##   Tagalog\_tgl & fiction & Latn & 8.73 & 83392 & 949474 & 0.09 \\ 
    ##   Tagalog\_tgl & non-fiction & Latn & 8.69 & 29737 & 891858 & 0.03 \\ 
    ##   Tagalog\_tgl & professional & Latn & 7.81 & 591 & 2083 & 0.28 \\ 
    ##   Thai\_tha & non-fiction & Thai & 5.77 & 57096 & 6662914 & 0.01 \\ 
    ##   Thai\_tha & professional & Thai & 4.51 & 538 & 2331 & 0.23 \\ 
    ##   Turkish\_tur & non-fiction & Latn & 9.62 & 300142 & 5468060 & 0.05 \\ 
    ##   Turkish\_tur & professional & Latn & 7.52 & 729 & 1364 & 0.53 \\ 
    ##   Vietnamese\_vie & non-fiction & Latn & 5.84 & 34381 & 5865544 & 0.01 \\ 
    ##   Vietnamese\_vie & professional & Latn & 4.08 & 554 & 2502 & 0.22 \\ 
    ##   Vietnamese\_vie & professional & Hani & 1.44 & 567 & 1990 & 0.28 \\ 
    ##   Warao\_wba & non-fiction & Latn & 6.62 & 185 & 351 & 0.53 \\ 
    ##   Wichi\_mzh & non-fiction & Latn & 9.13 & 24348 & 720572 & 0.03 \\ 
    ##   Wichita\_wic & conversation & Latn & 13.22 & 348 & 529 & 0.66 \\ 
    ##   Yagua\_yad & non-fiction & Latn & 12.00 & 21829 & 142301 & 0.15 \\ 
    ##   Yagua\_yad & professional & Latn & 8.68 & 636 & 1180 & 0.54 \\ 
    ##   Yaqui\_yaq & non-fiction & Latn & 8.90 & 14013 & 240424 & 0.06 \\ 
    ##   Yoruba\_yor & non-fiction & Latn & 5.75 & 12744 & 790879 & 0.02 \\ 
    ##   Yoruba\_yor & professional & Latn & 5.05 & 512 & 2548 & 0.20 \\ 
    ##   Zoque\_Copainala\_zoc & non-fiction & Latn & 7.62 & 420 & 846 & 0.50 \\ 
    ##   Zulu\_zul & professional & Latn & 9.00 & 710 & 1077 & 0.66 \\ 
    ##   \hline
    ## \end{longtable}

# Grapheme TTR

We generate the grapheme TTR figures here:

-   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/get_grapheme_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/get_grapheme_ttr.md</a>

Let’s load the results from that report.

    grapheme_ttr <- read_csv("../ttr/grapheme_ttr.csv")

And have a look:

    grapheme_ttr %>%
      head() %>%
      kable()

| name                  | genre\_broad | types |  tokens |       ttr |
|:----------------------|:-------------|------:|--------:|----------:|
| Abkhaz\_abk           | professional |    64 |   10003 | 0.0063981 |
| Acoma\_kjq            | non-fiction  |    43 |   15893 | 0.0027056 |
| Alamblak\_amp         | non-fiction  |    66 | 1290455 | 0.0000511 |
| Amele\_aey            | non-fiction  |    68 | 1160739 | 0.0000586 |
| Apurina\_apu          | non-fiction  |    59 | 1247091 | 0.0000473 |
| Arabic\_Egyptian\_arz | non-fiction  |   426 | 1961436 | 0.0002172 |

Rename the columns to match in the paper.

    grapheme_ttr <- grapheme_ttr %>%
      rename("Language" = name,
             "Genre" = genre_broad,
             "Grapheme types" = types,
             "Grapheme tokens" = tokens,
             "Type-token ratio" = ttr)

    grapheme_ttr %>%
      head() %>%
      kable()

| Language              | Genre        | Grapheme types | Grapheme tokens | Type-token ratio |
|:----------------------|:-------------|---------------:|----------------:|-----------------:|
| Abkhaz\_abk           | professional |             64 |           10003 |        0.0063981 |
| Acoma\_kjq            | non-fiction  |             43 |           15893 |        0.0027056 |
| Alamblak\_amp         | non-fiction  |             66 |         1290455 |        0.0000511 |
| Amele\_aey            | non-fiction  |             68 |         1160739 |        0.0000586 |
| Apurina\_apu          | non-fiction  |             59 |         1247091 |        0.0000473 |
| Arabic\_Egyptian\_arz | non-fiction  |            426 |         1961436 |        0.0002172 |

    add_to_row <- list(pos = list(0), command = NULL)
    command <- paste0(
      "\\hline\n\\endhead\n",
      "\\hline\n",
      "\\multicolumn{", dim(grapheme_ttr)[2], "}{l}",
      "{\\footnotesize Continued on next page}\n",
      "\\endfoot\n",
      "\\endlastfoot\n"
    )
    add_to_row$command <- command
    print(xtable(grapheme_ttr,
                 digits = c(0, 0, 0, 0, 0, 2)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE,
          file = "grapheme_ttr.tex")

    ## Warning in print.xtable(xtable(grapheme_ttr, digits = c(0, 0, 0, 0, 0, 2)), :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

# Plots

For a [histrograph plot](https://github.com/uzling/100LC/pull/193) of
word ttr, see [plot\_ttr.md](../ttr/plot_ttr.md).
