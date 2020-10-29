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

Decide what we want to keep from the language index and create a LaTeX
(long) table for the paper submission.

    df <- index %>% select(name_glotto, glottocode, iso639_3, status, genus_wals, macroarea_glotto) %>% arrange(name_glotto)

Rename the columns.

    df <- df %>% rename('Language name' = name_glotto, 'Glottocode' = glottocode, 'ISO 630-3' = iso639_3, 'Endangerment' = status, 'Genus' = genus_wals, 'Area' = macroarea_glotto)

How about this for a descriptive table of the languages in the 100 LC
sample?

    df %>% head() %>% kable()

| Language name   | Glottocode | ISO 630-3 | Endangerment          | Genus               | Area          |
|:----------------|:-----------|:----------|:----------------------|:--------------------|:--------------|
| Abkhazian       | abkh1244   | abk       | vulnerable            | Northwest Caucasian | Eurasia       |
| Alamblak        | alam1246   | amp       | definitely endangered | Sepik Hill          | Papunesia     |
| Amele           | amel1241   | aey       | vulnerable            | Madang              | Papunesia     |
| Apurinã         | apur1254   | apu       | definitely endangered | Purus               | South America |
| Bagirmi         | bagi1246   | bmi       | safe                  | Bongo-Bagirmi       | Africa        |
| Barasana-Eduria | bara1380   | bsn       | definitely endangered | Tucanoan            | South America |

Dump an xtable (`longtable` in latex) for the paper. Currently, I just
copy and paste the table into the Overleaf document.

    add.to.row <- list(pos = list(0), command = NULL)
    command <- paste0("\\hline\n\\endhead\n",
                    "\\hline\n",
                    "\\multicolumn{", dim(df)[2] + 1, "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(df), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE)

    ## Warning in print.xtable(xtable(df), hline.after = c(-1), add.to.row =
    ## add.to.row, : Attempt to use "longtable" with floating = TRUE. Changing to
    ## FALSE.

    ## % latex table generated in R 4.0.3 by xtable 1.8-4 package
    ## % Thu Oct 29 14:26:32 2020
    ## \begin{longtable}{llllll}
    ##   \hline
    ## Language name & Glottocode & ISO 630-3 & Endangerment & Genus & Area \\ 
    ##   \hline
    ## \endhead
    ## \hline
    ## \multicolumn{7}{l}{\footnotesize Continued on next page}
    ## \endfoot
    ## \endlastfoot
    ## Abkhazian & abkh1244 & abk & vulnerable & Northwest Caucasian & Eurasia \\ 
    ##   Alamblak & alam1246 & amp & definitely endangered & Sepik Hill & Papunesia \\ 
    ##   Amele & amel1241 & aey & vulnerable & Madang & Papunesia \\ 
    ##   Apurinã & apur1254 & apu & definitely endangered & Purus & South America \\ 
    ##   Bagirmi & bagi1246 & bmi & safe & Bongo-Bagirmi & Africa \\ 
    ##   Barasana-Eduria & bara1380 & bsn & definitely endangered & Tucanoan & South America \\ 
    ##   Barclayville Grebo & barc1235 & gry & safe & Kru & Africa \\ 
    ##   Basque & basq1248 & eus & vulnerable & Basque & Eurasia \\ 
    ##   Bukiyip & buki1249 & ape & definitely endangered & Kombio-Arapesh & Papunesia \\ 
    ##   Burmese & nucl1310 & mya & definitely endangered & Burmese-Lolo & Eurasia \\ 
    ##   Burushaski & buru1296 & bsk & definitely endangered & Burushaski & Eurasia \\ 
    ##   Canela-Krahô & cane1242 & ram & definitely endangered & Ge-Kaingang & South America \\ 
    ##   Central Moroccan Berber & cent2194 & tzm & safe & Berber & Africa \\ 
    ##   Chamorro & cham1312 & cha & vulnerable & Chamorro & Papunesia \\ 
    ##   Chukchi & chuk1273 & ckt & definitely endangered & Northern Chukotko-Kamchatkan & Eurasia \\ 
    ##   Copainalá Zoque & copa1236 & zoc & definitely endangered & Mixe-Zoque & North America \\ 
    ##   Daga & daga1275 & dgz & safe & Dagan & Papunesia \\ 
    ##   Eastern Oromo & east2652 & hae & safe & Lowland East Cushitic & Africa \\ 
    ##   Egyptian Arabic & egyp1253 & arz & safe & Semitic & Africa \\ 
    ##   English & stan1293 & eng & safe & Germanic & Eurasia \\ 
    ##   Fijian & fiji1243 & fij & safe & Oceanic & Papunesia \\ 
    ##   Finnish & finn1318 & fin & safe & Finnic & Eurasia \\ 
    ##   French & stan1290 & fra & safe & Romance & Eurasia \\ 
    ##   Georgian & nucl1302 & kat & safe & Kartvelian & Eurasia \\ 
    ##   German & stan1295 & deu & safe & Germanic & Eurasia \\ 
    ##   Gooniyandi & goon1238 & gni & severely endangered & Bunuban & Australia \\ 
    ##   Halh Mongolian & halh1238 & khk & definitely endangered & Mongolic & Eurasia \\ 
    ##   Hausa & haus1257 & hau & safe & West Chadic & Africa \\ 
    ##   Hindi & hind1269 & hin & safe & Indic & Eurasia \\ 
    ##   Hixkaryána & hixk1239 & hix & definitely endangered & Cariban & South America \\ 
    ##   Hmong Njua & hmon1264 & hnj & safe & Hmong-Mien & Eurasia \\ 
    ##   Imbabura Highland Quichua & imba1240 & qvi & vulnerable & Quechuan & South America \\ 
    ##   Imonda & imon1245 & imn & definitely endangered & Border & Papunesia \\ 
    ##   Indonesian & indo1316 & ind & safe & Malayo-Sumbawan & Papunesia \\ 
    ##   Japanese & nucl1643 & jpn & safe & Japanese & Eurasia \\ 
    ##   Kalaallisut & kala1399 & kal & vulnerable & Eskimo & Eurasia \\ 
    ##   Kannada & nucl1305 & kan & critically endangered & Southern Dravidian & Eurasia \\ 
    ##   Karok & karo1304 & kyh & critically endangered & Karok & North America \\ 
    ##   Kayardild & kaya1319 & gyd & critically endangered & Tangkic & Australia \\ 
    ##   Kiowa & kiow1266 & kio & critically endangered & Kiowa-Tanoan & North America \\ 
    ##   Koasati & koas1236 & cku & severely endangered & Muskogean & North America \\ 
    ##   Korean & kore1280 & kor & safe & Korean & Eurasia \\ 
    ##   Koyraboro Senni Songhai & koyr1242 & ses & safe & Songhay & Africa \\ 
    ##   Krongo & kron1241 & kgo & vulnerable & Kadugli & Africa \\ 
    ##   Kutenai & kute1249 & kut & severely endangered & Kutenai & North America \\ 
    ##   Lakota & lako1247 & lkt & definitely endangered & Core Siouan & North America \\ 
    ##   Lango (Uganda) & lang1324 & laj & safe & Nilotic & Africa \\ 
    ##   Lavukaleve & lavu1241 & lvk & definitely endangered & Lavukaleve & Papunesia \\ 
    ##   Lezgian & lezg1247 & lez & vulnerable & Lezgic & Eurasia \\ 
    ##   Lower Grand Valley Dani & lowe1415 & dni & safe & Dani & Papunesia \\ 
    ##   Luvale & luva1239 & lue & safe & Bantoid & Africa \\ 
    ##   Makah & maka1318 & myh & extinct & Southern Wakashan & North America \\ 
    ##   Mandarin Chinese & mand1415 & cmn & safe & Chinese & Eurasia \\ 
    ##   Mangarrayi & mang1381 & mpc & critically endangered & Mangarrayi & Australia \\ 
    ##   Manipuri & mani1292 & mni & vulnerable & Kuki-Chin & Eurasia \\ 
    ##   Mapudungun & mapu1245 & arn & definitely endangered & Araucanian & South America \\ 
    ##   Maricopa & mari1440 & mrc & severely endangered & Yuman & North America \\ 
    ##   Martuthunira & mart1255 & vma & critically endangered & Western Pama-Nyungan & Australia \\ 
    ##   Mawng & maun1240 & mph & vulnerable & Iwaidjan & Australia \\ 
    ##   Maybrat-Karon & maib1239 & ayz & safe & North-Central Bird's Head & Papunesia \\ 
    ##   Mezquital Otomi & mezq1235 & ote & safe & Otomian & North America \\ 
    ##   Modern Greek & mode1248 & ell & severely endangered & Greek & Eurasia \\ 
    ##   Modern Hebrew & hebr1245 & heb & safe & Semitic & Eurasia \\ 
    ##   Nama (Namibia) & nama1264 & naq & vulnerable & Khoe-Kwadi & Africa \\ 
    ##   Ngiyambaa & wang1291 & wyb & critically endangered & Southeastern Pama-Nyungan & Australia \\ 
    ##   North Slavey & nort2942 & scs & definitely endangered & Athapaskan & North America \\ 
    ##   Oneida & onei1249 & one & definitely endangered & Northern Iroquoian & North America \\ 
    ##   Paiwan & paiw1248 & pwn & vulnerable & Paiwan & Papunesia \\ 
    ##   Paraguayan Guaraní & para1311 & gug & safe & Tupi-Guaraní & South America \\ 
    ##   Pirahã & pira1253 & myp & vulnerable & Mura & South America \\ 
    ##   Plains Cree & plai1258 & crk & severely endangered & Algonquian & North America \\ 
    ##   Plateau Malagasy & plat1254 & plt & safe & Barito & Africa \\ 
    ##   Popti' & popt1235 & jac & vulnerable & Mayan & North America \\ 
    ##   Rama & rama1270 & rma & critically endangered & Rama & North America \\ 
    ##   Rapanui & rapa1244 & rap & definitely endangered & Oceanic & Papunesia \\ 
    ##   Russian & russ1263 & rus & critically endangered & Slavic & Eurasia \\ 
    ##   San Miguel El Grande Mixtec & sanm1295 & mig & vulnerable & Mixtecan & North America \\ 
    ##   Sango & sang1328 & sag & safe & Ubangi & Africa \\ 
    ##   Sanumá & sanu1240 & xsu & definitely endangered & Yanomam & South America \\ 
    ##   Spanish & stan1288 & spa & safe & Romance & Eurasia \\ 
    ##   Supyire Senoufo & supy1237 & spp & safe & Gur & Africa \\ 
    ##   Swahili & swah1253 & swh & definitely endangered & Bantoid & Africa \\ 
    ##   Tagalog & taga1270 & tgl & safe & Greater Central Philippine & Papunesia \\ 
    ##   Tamnim Citak & tamn1235 & tml & safe & Asmat-Kamoro & Papunesia \\ 
    ##   Thai & thai1261 & tha & safe & Kam-Tai & Eurasia \\ 
    ##   Tiwi & tiwi1244 & tiw & definitely endangered & Tiwian & Australia \\ 
    ##   Tukang Besi South & tuka1249 & bhq & safe & Celebic & Papunesia \\ 
    ##   Turkish & nucl1301 & tur & safe & Turkic & Eurasia \\ 
    ##   Vietnamese & viet1252 & vie & safe & Viet-Muong & Eurasia \\ 
    ##   Warao & wara1303 & wba & vulnerable & Warao & South America \\ 
    ##   Wari' & wari1268 & pav & definitely endangered & Chapacura-Wanham & South America \\ 
    ##   West Kewa & west2599 & kew & safe & Engan & Papunesia \\ 
    ##   Western Farsi & west2369 & pes & safe & Iranian & Eurasia \\ 
    ##   Western Keres & west2632 & kjq & definitely endangered & Keresan & North America \\ 
    ##   Wichí Lhamtés Güisnay & wich1264 & mzh & vulnerable & Matacoan & South America \\ 
    ##   Wichita & wich1260 & wic & extinct & Caddoan & North America \\ 
    ##   Yagua & yagu1244 & yad & definitely endangered & Peba-Yaguan & South America \\ 
    ##   Yaqui & yaqu1251 & yaq & vulnerable & Cahita & North America \\ 
    ##   Yoruba & yoru1245 & yor & safe & Defoid & Africa \\ 
    ##   Zulu & zulu1248 & zul & safe & Bantoid & Africa \\ 
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
                    "\\multicolumn{", dim(word_ttr)[2] + 1, "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(word_ttr), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE)

    ## Warning in print.xtable(xtable(word_ttr), hline.after = c(-1), add.to.row =
    ## add.to.row, : Attempt to use "longtable" with floating = TRUE. Changing to
    ## FALSE.

    ## % latex table generated in R 4.0.3 by xtable 1.8-4 package
    ## % Thu Oct 29 14:26:32 2020
    ## \begin{longtable}{llrrr}
    ##   \hline
    ## Language & Genre & Word types & Word tokens & Type-token ratio \\ 
    ##   \hline
    ## \endhead
    ## \hline
    ## \multicolumn{6}{l}{\footnotesize Continued on next page}
    ## \endfoot
    ## \endlastfoot
    ## Abkhaz\_abk & professional & 787.00 & 1332.00 & 0.59 \\ 
    ##   Acoma\_kjq & non-fiction & 849.00 & 3341.00 & 0.25 \\ 
    ##   Alamblak\_amp & non-fiction & 25322.00 & 229160.00 & 0.11 \\ 
    ##   Amele\_aey & non-fiction & 14139.00 & 233776.00 & 0.06 \\ 
    ##   Apurina\_apu & non-fiction & 14699.00 & 159164.00 & 0.09 \\ 
    ##   Arabic\_Egyptian\_arz & non-fiction & 74262.00 & 434040.00 & 0.17 \\ 
    ##   Arapesh\_Mountain\_ape & non-fiction & 14890.00 & 270754.00 & 0.05 \\ 
    ##   Asmat\_tml & conversation & 99.00 & 141.00 & 0.70 \\ 
    ##   Bagirmi\_bmi & grammar & 53.00 & 71.00 & 0.75 \\ 
    ##   Barasano\_bsn & non-fiction & 17089.00 & 221691.00 & 0.08 \\ 
    ##   Basque\_eus & non-fiction & 126640.00 & 2715508.00 & 0.05 \\ 
    ##   Basque\_eus & professional & 707.00 & 1407.00 & 0.50 \\ 
    ##   Berber\_MiddleAtlas\_tzm & professional & 670.00 & 1869.00 & 0.36 \\ 
    ##   Burmese\_mya & non-fiction & 6381.00 & 908516.00 & 0.01 \\ 
    ##   Burmese\_mya & professional & 665.00 & 2966.00 & 0.22 \\ 
    ##   Burushaski\_bsk & grammar & 123.00 & 198.00 & 0.62 \\ 
    ##   CanelaKraho\_ram & non-fiction & 3043.00 & 51061.00 & 0.06 \\ 
    ##   Chamorro\_cha & non-fiction & 9653.00 & 198523.00 & 0.05 \\ 
    ##   Chamorro\_cha & professional & 571.00 & 1951.00 & 0.29 \\ 
    ##   Chukchi\_ckt & non-fiction & 5192.00 & 16442.00 & 0.32 \\ 
    ##   Daga\_dgz & non-fiction & 7839.00 & 214348.00 & 0.04 \\ 
    ##   Dani\_LowerGrandValley\_dni & conversation & 160.00 & 337.00 & 0.47 \\ 
    ##   English\_eng & fiction & 80966.00 & 5073103.00 & 0.02 \\ 
    ##   English\_eng & non-fiction & 60787.00 & 5711261.00 & 0.01 \\ 
    ##   English\_eng & professional & 534.00 & 1753.00 & 0.30 \\ 
    ##   Fijian\_fij & non-fiction & 3636.00 & 227543.00 & 0.02 \\ 
    ##   Fijian\_fij & professional & 396.00 & 2096.00 & 0.19 \\ 
    ##   Finnish\_fin & fiction & 366900.00 & 5021399.00 & 0.07 \\ 
    ##   Finnish\_fin & non-fiction & 340673.00 & 5549590.00 & 0.06 \\ 
    ##   Finnish\_fin & professional & 824.00 & 1400.00 & 0.59 \\ 
    ##   French\_fra & fiction & 133702.00 & 4814508.00 & 0.03 \\ 
    ##   French\_fra & non-fiction & 97156.00 & 5436716.00 & 0.02 \\ 
    ##   French\_fra & professional & 647.00 & 1946.00 & 0.33 \\ 
    ##   Georgian\_kat & non-fiction & 81798.00 & 827965.00 & 0.10 \\ 
    ##   Georgian\_kat & professional & 712.00 & 1410.00 & 0.50 \\ 
    ##   German\_deu & fiction & 233110.00 & 5074046.00 & 0.05 \\ 
    ##   German\_deu & non-fiction & 135986.00 & 5696371.00 & 0.02 \\ 
    ##   German\_deu & professional & 642.00 & 1642.00 & 0.39 \\ 
    ##   Gooniyandi\_gni & conversation & 60.00 & 79.00 & 0.76 \\ 
    ##   Greek\_Modern\_ell & fiction & 289990.00 & 5054722.00 & 0.06 \\ 
    ##   Greek\_Modern\_ell & non-fiction & 174685.00 & 5738930.00 & 0.03 \\ 
    ##   Greek\_Modern\_ell & professional & 1394.00 & 3822.00 & 0.36 \\ 
    ##   Greenlandic\_West\_kal & non-fiction & 27006.00 & 62436.00 & 0.43 \\ 
    ##   Greenlandic\_West\_kal & professional & 714.00 & 1071.00 & 0.67 \\ 
    ##   Guarani\_gug & non-fiction & 12766.00 & 141501.00 & 0.09 \\ 
    ##   Guarani\_gug & professional & 607.00 & 1189.00 & 0.51 \\ 
    ##   Hausa\_hau & non-fiction & 6865.00 & 177554.00 & 0.04 \\ 
    ##   Hausa\_hau & professional & 602.00 & 5444.00 & 0.11 \\ 
    ##   Hebrew\_Modern\_heb & fiction & 27281.00 & 114252.00 & 0.24 \\ 
    ##   Hebrew\_Modern\_heb & non-fiction & 162005.00 & 5021329.00 & 0.03 \\ 
    ##   Hebrew\_Modern\_heb & professional & 786.00 & 1278.00 & 0.62 \\ 
    ##   Hindi\_hin & non-fiction & 55189.00 & 2045075.00 & 0.03 \\ 
    ##   Hindi\_hin & professional & 653.00 & 2076.00 & 0.31 \\ 
    ##   Hixkaryana\_hix & non-fiction & 3732.00 & 43568.00 & 0.09 \\ 
    ##   HmongNjua\_hnj & professional & 486.00 & 2801.00 & 0.17 \\ 
    ##   Imonda\_imn & non-fiction & 177.00 & 289.00 & 0.61 \\ 
    ##   Indonesian\_ind & non-fiction & 82826.00 & 5719697.00 & 0.01 \\ 
    ##   Indonesian\_ind & professional & 558.00 & 1726.00 & 0.32 \\ 
    ##   Jakaltek\_jac & non-fiction & 11762.00 & 220787.00 & 0.05 \\ 
    ##   Japanese\_jpn & fiction & 26967.00 & 955184.00 & 0.03 \\ 
    ##   Japanese\_jpn & non-fiction & 53221.00 & 5213332.00 & 0.01 \\ 
    ##   Japanese\_jpn & professional & 526.00 & 2161.00 & 0.24 \\ 
    ##   Kannada\_kan & professional & 715.00 & 1081.00 & 0.66 \\ 
    ##   Kayardild\_gyd & grammar & 21.00 & 22.00 & 0.95 \\ 
    ##   Kewa\_kew & non-fiction & 10147.00 & 272299.00 & 0.04 \\ 
    ##   Khalkha\_khk & non-fiction & 15945.00 & 138743.00 & 0.11 \\ 
    ##   Khalkha\_khk & professional & 785.00 & 1548.00 & 0.51 \\ 
    ##   Khoekhoe\_naq & non-fiction & 10030.00 & 181370.00 & 0.06 \\ 
    ##   Kiowa\_kio & non-fiction & 75.00 & 148.00 & 0.51 \\ 
    ##   Korean\_kor & non-fiction & 425846.00 & 3372345.00 & 0.13 \\ 
    ##   Korean\_kor & professional & 658.00 & 1186.00 & 0.55 \\ 
    ##   Kutenai\_kut & non-fiction & 37.00 & 60.00 & 0.62 \\ 
    ##   Lango\_laj & non-fiction & 7316.00 & 174637.00 & 0.04 \\ 
    ##   Lavukaleve\_lvk & non-fiction & 562.00 & 1524.00 & 0.37 \\ 
    ##   Luvale\_lue & professional & 587.00 & 1216.00 & 0.48 \\ 
    ##   Makah\_myh & conversation & 114.00 & 138.00 & 0.83 \\ 
    ##   Makah\_myh & non-fiction & 19.00 & 29.00 & 0.66 \\ 
    ##   Malagasy\_plt & non-fiction & 30456.00 & 679065.00 & 0.04 \\ 
    ##   Malagasy\_plt & professional & 634.00 & 1857.00 & 0.34 \\ 
    ##   Mandarin\_cmn & fiction & 58133.00 & 4618542.00 & 0.01 \\ 
    ##   Mandarin\_cmn & non-fiction & 83494.00 & 4458428.00 & 0.02 \\ 
    ##   Mandarin\_cmn & professional & 845.00 & 3094.00 & 0.27 \\ 
    ##   Mapudungun\_arn & non-fiction & 16630.00 & 193538.00 & 0.09 \\ 
    ##   Mapudungun\_arn & professional & 422.00 & 2620.00 & 0.16 \\ 
    ##   Martuthunira\_vma & conversation & 1155.00 & 3133.00 & 0.37 \\ 
    ##   Maung\_mph & non-fiction & 2540.00 & 22452.00 & 0.11 \\ 
    ##   Maybrat\_ayz & non-fiction & 191.00 & 726.00 & 0.26 \\ 
    ##   Mixtec\_Chalcatongo\_mig & non-fiction & 3988.00 & 226957.00 & 0.02 \\ 
    ##   Ngiyambaa\_wyb & conversation & 18.00 & 22.00 & 0.82 \\ 
    ##   Oromo\_Harar\_hae & non-fiction & 15944.00 & 163318.00 & 0.10 \\ 
    ##   Otomi\_Mezquital\_ote & professional & 347.00 & 1849.00 & 0.19 \\ 
    ##   Persian\_pes & fiction & 6129.00 & 23201.00 & 0.26 \\ 
    ##   Persian\_pes & non-fiction & 166755.00 & 5189444.00 & 0.03 \\ 
    ##   Persian\_pes & professional & 641.00 & 1821.00 & 0.35 \\ 
    ##   Quechua\_Imbabura\_qvi & non-fiction & 18288.00 & 142011.00 & 0.13 \\ 
    ##   Rama\_rma & grammar & 270.00 & 396.00 & 0.68 \\ 
    ##   Rama\_rma & non-fiction & 92.00 & 164.00 & 0.56 \\ 
    ##   Rapanui\_rap & non-fiction & 362.00 & 2464.00 & 0.15 \\ 
    ##   Russian\_rus & fiction & 13576.00 & 54202.00 & 0.25 \\ 
    ##   Russian\_rus & non-fiction & 221031.00 & 5577162.00 & 0.04 \\ 
    ##   Russian\_rus & professional & 745.00 & 1611.00 & 0.46 \\ 
    ##   Sango\_sag & non-fiction & 1691.00 & 265302.00 & 0.01 \\ 
    ##   Sango\_sag & professional & 400.00 & 2257.00 & 0.18 \\ 
    ##   Sanuma\_xsu & non-fiction & 7983.00 & 408796.00 & 0.02 \\ 
    ##   Spanish\_spa & fiction & 141762.00 & 5057876.00 & 0.03 \\ 
    ##   Spanish\_spa & non-fiction & 105675.00 & 5709621.00 & 0.02 \\ 
    ##   Spanish\_spa & professional & 601.00 & 1927.00 & 0.31 \\ 
    ##   Swahili\_swh & non-fiction & 16317.00 & 128853.00 & 0.13 \\ 
    ##   Swahili\_swh & professional & 529.00 & 1786.00 & 0.30 \\ 
    ##   Tagalog\_tgl & fiction & 83392.00 & 949474.00 & 0.09 \\ 
    ##   Tagalog\_tgl & non-fiction & 29737.00 & 891858.00 & 0.03 \\ 
    ##   Tagalog\_tgl & professional & 591.00 & 2083.00 & 0.28 \\ 
    ##   Thai\_tha & non-fiction & 57096.00 & 6662914.00 & 0.01 \\ 
    ##   Thai\_tha & professional & 538.00 & 2331.00 & 0.23 \\ 
    ##   Turkish\_tur & non-fiction & 300142.00 & 5468060.00 & 0.05 \\ 
    ##   Turkish\_tur & professional & 729.00 & 1364.00 & 0.53 \\ 
    ##   Vietnamese\_vie & non-fiction & 34381.00 & 5865544.00 & 0.01 \\ 
    ##   Vietnamese\_vie & professional & 1088.00 & 4492.00 & 0.24 \\ 
    ##   Warao\_wba & non-fiction & 183.00 & 346.00 & 0.53 \\ 
    ##   Wichi\_mzh & non-fiction & 24348.00 & 720572.00 & 0.03 \\ 
    ##   Wichita\_wic & conversation & 345.00 & 525.00 & 0.66 \\ 
    ##   Yagua\_yad & non-fiction & 21829.00 & 142301.00 & 0.15 \\ 
    ##   Yagua\_yad & professional & 636.00 & 1180.00 & 0.54 \\ 
    ##   Yaqui\_yaq & non-fiction & 14013.00 & 240424.00 & 0.06 \\ 
    ##   Yoruba\_yor & non-fiction & 12744.00 & 790879.00 & 0.02 \\ 
    ##   Yoruba\_yor & professional & 512.00 & 2548.00 & 0.20 \\ 
    ##   Zoque\_Copainala\_zoc & non-fiction & 417.00 & 839.00 & 0.50 \\ 
    ##   Zulu\_zul & professional & 710.00 & 1077.00 & 0.66 \\ 
    ##   \hline
    ## \end{longtable}

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
                    "\\multicolumn{", dim(grapheme_ttr)[2] + 1, "}{l}",
                    "{\\footnotesize Continued on next page}\n",
                    "\\endfoot\n",
                    "\\endlastfoot\n")
    add.to.row$command <- command
    print(xtable(grapheme_ttr), hline.after=c(-1), add.to.row = add.to.row, tabular.environment = "longtable", include.rownames=FALSE)

    ## Warning in print.xtable(xtable(grapheme_ttr), hline.after = c(-1), add.to.row
    ## = add.to.row, : Attempt to use "longtable" with floating = TRUE. Changing to
    ## FALSE.

    ## % latex table generated in R 4.0.3 by xtable 1.8-4 package
    ## % Thu Oct 29 14:26:32 2020
    ## \begin{longtable}{llrrr}
    ##   \hline
    ## Language & Genre & Grapheme types & Grapheme tokens & Type-token ratio \\ 
    ##   \hline
    ## \endhead
    ## \hline
    ## \multicolumn{6}{l}{\footnotesize Continued on next page}
    ## \endfoot
    ## \endlastfoot
    ## Abkhaz\_abk & professional & 64.00 & 10003.00 & 0.01 \\ 
    ##   Acoma\_kjq & non-fiction & 43.00 & 15893.00 & 0.00 \\ 
    ##   Alamblak\_amp & non-fiction & 66.00 & 1290455.00 & 0.00 \\ 
    ##   Amele\_aey & non-fiction & 68.00 & 1160739.00 & 0.00 \\ 
    ##   Apurina\_apu & non-fiction & 59.00 & 1247091.00 & 0.00 \\ 
    ##   Arabic\_Egyptian\_arz & non-fiction & 426.00 & 1961436.00 & 0.00 \\ 
    ##   Arapesh\_Mountain\_ape & non-fiction & 69.00 & 1510912.00 & 0.00 \\ 
    ##   Asmat\_tml & conversation & 32.00 & 870.00 & 0.04 \\ 
    ##   Bagirmi\_bmi & grammar & 47.00 & 210.00 & 0.22 \\ 
    ##   Barasano\_bsn & non-fiction & 90.00 & 1360928.00 & 0.00 \\ 
    ##   Basque\_eus & non-fiction & 172.00 & 16116015.00 & 0.00 \\ 
    ##   Basque\_eus & professional & 54.00 & 9623.00 & 0.01 \\ 
    ##   Berber\_MiddleAtlas\_tzm & professional & 70.00 & 8511.00 & 0.01 \\ 
    ##   Burmese\_mya & non-fiction & 663.00 & 2249570.00 & 0.00 \\ 
    ##   Burmese\_mya & professional & 273.00 & 8484.00 & 0.03 \\ 
    ##   Burushaski\_bsk & grammar & 40.00 & 925.00 & 0.04 \\ 
    ##   CanelaKraho\_ram & non-fiction & 73.00 & 192513.00 & 0.00 \\ 
    ##   Chamorro\_cha & non-fiction & 76.00 & 921354.00 & 0.00 \\ 
    ##   Chamorro\_cha & professional & 61.00 & 9910.00 & 0.01 \\ 
    ##   Chukchi\_ckt & non-fiction & 79.00 & 134477.00 & 0.00 \\ 
    ##   Daga\_dgz & non-fiction & 64.00 & 997386.00 & 0.00 \\ 
    ##   Dani\_LowerGrandValley\_dni & conversation & 33.00 & 1789.00 & 0.02 \\ 
    ##   English\_eng & fiction & 289.00 & 23630990.00 & 0.00 \\ 
    ##   English\_eng & non-fiction & 174.00 & 25054918.00 & 0.00 \\ 
    ##   English\_eng & professional & 56.00 & 8891.00 & 0.01 \\ 
    ##   Fijian\_fij & non-fiction & 59.00 & 861344.00 & 0.00 \\ 
    ##   Fijian\_fij & professional & 56.00 & 9094.00 & 0.01 \\ 
    ##   Finnish\_fin & fiction & 171.00 & 33106295.00 & 0.00 \\ 
    ##   Finnish\_fin & non-fiction & 163.00 & 35407637.00 & 0.00 \\ 
    ##   Finnish\_fin & professional & 56.00 & 10835.00 & 0.01 \\ 
    ##   French\_fra & fiction & 247.00 & 23767792.00 & 0.00 \\ 
    ##   French\_fra & non-fiction & 191.00 & 25150294.00 & 0.00 \\ 
    ##   French\_fra & professional & 60.00 & 9953.00 & 0.01 \\ 
    ##   Georgian\_kat & non-fiction & 173.00 & 3914602.00 & 0.00 \\ 
    ##   Georgian\_kat & professional & 46.00 & 10455.00 & 0.00 \\ 
    ##   German\_deu & fiction & 351.00 & 27780867.00 & 0.00 \\ 
    ##   German\_deu & non-fiction & 184.00 & 28779152.00 & 0.00 \\ 
    ##   German\_deu & professional & 70.00 & 10295.00 & 0.01 \\ 
    ##   Gooniyandi\_gni & conversation & 20.00 & 775.00 & 0.03 \\ 
    ##   Greek\_Modern\_ell & fiction & 358.00 & 25932449.00 & 0.00 \\ 
    ##   Greek\_Modern\_ell & non-fiction & 242.00 & 28844378.00 & 0.00 \\ 
    ##   Greek\_Modern\_ell & professional & 118.00 & 21056.00 & 0.01 \\ 
    ##   Greenlandic\_West\_kal & non-fiction & 71.00 & 726470.00 & 0.00 \\ 
    ##   Greenlandic\_West\_kal & professional & 50.00 & 15779.00 & 0.00 \\ 
    ##   Guarani\_gug & non-fiction & 94.00 & 813314.00 & 0.00 \\ 
    ##   Guarani\_gug & professional & 75.00 & 7882.00 & 0.01 \\ 
    ##   Hausa\_hau & non-fiction & 71.00 & 736578.00 & 0.00 \\ 
    ##   Hausa\_hau & professional & 61.00 & 23404.00 & 0.00 \\ 
    ##   Hebrew\_Modern\_heb & fiction & 358.00 & 488629.00 & 0.00 \\ 
    ##   Hebrew\_Modern\_heb & non-fiction & 392.00 & 21215980.00 & 0.00 \\ 
    ##   Hebrew\_Modern\_heb & professional & 31.00 & 5983.00 & 0.01 \\ 
    ##   Hindi\_hin & non-fiction & 1081.00 & 6540546.00 & 0.00 \\ 
    ##   Hindi\_hin & professional & 277.00 & 5821.00 & 0.05 \\ 
    ##   Hixkaryana\_hix & non-fiction & 49.00 & 247518.00 & 0.00 \\ 
    ##   HmongNjua\_hnj & professional & 57.00 & 10880.00 & 0.01 \\ 
    ##   Imonda\_imn & non-fiction & 25.00 & 1599.00 & 0.02 \\ 
    ##   Indonesian\_ind & non-fiction & 265.00 & 32402441.00 & 0.00 \\ 
    ##   Indonesian\_ind & professional & 52.00 & 10865.00 & 0.00 \\ 
    ##   Jakaltek\_jac & non-fiction & 68.00 & 1154758.00 & 0.00 \\ 
    ##   Japanese\_jpn & fiction & 4349.00 & 1626514.00 & 0.00 \\ 
    ##   Japanese\_jpn & non-fiction & 3843.00 & 9365709.00 & 0.00 \\ 
    ##   Japanese\_jpn & professional & 505.00 & 4091.00 & 0.12 \\ 
    ##   Kannada\_kan & professional & 287.00 & 5862.00 & 0.05 \\ 
    ##   Kayardild\_gyd & grammar & 21.00 & 221.00 & 0.10 \\ 
    ##   Kewa\_kew & non-fiction & 64.00 & 1255293.00 & 0.00 \\ 
    ##   Khalkha\_khk & non-fiction & 59.00 & 783108.00 & 0.00 \\ 
    ##   Khalkha\_khk & professional & 54.00 & 9290.00 & 0.01 \\ 
    ##   Khoekhoe\_naq & non-fiction & 74.00 & 718250.00 & 0.00 \\ 
    ##   Kiowa\_kio & non-fiction & 42.00 & 581.00 & 0.07 \\ 
    ##   Korean\_kor & non-fiction & 2772.00 & 10433726.00 & 0.00 \\ 
    ##   Korean\_kor & professional & 315.00 & 3531.00 & 0.09 \\ 
    ##   Kutenai\_kut & non-fiction & 28.00 & 278.00 & 0.10 \\ 
    ##   Lango\_laj & non-fiction & 60.00 & 681594.00 & 0.00 \\ 
    ##   Lavukaleve\_lvk & non-fiction & 46.00 & 7575.00 & 0.01 \\ 
    ##   Luvale\_lue & professional & 52.00 & 8892.00 & 0.01 \\ 
    ##   Makah\_myh & conversation & 38.00 & 1378.00 & 0.03 \\ 
    ##   Makah\_myh & non-fiction & 27.00 & 233.00 & 0.12 \\ 
    ##   Malagasy\_plt & non-fiction & 84.00 & 3738533.00 & 0.00 \\ 
    ##   Malagasy\_plt & professional & 58.00 & 10681.00 & 0.01 \\ 
    ##   Mandarin\_cmn & fiction & 9453.00 & 7395033.00 & 0.00 \\ 
    ##   Mandarin\_cmn & non-fiction & 8659.00 & 9142941.00 & 0.00 \\ 
    ##   Mandarin\_cmn & professional & 696.00 & 5592.00 & 0.12 \\ 
    ##   Mapudungun\_arn & non-fiction & 66.00 & 1067903.00 & 0.00 \\ 
    ##   Mapudungun\_arn & professional & 67.00 & 12523.00 & 0.01 \\ 
    ##   Martuthunira\_vma & conversation & 34.00 & 29771.00 & 0.00 \\ 
    ##   Maung\_mph & non-fiction & 66.00 & 135696.00 & 0.00 \\ 
    ##   Maybrat\_ayz & non-fiction & 32.00 & 2385.00 & 0.01 \\ 
    ##   Mixtec\_Chalcatongo\_mig & non-fiction & 76.00 & 877602.00 & 0.00 \\ 
    ##   Ngiyambaa\_wyb & conversation & 19.00 & 161.00 & 0.12 \\ 
    ##   Oromo\_Harar\_hae & non-fiction & 66.00 & 1000842.00 & 0.00 \\ 
    ##   Otomi\_Mezquital\_ote & grammar & 0.00 & 0.00 &  \\ 
    ##   Otomi\_Mezquital\_ote & non-fiction & 0.00 & 0.00 &  \\ 
    ##   Otomi\_Mezquital\_ote & professional & 72.00 & 6157.00 & 0.01 \\ 
    ##   Persian\_pes & fiction & 200.00 & 88721.00 & 0.00 \\ 
    ##   Persian\_pes & non-fiction & 642.00 & 21015634.00 & 0.00 \\ 
    ##   Persian\_pes & professional & 49.00 & 7146.00 & 0.01 \\ 
    ##   Piraha\_myp & non-fiction & 33.00 & 22722.00 & 0.00 \\ 
    ##   Quechua\_Imbabura\_qvi & non-fiction & 72.00 & 1226343.00 & 0.00 \\ 
    ##   Rama\_rma & grammar & 28.00 & 2595.00 & 0.01 \\ 
    ##   Rama\_rma & non-fiction & 23.00 & 1062.00 & 0.02 \\ 
    ##   Rapanui\_rap & non-fiction & 43.00 & 7924.00 & 0.01 \\ 
    ##   Russian\_rus & fiction & 150.00 & 267516.00 & 0.00 \\ 
    ##   Russian\_rus & non-fiction & 232.00 & 28327840.00 & 0.00 \\ 
    ##   Russian\_rus & professional & 66.00 & 10204.00 & 0.01 \\ 
    ##   Sango\_sag & non-fiction & 78.00 & 920017.00 & 0.00 \\ 
    ##   Sango\_sag & professional & 69.00 & 8196.00 & 0.01 \\ 
    ##   Sanuma\_xsu & non-fiction & 85.00 & 1511667.00 & 0.00 \\ 
    ##   Spanish\_spa & fiction & 200.00 & 24083125.00 & 0.00 \\ 
    ##   Spanish\_spa & non-fiction & 176.00 & 27079157.00 & 0.00 \\ 
    ##   Spanish\_spa & professional & 60.00 & 10038.00 & 0.01 \\ 
    ##   Swahili\_swh & non-fiction & 82.00 & 725026.00 & 0.00 \\ 
    ##   Swahili\_swh & professional & 62.00 & 8670.00 & 0.01 \\ 
    ##   Tagalog\_tgl & fiction & 154.00 & 4833124.00 & 0.00 \\ 
    ##   Tagalog\_tgl & non-fiction & 83.00 & 4355512.00 & 0.00 \\ 
    ##   Tagalog\_tgl & professional & 56.00 & 11363.00 & 0.00 \\ 
    ##   Thai\_tha & non-fiction & 2003.00 & 18366621.00 & 0.00 \\ 
    ##   Thai\_tha & professional & 262.00 & 7111.00 & 0.04 \\ 
    ##   Turkish\_tur & non-fiction & 180.00 & 33994537.00 & 0.00 \\ 
    ##   Turkish\_tur & professional & 56.00 & 8915.00 & 0.01 \\ 
    ##   Vietnamese\_vie & non-fiction & 371.00 & 20189329.00 & 0.00 \\ 
    ##   Vietnamese\_vie & professional & 665.00 & 11291.00 & 0.06 \\ 
    ##   Warao\_wba & non-fiction & 22.00 & 2183.00 & 0.01 \\ 
    ##   Wichi\_mzh & non-fiction & 92.00 & 3918965.00 & 0.00 \\ 
    ##   Wichita\_wic & conversation & 20.00 & 5552.00 & 0.00 \\ 
    ##   Yagua\_yad & non-fiction & 77.00 & 1117898.00 & 0.00 \\ 
    ##   Yagua\_yad & professional & 64.00 & 9602.00 & 0.01 \\ 
    ##   Yaqui\_yaq & non-fiction & 51.00 & 1386107.00 & 0.00 \\ 
    ##   Yoruba\_yor & non-fiction & 98.00 & 2727263.00 & 0.00 \\ 
    ##   Yoruba\_yor & professional & 73.00 & 9093.00 & 0.01 \\ 
    ##   Zoque\_Copainala\_zoc & non-fiction & 36.00 & 5250.00 & 0.01 \\ 
    ##   Zulu\_zul & professional & 60.00 & 9192.00 & 0.01 \\ 
    ##   \hline
    ## \end{longtable}

# TODOS

-   Plot words and graphemes TTR? These are (bad) preliminary:
    -   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/plot_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/plot_ttr.md</a>
    -   <a href="https://github.com/uzling/100LC/blob/master/Reports/ttr/words_vs_graphemes_ttr.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/ttr/words_vs_graphemes_ttr.md</a>
-   Plot maps (see:
    <a href="https://github.com/uzling/100LC/issues/190" class="uri">https://github.com/uzling/100LC/issues/190</a>)
-   Generate median word length (in characters) (see:
    <a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>)
