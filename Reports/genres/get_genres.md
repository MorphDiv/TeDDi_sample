Get the unique mode and genre labels from metadata and file folder
structure
================
Steven Moran
30 July, 2020

Setup
=====

    library(dplyr)

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

    library(readr)
    library(knitr)

Load the RData serialized version of the 100LC database.

    load('../../Database/100LC.RData')

Get genre info from the files
=============================

Select the `mode`, `genre_narrow`, and `genre_broad` fields from the
file table and get the distinct values per corpus.

    genre_info <- clc_file %>% select(corpus_id, language_name_wals, mode, genre_broad, genre_narrow) %>% distinct()
    write_csv(genre_info, 'genres_in_file_metadata_headers.csv')
    genre_info %>% kable()

| corpus\_id | language\_name\_wals      | mode    | genre\_broad | genre\_narrow               |
|-----------:|:--------------------------|:--------|:-------------|:----------------------------|
|          1 | Abkhaz                    | written | professional | official\_documents         |
|          2 | Acoma                     | spoken  | non-fiction  | oral\_tradition             |
|          3 | Alamblak                  | written | non-fiction  | religion                    |
|          4 | Amele                     | written | non-fiction  | religion                    |
|          5 | Apurinã                   | written | non-fiction  | religion                    |
|          6 | Arabic (Egyptian)         | written | non-fiction  | religion                    |
|          7 | Arapesh (Mountain)        | written | non-fiction  | religion                    |
|          8 | Asmat                     | spoken  | conversation | spontaneous\_speeches       |
|          9 | Bagirmi                   | spoken  | grammar      | spoken                      |
|         10 | Barasano                  | written | non-fiction  | religion                    |
|         11 | Basque                    | written | non-fiction  | religion                    |
|         11 | Basque                    | written | non-fiction  | prepared\_speeches          |
|         12 | Basque                    | written | professional | official\_documents         |
|         13 | Berber (Middle Atlas)     | written | professional | official\_documents         |
|         14 | Burmese                   | written | non-fiction  | religion                    |
|         15 | Burmese                   | written | professional | official\_documents         |
|         16 | Burushaski                | spoken  | grammar      | spoken                      |
|         17 | Canela-Krahô              | written | non-fiction  | religion                    |
|         18 | Chamorro                  | written | non-fiction  | religion                    |
|         19 | Chamorro                  | written | professional | official\_documents         |
|         20 | Chukchi                   | written | non-fiction  | religion                    |
|         21 | Daga                      | written | non-fiction  | religion                    |
|         22 | Dani (Lower Grand Valley) | spoken  | conversation | face-to-face\_conversations |
|         23 | English                   | written | fiction      | general\_fiction            |
|         24 | English                   | written | non-fiction  | religion                    |
|         24 | English                   | written | non-fiction  | prepared\_speeches          |
|         25 | English                   | written | professional | official\_documents         |
|         26 | Fijian                    | written | non-fiction  | religion                    |
|         27 | Fijian                    | written | professional | official\_documents         |
|         28 | Finnish                   | written | fiction      | general\_fiction            |
|         29 | Finnish                   | written | non-fiction  | religion                    |
|         29 | Finnish                   | written | non-fiction  | prepared\_speeches          |
|         30 | Finnish                   | written | professional | official\_documents         |
|         31 | French                    | written | fiction      | general\_fiction            |
|         32 | French                    | written | non-fiction  | religion                    |
|         32 | French                    | written | non-fiction  | prepared\_speeches          |
|         33 | French                    | written | professional | official\_documents         |
|         34 | Georgian                  | written | non-fiction  | religion                    |
|         34 | Georgian                  | written | non-fiction  | prepared\_speeches          |
|         35 | Georgian                  | written | professional | official\_documents         |
|         36 | German                    | written | fiction      | general\_fiction            |
|         37 | German                    | written | non-fiction  | religion                    |
|         37 | German                    | written | non-fiction  | prepared\_speeches          |
|         38 | German                    | written | professional | official\_documents         |
|         39 | Gooniyandi                | spoken  | conversation | spontaneous\_speeches       |
|         40 | Greek (Modern)            | written | fiction      | general\_fiction            |
|         41 | Greek (Modern)            | written | non-fiction  | religion                    |
|         41 | Greek (Modern)            | written | non-fiction  | prepared\_speeches          |
|         42 | Greek (Modern)            | written | professional | official\_documents         |
|         43 | Greenlandic (West)        | written | non-fiction  | religion                    |
|         44 | Greenlandic (West)        | written | professional | official\_documents         |
|         45 | Guraní                    | written | non-fiction  | religion                    |
|         46 | Guaraní                   | written | professional | official\_documents         |
|         47 | Hausa                     | written | non-fiction  | religion                    |
|         48 | Hausa                     | written | professional | official\_documents         |
|         49 | Hebrew (Modern)           | written | fiction      | general\_fiction            |
|         50 | Hebrew (Modern)           | written | non-fiction  | prepared\_speeches          |
|         51 | Hebrew (Modern)           | written | professional | official\_documents         |
|         52 | Hindi                     | written | non-fiction  | religion                    |
|         52 | Hindi                     | written | non-fiction  | prepared\_speeches          |
|         53 | Hindi                     | written | professional | official\_documents         |
|         54 | Hixkaryana                | written | non-fiction  | religion                    |
|         55 | Hmong Njua                | written | professional | official\_documents         |
|         56 | Imonda                    | spoken  | non-fiction  | oral\_tradition             |
|         57 | Indonesian                | written | non-fiction  | religion                    |
|         57 | Indonesian                | written | non-fiction  | prepared\_speeches          |
|         58 | Indonesian                | written | professional | official\_documents         |
|         59 | Jakaltek                  | written | non-fiction  | religion                    |
|         60 | Japanese                  | written | fiction      | general\_fiction            |
|         61 | Japanese                  | written | non-fiction  | prepared\_speeches          |
|         62 | Japanese                  | written | professional | official\_documents         |
|         63 | Kannada                   | written | professional | official\_documents         |
|         64 | Kayardild                 | spoken  | grammar      | spoken                      |
|         65 | Kewa                      | written | non-fiction  | religion                    |
|         66 | Khalkha                   | written | non-fiction  | religion                    |
|         67 | Khalkha                   | written | professional | official\_documents         |
|         68 | Khoekhoe                  | written | non-fiction  | religion                    |
|         69 | Kiowa                     | spoken  | non-fiction  | oral\_tradition             |
|         70 | Korean                    | written | non-fiction  | religion                    |
|         70 | Korean                    | written | non-fiction  | prepared\_speeches          |
|         71 | Korean                    | written | professional | official\_documents         |
|         72 | Kutenai                   | spoken  | non-fiction  | oral\_tradition             |
|         73 | Lango                     | written | non-fiction  | religion                    |
|         74 | Lavukaleve                | spoken  | non-fiction  | oral\_tradition             |
|         75 | Luvale                    | written | professional | official\_documents         |
|         76 | Makah                     | spoken  | conversation | spontaneous\_speeches       |
|         77 | Makah                     | spoken  | non-fiction  | oral\_tradition             |
|         78 | Malagasy                  | written | non-fiction  | religion                    |
|         79 | Malagasy                  | written | professional | official\_documents         |
|         80 | Mandarin                  | written | fiction      | general\_fiction            |
|         81 | Mandarin                  | written | non-fiction  | prepared\_speeches          |
|         82 | Mandarin                  | written | professional | official\_documents         |
|         83 | Mapudungun                | written | non-fiction  | religion                    |
|         84 | Mapudungun                | written | professional | official\_documents         |
|         85 | Martuthunira              | spoken  | conversation | spontaneous\_speeches       |
|         86 | Maung                     | written | non-fiction  | religion                    |
|         87 | Maybrat                   | written | non-fiction  | written\_traditions         |
|         88 | Mixtec (Chalcatongo)      | written | non-fiction  | religion                    |
|         89 | Ngiyambaa                 | spoken  | conversation | spontaneous\_speeches       |
|         90 | Oromo (Harar)             | written | non-fiction  | religion                    |
|         91 | Otomí (Mezquital)         | written | grammar      | NA                          |
|         92 | Otomí (Mezquital)         | written | non-fiction  | writtten tradition          |
|         92 | Otomí (Mezquital)         | written | non-fiction  | written tradition           |
|         93 | Otomi (Mezquital)         | written | professional | official\_documents         |
|         94 | Persian                   | written | fiction      | general\_fiction            |
|         95 | Persian                   | written | non-fiction  | religion                    |
|         95 | Persian                   | written | non-fiction  | prepared\_speeches          |
|         96 | Persian                   | written | professional | official\_documents         |
|         97 | Quechua (Imbabura)        | written | non-fiction  | religion                    |
|         98 | Rama                      | spoken  | grammar      | spoken                      |
|         99 | Rama                      | spoken  | non-fiction  | oral\_tradition             |
|        100 | Rapanui                   | spoken  | non-fiction  | oral\_tradition             |
|        101 | Russian                   | written | fiction      | general\_fiction            |
|        102 | Russian                   | written | non-fiction  | religion                    |
|        102 | Russian                   | written | non-fiction  | prepared\_speeches          |
|        103 | Russian                   | written | professional | official\_documents         |
|        104 | Sango                     | written | non-fiction  | religion                    |
|        105 | Sango                     | written | professional | official\_documents         |
|        106 | Sanuma                    | written | non-fiction  | religion                    |
|        107 | Spanish                   | written | fiction      | general\_fiction            |
|        108 | Spanish                   | written | non-fiction  | religion                    |
|        108 | Spanish                   | written | non-fiction  | prepared\_speeches          |
|        109 | Spanish                   | written | professional | official\_documents         |
|        110 | Swahili                   | written | non-fiction  | religion                    |
|        110 | Swahili                   | written | non-fiction  | prepared\_speeches          |
|        111 | Swahili                   | written | professional | official\_documents         |
|        112 | Tagalog                   | written | fiction      | general\_fiction            |
|        113 | Tagalog                   | written | non-fiction  | religion                    |
|        113 | Tagalog                   | written | non-fiction  | prepared\_speeches          |
|        114 | Tagalog                   | written | professional | official\_documents         |
|        115 | Thai                      | written | non-fiction  | religion                    |
|        115 | Thai                      | written | non-fiction  | prepared\_speeches          |
|        116 | Thai                      | written | professional | official\_documents         |
|        117 | Turkish                   | written | non-fiction  | religion                    |
|        117 | Turkish                   | written | non-fiction  | prepared\_speeches          |
|        118 | Turkish                   | written | professional | official\_documents         |
|        119 | Vietnamese                | written | non-fiction  | religion                    |
|        119 | Vietnamese                | written | non-fiction  | prepared\_speeches          |
|        120 | Vietnamese                | written | professional | official\_documents         |
|        121 | Warao                     | spoken  | non-fiction  | oral\_tradition             |
|        122 | Wichí                     | written | non-fiction  | religion                    |
|        123 | Wichita                   | spoken  | conversation | oral\_tradition             |
|        124 | Yagua                     | written | non-fiction  | religion                    |
|        125 | Yagua                     | written | professional | official\_documents         |
|        126 | Yaqui                     | written | non-fiction  | religion                    |
|        127 | Yoruba                    | written | non-fiction  | religion                    |
|        128 | Yoruba                    | written | professional | official\_documents         |
|        129 | Zoque (Copainalá)         | spoken  | non-fiction  | oral\_tradition             |
|        130 | Zulu                      | written | professional | official\_documents         |

What are the distinct values of each?

Mode:

    clc_file %>% select(mode) %>% distinct() %>% kable()

| mode    |
|:--------|
| written |
| spoken  |

Genre broad:

    clc_file %>% select(genre_broad) %>% distinct() %>% kable()

| genre\_broad |
|:-------------|
| professional |
| non-fiction  |
| conversation |
| grammar      |
| fiction      |

Genre narrow:

    clc_file %>% select(genre_narrow) %>% distinct() %>% kable()

| genre\_narrow               |
|:----------------------------|
| official\_documents         |
| oral\_tradition             |
| religion                    |
| spontaneous\_speeches       |
| spoken                      |
| prepared\_speeches          |
| face-to-face\_conversations |
| general\_fiction            |
| written\_traditions         |
| NA                          |
| writtten tradition          |
| written tradition           |

Opps, looks like we still have some typos in the text! So I made an
issue:

-   <a href="https://github.com/uzling/100LC/issues/165" class="uri">https://github.com/uzling/100LC/issues/165</a>

Get genre info from the file folder structure
=============================================

Select the `genre_narrow` and `genre_broad` categories as encoded in the
file folder structure.

    file_folders <- clc_corpus %>% select(name, genre_broad, genre_narrow) %>% distinct()
    write_csv(file_folders, 'genres_in_file_folders.csv')
    kable(file_folders)

| name                        | genre\_broad | genre\_narrow |
|:----------------------------|:-------------|:--------------|
| Abkhaz\_abk                 | professional | NA            |
| Acoma\_kjq                  | non-fiction  | spoken        |
| Alamblak\_amp               | non-fiction  | written       |
| Amele\_aey                  | non-fiction  | written       |
| Apurina\_apu                | non-fiction  | written       |
| Arabic\_Egyptian\_arz       | non-fiction  | written       |
| Arapesh\_Mountain\_ape      | non-fiction  | written       |
| Asmat\_tml                  | conversation | NA            |
| Bagirmi\_bmi                | grammar      | spoken        |
| Barasano\_bsn               | non-fiction  | written       |
| Basque\_eus                 | non-fiction  | written       |
| Basque\_eus                 | professional | NA            |
| Berber\_MiddleAtlas\_tzm    | professional | NA            |
| Burmese\_mya                | non-fiction  | written       |
| Burmese\_mya                | professional | NA            |
| Burushaski\_bsk             | grammar      | spoken        |
| CanelaKraho\_ram            | non-fiction  | written       |
| Chamorro\_cha               | non-fiction  | written       |
| Chamorro\_cha               | professional | NA            |
| Chukchi\_ckt                | non-fiction  | written       |
| Daga\_dgz                   | non-fiction  | written       |
| Dani\_LowerGrandValley\_dni | conversation | NA            |
| English\_eng                | fiction      | NA            |
| English\_eng                | non-fiction  | written       |
| English\_eng                | professional | NA            |
| Fijian\_fij                 | non-fiction  | written       |
| Fijian\_fij                 | professional | NA            |
| Finnish\_fin                | fiction      | NA            |
| Finnish\_fin                | non-fiction  | written       |
| Finnish\_fin                | professional | NA            |
| French\_fra                 | fiction      | NA            |
| French\_fra                 | non-fiction  | written       |
| French\_fra                 | professional | NA            |
| Georgian\_kat               | non-fiction  | written       |
| Georgian\_kat               | professional | NA            |
| German\_deu                 | fiction      | NA            |
| German\_deu                 | non-fiction  | written       |
| German\_deu                 | professional | NA            |
| Gooniyandi\_gni             | conversation | NA            |
| Greek\_Modern\_ell          | fiction      | NA            |
| Greek\_Modern\_ell          | non-fiction  | written       |
| Greek\_Modern\_ell          | professional | NA            |
| Greenlandic\_West\_kal      | non-fiction  | written       |
| Greenlandic\_West\_kal      | professional | NA            |
| Guarani\_gug                | non-fiction  | written       |
| Guarani\_gug                | professional | NA            |
| Hausa\_hau                  | non-fiction  | written       |
| Hausa\_hau                  | professional | NA            |
| Hebrew\_Modern\_heb         | fiction      | NA            |
| Hebrew\_Modern\_heb         | non-fiction  | written       |
| Hebrew\_Modern\_heb         | professional | NA            |
| Hindi\_hin                  | non-fiction  | written       |
| Hindi\_hin                  | professional | NA            |
| Hixkaryana\_hix             | non-fiction  | written       |
| HmongNjua\_hnj              | professional | NA            |
| Imonda\_imn                 | non-fiction  | spoken        |
| Indonesian\_ind             | non-fiction  | written       |
| Indonesian\_ind             | professional | NA            |
| Jakaltek\_jac               | non-fiction  | written       |
| Japanese\_jpn               | fiction      | NA            |
| Japanese\_jpn               | non-fiction  | written       |
| Japanese\_jpn               | professional | NA            |
| Kannada\_kan                | professional | NA            |
| Kayardild\_gyd              | grammar      | spoken        |
| Kewa\_kew                   | non-fiction  | written       |
| Khalkha\_khk                | non-fiction  | written       |
| Khalkha\_khk                | professional | NA            |
| Khoekhoe\_naq               | non-fiction  | written       |
| Kiowa\_kio                  | non-fiction  | spoken        |
| Korean\_kor                 | non-fiction  | written       |
| Korean\_kor                 | professional | NA            |
| Kutenai\_kut                | non-fiction  | spoken        |
| Lango\_laj                  | non-fiction  | written       |
| Lavukaleve\_lvk             | non-fiction  | spoken        |
| Luvale\_lue                 | professional | NA            |
| Makah\_myh                  | conversation | NA            |
| Makah\_myh                  | non-fiction  | spoken        |
| Malagasy\_plt               | non-fiction  | written       |
| Malagasy\_plt               | professional | NA            |
| Mandarin\_cmn               | fiction      | NA            |
| Mandarin\_cmn               | non-fiction  | written       |
| Mandarin\_cmn               | professional | NA            |
| Mapudungun\_arn             | non-fiction  | written       |
| Mapudungun\_arn             | professional | NA            |
| Martuthunira\_vma           | conversation | NA            |
| Maung\_mph                  | non-fiction  | written       |
| Maybrat\_ayz                | non-fiction  | written       |
| Mixtec\_Chalcatongo\_mig    | non-fiction  | written       |
| Ngiyambaa\_wyb              | conversation | NA            |
| Oromo\_Harar\_hae           | non-fiction  | written       |
| Otomi\_Mezquital\_ote       | grammar      | written       |
| Otomi\_Mezquital\_ote       | non-fiction  | written       |
| Otomi\_Mezquital\_ote       | professional | NA            |
| Persian\_pes                | fiction      | NA            |
| Persian\_pes                | non-fiction  | written       |
| Persian\_pes                | professional | NA            |
| Quechua\_Imbabura\_qvi      | non-fiction  | written       |
| Rama\_rma                   | grammar      | spoken        |
| Rama\_rma                   | non-fiction  | spoken        |
| Rapanui\_rap                | non-fiction  | spoken        |
| Russian\_rus                | fiction      | NA            |
| Russian\_rus                | non-fiction  | written       |
| Russian\_rus                | professional | NA            |
| Sango\_sag                  | non-fiction  | written       |
| Sango\_sag                  | professional | NA            |
| Sanuma\_xsu                 | non-fiction  | written       |
| Spanish\_spa                | fiction      | NA            |
| Spanish\_spa                | non-fiction  | written       |
| Spanish\_spa                | professional | NA            |
| Swahili\_swh                | non-fiction  | written       |
| Swahili\_swh                | professional | NA            |
| Tagalog\_tgl                | fiction      | NA            |
| Tagalog\_tgl                | non-fiction  | written       |
| Tagalog\_tgl                | professional | NA            |
| Thai\_tha                   | non-fiction  | written       |
| Thai\_tha                   | professional | NA            |
| Turkish\_tur                | non-fiction  | written       |
| Turkish\_tur                | professional | NA            |
| Vietnamese\_vie             | non-fiction  | written       |
| Vietnamese\_vie             | professional | NA            |
| Warao\_wba                  | non-fiction  | spoken        |
| Wichi\_mzh                  | non-fiction  | written       |
| Wichita\_wic                | conversation | NA            |
| Yagua\_yad                  | non-fiction  | written       |
| Yagua\_yad                  | professional | NA            |
| Yaqui\_yaq                  | non-fiction  | written       |
| Yoruba\_yor                 | non-fiction  | written       |
| Yoruba\_yor                 | professional | NA            |
| Zoque\_Copainala\_zoc       | non-fiction  | spoken        |
| Zulu\_zul                   | professional | NA            |

Get the unique values.

Genre broad:

    clc_corpus %>% select(genre_broad) %>% distinct() %>% kable()

| genre\_broad |
|:-------------|
| professional |
| non-fiction  |
| conversation |
| grammar      |
| fiction      |

Genre narrow:

    clc_corpus %>% select(genre_narrow) %>% distinct() %>% kable()

| genre\_narrow |
|:--------------|
| NA            |
| spoken        |
| written       |
