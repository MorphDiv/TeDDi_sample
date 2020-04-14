Compare simple vs advanced tokenization counts
================
Steven Moran
14 April, 2020

``` r
library(dplyr)
library(knitr)
library(testthat)
```

``` r
# Read in reports
simple <- read.csv("progress_simple.csv")
advanced <- read.csv("progress_advanced.csv")
```

``` r
# Rename columns
simple <- simple %>% rename(simple_number_texts = number_texts, simple_number_genres = number_genres, simple_number_characters = number_characters, simple_number_tokens = number_tokens)
advanced <- advanced %>% rename(advanced_number_texts = number_texts, advanced_number_genres = number_genres,  advanced_number_characters = number_characters, advanced_number_tokens = number_tokens)
```

``` r
# Merge
both <- left_join(simple, advanced)
```

    ## Joining, by = "language"

``` r
# We expect that the count for texts, genres, and unique characters are the same across reports
expect_true(all(both$simple_number_texts==both$advanced_number_texts))
expect_true(all(both$simple_number_genres==both$advanced_number_genres))
expect_true(all(both$simple_number_characters==both$advanced_number_characters))
```

``` r
# Get the delta between tokenization routines
both$delta_tokens <- abs(both$simple_number_tokens-both$advanced_number_tokens)
```

``` r
# TODO: Add in the writing system data
# The current counts do not account for different writing systems within the same language folder, e.g.
# https://github.com/uzling/100LC/blob/master/Corpus/Vietnamese_vie/professional/vie_pro_1.txt
# https://github.com/uzling/100LC/blob/master/Corpus/Vietnamese_vie/professional/vie_pro_2.txt
```

``` r
# Display the difference in tokenization routines
kable(both %>% select(language, simple_number_tokens, advanced_number_tokens, delta_tokens))
```

| language                   |  simple\_number\_tokens|  advanced\_number\_tokens|  delta\_tokens|
|:---------------------------|-----------------------:|-------------------------:|--------------:|
| Abkhaz\_abk                |                    2650|                      2860|            210|
| Acoma\_kjq                 |                    2189|                      2220|             31|
| Alamblak\_amp              |                  276878|                    276878|              0|
| Amele\_aey                 |                  282106|                    282106|              0|
| Apurina\_apu               |                  216105|                    216105|              0|
| Arabic\_Egyptian\_arz      |                  559809|                    559809|              0|
| Arapesh\_Mountain\_ape     |                  313569|                    313569|              0|
| Asmat\_tml                 |                     736|                       832|             96|
| Bagirmi\_bmi               |                      67|                        68|              1|
| Barasano\_bsn              |                  301879|                    303425|           1546|
| Basque\_eus                |                 2766143|                   3550800|         784657|
| Berber\_MiddleAtlas\_tzm   |                    3644|                      3830|            186|
| Burmese\_mya               |                  528128|                     40902|         487226|
| Burushaski\_bsk            |                     185|                       185|              0|
| CanelaKraho\_ram           |                   39898|                     40276|            378|
| Chamorro\_cha              |                  233275|                    253436|          20161|
| Chukchi\_ckt               |                   22677|                     22793|            116|
| Cree\_Plains\_crk          |                     612|                       641|             29|
| Daga\_dgz                  |                  252821|                    252843|             22|
| Dani\_LoweGrandValley\_dni |                       0|                         0|              0|
| English\_eng               |                15955891|                  15864985|          90906|
| Fijian\_fij                |                  268515|                    269942|           1427|
| Finnish\_fin               |                15980444|                  15696845|         283599|
| French\_fra                |                15195137|                  15678558|         483421|
| Georgian\_kat              |                  836482|                   1032815|         196333|
| German\_deu                |                16099011|                  15903171|         195840|
| Gooniyandi\_gni            |                     240|                       258|             18|
| Grebo\_gry                 |                       0|                         0|              0|
| Greek\_Modern\_ell         |                16212378|                  15960039|         252339|
| Greenlandic\_West\_kal     |                   88134|                     88297|            163|
| Guarani\_gug               |                  180442|                    204675|          24233|
| Hausa\_hau                 |                  231356|                    233393|           2037|
| Hebrew\_Modern\_heb        |                 5290560|                   6737489|        1446929|
| Hindi\_hin                 |                 2304409|                   2112281|         192128|
| Hixkaryana\_hix            |                   57023|                     57485|            462|
| HmongNjua\_hnj             |                    5602|                      5890|            288|
| Imonda\_imn                |                     354|                       361|              7|
| Indonesian\_ind            |                 5892959|                   5760552|         132407|
| Jakaltek\_jac              |                  265326|                    295408|          30082|
| Japanese\_jpn              |                 1290714|                   5997500|        4706786|
| Kannada\_kan               |                    2160|                      2342|            182|
| Karok\_kyh                 |                     379|                       423|             44|
| Kayardild\_gyd             |                      65|                        85|             20|
| Kewa\_kew                  |                  282373|                    282373|              0|
| Khalkha\_khk               |                  172549|                    172767|            218|
| Khoekhoe\_naq              |                  209442|                    209442|              0|
| Kiowa\_kio                 |                      80|                       179|             99|
| Koasati\_cku               |                       0|                         0|              0|
| Korean\_kor                |                 3436864|                   5948724|        2511860|
| KoyraboroSenni\_ses        |                       0|                         0|              0|
| Krongo\_kgo                |                       0|                         0|              0|
| Kutenai\_kut               |                      32|                        48|             16|
| Lakota\_lkt                |                       0|                         0|              0|
| Lango\_laj                 |                  213964|                    213964|              0|
| Lavukaleve\_lvk            |                    1905|                      1941|             36|
| Lezgian\_lez               |                       0|                         0|              0|
| Luvale\_lue                |                    2432|                      2551|            119|
| Makah\_myh                 |                     393|                       394|              1|
| Malagasy\_plt              |                  817977|                    946291|         128314|
| Mandarin\_cmn              |                 1897794|                  12060320|       10162526|
| Mangarrayi\_mpc            |                       0|                         0|              0|
| Mapudungun\_arn            |                  239259|                    239792|            533|
| Maricopa\_mrc              |                       0|                         0|              0|
| Martuthunira\_vma          |                    7658|                      7874|            216|
| Maung\_mph                 |                   26176|                     26176|              0|
| Maybrat\_ayz               |                     678|                       678|              0|
| Meithei\_mni               |                       0|                         0|              0|
| Mixtec\_Chalcatongo\_mig   |                  223793|                    268161|          44368|
| Ngiyambaa\_wyb             |                      34|                        45|             11|
| Oneida\_one                |                       0|                         0|              0|
| Oromo\_Harar\_hae          |                  205876|                    206966|           1090|
| Otomi\_Mezquital\_ote      |                    3698|                      3952|            254|
| Paiwan\_pwn                |                       0|                         0|              0|
| Persian\_pes               |                 5385056|                   5250801|         134255|
| Piraha\_myp                |                       0|                         0|              0|
| Quechua\_Imbabura\_qvi     |                  198842|                    198842|              0|
| Rama\_rma                  |                     456|                       458|              2|
| Rapanui\_rap               |                    2714|                      2792|             78|
| Russian\_rus               |                 5903177|                   5723100|         180077|
| Sango\_sag                 |                  312472|                    312621|            149|
| Sanuma\_xsu                |                  500527|                    500527|              0|
| Slave\_scs                 |                       0|                         0|              0|
| Spanish\_spa               |                15914725|                  15777791|         136934|
| Supyire\_spp               |                       0|                         0|              0|
| Swahili\_swh               |                  167424|                    168316|            892|
| Tagalog\_tgl               |                 2873591|                   3114081|         240490|
| Thai\_tha                  |                 2381971|                   8739745|        6357774|
| Tiwi\_tiw                  |                       0|                         0|              0|
| TukangBesi\_bhq            |                       0|                         0|              0|
| Turkish\_tur               |                 5712949|                   5528054|         184895|
| Vietnamese\_vie            |                 6003452|                   6858326|         854874|
| Warao\_wba                 |                     395|                       399|              4|
| Wari\_pav                  |                       0|                         0|              0|
| Wichi\_mzh                 |                  884293|                    931061|          46768|
| Wichita\_wic               |                     772|                       773|              1|
| Yagua\_yad                 |                  194137|                    194377|            240|
| Yaqui\_yaq                 |                  306039|                    377078|          71039|
| Yoruba\_yor                |                  942404|                    942610|            206|
| Zoque\_Copainala\_zoc      |                     872|                       894|             22|
| Zulu\_zul                  |                    2150|                      2309|            159|

``` r
# Compared reports as CSV
compared <- both %>% select(language, simple_number_tokens, advanced_number_tokens, delta_tokens)
write.csv(compared, file="compare_reports.csv", row.names = FALSE, quote=FALSE)
```
