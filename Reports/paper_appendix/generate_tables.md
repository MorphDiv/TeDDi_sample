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
                        # "Glottocode" = glottocode,
                        # "ISO 630-3" = iso639_3,
                        # "Endangerment" = status,
                        "Genus" = genus_wals,
                        "Area" = macroarea_glotto,
                        "Size (in words)" = corpus_size)

How about this for a descriptive table of the languages in the 100LC
sample?

    df %>%
      head(n = 30) %>%
      kable()

| Language name           | glottocode | iso639\_3 | status                | Genus                        | Area          | Size (in words) |
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
    ## % Sat Oct 31 12:33:39 2020
    ## \begin{longtable}{llllllr}
    ##   \hline
    ## Language name & glottocode & iso639\_3 & status & Genus & Area & Size (in words) \\ 
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

Rename the columns to match in the paper.

    word_ttr <- word_ttr %>%
      rename("Language" = name,
             "Genre" = genre_broad,
             "Word types" = types,
             "Word tokens" = tokens,
             "Type-token ratio" = ttr)

    word_ttr %>%
      head() %>%
      kable()

| Language              | Genre        | writing\_system | Word types | Word tokens | mean\_word\_length | Type-token ratio |
|:----------------------|:-------------|:----------------|-----------:|------------:|-------------------:|-----------------:|
| Abkhaz\_abk           | professional | Cyrl            |        787 |        1332 |           7.936468 |        0.5908408 |
| Acoma\_kjq            | non-fiction  | Latn            |        849 |        3341 |           5.361602 |        0.2541155 |
| Alamblak\_amp         | non-fiction  | Latn            |      25322 |      229160 |           8.520930 |        0.1104992 |
| Amele\_aey            | non-fiction  | Latn            |      14139 |      233776 |           7.803027 |        0.0604810 |
| Apurina\_apu          | non-fiction  | Latn            |      14699 |      159164 |          11.055038 |        0.0923513 |
| Arabic\_Egyptian\_arz | non-fiction  | Arab            |      74262 |      434040 |          10.090800 |        0.1710948 |

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
                 digits = c(0, 0, 0, 0, 0, 0, 2, 2)),
          hline.after = c(-1),
          add_to_row = add_to_row,
          tabular.environment = "longtable",
          include.rownames = FALSE,
          file = "word_ttr.tex")

    ## Warning in print.xtable(xtable(word_ttr, digits = c(0, 0, 0, 0, 0, 0, 2, :
    ## Attempt to use "longtable" with floating = TRUE. Changing to FALSE.

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
