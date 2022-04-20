Get the unique mode and genre labels from metadata and file folder
structure
================
Steven Moran
12 December, 2021

# Setup

``` r
library(dplyr)
library(readr)
library(knitr)
```

Load the RData serialized version of the TeDDi database.

``` r
load('../../Database/TeDDi.RData')
```

# Get genre info from the files

Select the `mode`, `genre_narrow`, and `genre_broad` fields from the
file table and get the distinct values per corpus.

``` r
genre_info <- clc_file %>% select(corpus_id, language_name_wals, mode, genre_broad, genre_narrow) %>% distinct()
write_csv(genre_info, 'genres_in_file_metadata_headers.csv')
genre_info %>% kable()
```

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
|          9 | Bagirmi                   | spoken  | grammar      | NA                          |
|         10 | Barasano                  | written | non-fiction  | religion                    |
|         11 | Basque                    | written | non-fiction  | religion                    |
|         11 | Basque                    | written | non-fiction  | prepared\_speeches          |
|         12 | Basque                    | written | professional | official\_documents         |
|         13 | Berber (Middle Atlas)     | written | professional | official\_documents         |
|         14 | Burmese                   | written | non-fiction  | religion                    |
|         15 | Burmese                   | written | professional | official\_documents         |
|         16 | Burushaski                | spoken  | grammar      | NA                          |
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
|         40 | Grebo                     | spoken  | non-fiction  | oral\_tradition             |
|         41 | Greek (Modern)            | written | fiction      | general\_fiction            |
|         42 | Greek (Modern)            | written | non-fiction  | religion                    |
|         42 | Greek (Modern)            | written | non-fiction  | prepared\_speeches          |
|         43 | Greek (Modern)            | written | professional | official\_documents         |
|         44 | Greenlandic (West)        | written | non-fiction  | religion                    |
|         45 | Greenlandic (West)        | written | professional | official\_documents         |
|         46 | Guraní                    | written | non-fiction  | religion                    |
|         47 | Guaraní                   | written | professional | official\_documents         |
|         48 | Hausa                     | written | non-fiction  | religion                    |
|         49 | Hausa                     | written | professional | official\_documents         |
|         50 | Hebrew (Modern)           | written | fiction      | general\_fiction            |
|         51 | Hebrew (Modern)           | written | non-fiction  | prepared\_speeches          |
|         52 | Hebrew (Modern)           | written | professional | official\_documents         |
|         53 | Hindi                     | written | non-fiction  | religion                    |
|         53 | Hindi                     | written | non-fiction  | prepared\_speeches          |
|         54 | Hindi                     | written | professional | official\_documents         |
|         55 | Hixkaryana                | written | non-fiction  | religion                    |
|         56 | Hmong Njua                | written | professional | official\_documents         |
|         57 | Imonda                    | spoken  | non-fiction  | oral\_tradition             |
|         58 | Indonesian                | written | non-fiction  | religion                    |
|         58 | Indonesian                | written | non-fiction  | prepared\_speeches          |
|         59 | Indonesian                | written | professional | official\_documents         |
|         60 | Jakaltek                  | written | non-fiction  | religion                    |
|         61 | Japanese                  | written | fiction      | general\_fiction            |
|         62 | Japanese                  | written | non-fiction  | prepared\_speeches          |
|         63 | Japanese                  | written | professional | official\_documents         |
|         64 | Kannada                   | written | professional | official\_documents         |
|         65 | Kayardild                 | spoken  | grammar      | NA                          |
|         66 | Kewa                      | written | non-fiction  | religion                    |
|         67 | Khalkha                   | written | non-fiction  | religion                    |
|         68 | Khalkha                   | written | professional | official\_documents         |
|         69 | Khoekhoe                  | written | non-fiction  | religion                    |
|         70 | Kiowa                     | spoken  | non-fiction  | oral\_tradition             |
|         71 | Korean                    | written | non-fiction  | religion                    |
|         71 | Korean                    | written | non-fiction  | prepared\_speeches          |
|         72 | Korean                    | written | professional | official\_documents         |
|         73 | Kutenai                   | spoken  | non-fiction  | oral\_tradition             |
|         74 | Lango                     | written | non-fiction  | religion                    |
|         75 | Lavukaleve                | spoken  | non-fiction  | oral\_tradition             |
|         76 | Luvale                    | written | professional | official\_documents         |
|         77 | Makah                     | spoken  | conversation | spontaneous\_speeches       |
|         78 | Makah                     | spoken  | non-fiction  | oral\_tradition             |
|         79 | Malagasy                  | written | non-fiction  | religion                    |
|         80 | Malagasy                  | written | professional | official\_documents         |
|         81 | Mandarin                  | written | fiction      | general\_fiction            |
|         82 | Mandarin                  | written | non-fiction  | prepared\_speeches          |
|         83 | Mandarin                  | written | professional | official\_documents         |
|         84 | Mapudungun                | written | non-fiction  | religion                    |
|         85 | Mapudungun                | written | professional | official\_documents         |
|         86 | Martuthunira              | spoken  | conversation | spontaneous\_speeches       |
|         87 | Maung                     | written | non-fiction  | religion                    |
|         88 | Maybrat                   | written | non-fiction  | written\_tradition          |
|         89 | Mixtec (Chalcatongo)      | written | non-fiction  | religion                    |
|         90 | Ngiyambaa                 | spoken  | conversation | spontaneous\_speeches       |
|         91 | Ngiyambaa                 | spoken  | non-fiction  | oral\_tradition             |
|         92 | Oromo (Harar)             | written | non-fiction  | religion                    |
|         93 | Otomí (Mezquital)         | written | grammar      | NA                          |
|         94 | Otomí (Mezquital)         | written | non-fiction  | written\_tradition          |
|         95 | Otomi (Mezquital)         | written | professional | official\_documents         |
|         96 | Paiwan                    | spoken  | conversation | spontaneous\_speeches       |
|         96 | Paiwan                    | spoken  | conversation | face-to-face\_conversations |
|         97 | Paiwan                    | spoken  | non-fiction  | oral\_tradition             |
|         98 | Persian                   | written | fiction      | general\_fiction            |
|         99 | Persian                   | written | non-fiction  | religion                    |
|         99 | Persian                   | written | non-fiction  | prepared\_speeches          |
|        100 | Persian                   | written | professional | official\_documents         |
|        101 | Pirahã                    | spoken  | conversation | spontaneous\_speeches       |
|        102 | Quechua (Imbabura)        | written | non-fiction  | religion                    |
|        103 | Rama                      | spoken  | grammar      | NA                          |
|        104 | Rama                      | spoken  | non-fiction  | oral\_tradition             |
|        105 | Rapanui                   | spoken  | non-fiction  | oral\_tradition             |
|        106 | Russian                   | written | fiction      | general\_fiction            |
|        107 | Russian                   | written | non-fiction  | religion                    |
|        107 | Russian                   | written | non-fiction  | prepared\_speeches          |
|        108 | Russian                   | written | professional | official\_documents         |
|        109 | Sango                     | written | non-fiction  | religion                    |
|        110 | Sango                     | written | professional | official\_documents         |
|        111 | Sanuma                    | written | non-fiction  | religion                    |
|        112 | Spanish                   | written | fiction      | general\_fiction            |
|        113 | Spanish                   | written | non-fiction  | religion                    |
|        113 | Spanish                   | written | non-fiction  | prepared\_speeches          |
|        114 | Spanish                   | written | professional | official\_documents         |
|        115 | Swahili                   | written | non-fiction  | religion                    |
|        115 | Swahili                   | written | non-fiction  | prepared\_speeches          |
|        116 | Swahili                   | written | professional | official\_documents         |
|        117 | Tagalog                   | written | fiction      | general\_fiction            |
|        118 | Tagalog                   | written | non-fiction  | religion                    |
|        118 | Tagalog                   | written | non-fiction  | prepared\_speeches          |
|        119 | Tagalog                   | written | professional | official\_documents         |
|        120 | Thai                      | written | non-fiction  | religion                    |
|        120 | Thai                      | written | non-fiction  | prepared\_speeches          |
|        121 | Thai                      | written | professional | official\_documents         |
|        122 | Tiwi                      | spoken  | non-fiction  | oral\_tradition             |
|        123 | Turkish                   | written | non-fiction  | religion                    |
|        123 | Turkish                   | written | non-fiction  | prepared\_speeches          |
|        124 | Turkish                   | written | professional | official\_documents         |
|        125 | Vietnamese                | written | non-fiction  | religion                    |
|        125 | Vietnamese                | written | non-fiction  | prepared\_speeches          |
|        126 | Vietnamese                | written | professional | official\_documents         |
|        127 | Warao                     | spoken  | non-fiction  | oral\_tradition             |
|        128 | Wari’                     | spoken  | conversation | spontaneous\_speeches       |
|        129 | Wichí                     | written | non-fiction  | religion                    |
|        130 | Wichita                   | spoken  | conversation | oral\_tradition             |
|        131 | Yagua                     | written | non-fiction  | religion                    |
|        132 | Yagua                     | written | professional | official\_documents         |
|        133 | Yaqui                     | written | non-fiction  | religion                    |
|        134 | Yoruba                    | written | non-fiction  | religion                    |
|        135 | Yoruba                    | written | professional | official\_documents         |
|        136 | Zoque (Copainalá)         | spoken  | non-fiction  | oral\_tradition             |
|        137 | Zulu                      | written | professional | official\_documents         |

What are the distinct values of each?

Mode:

``` r
clc_file %>% select(mode) %>% distinct() %>% kable()
```

| mode    |
|:--------|
| written |
| spoken  |

Genre broad:

``` r
clc_file %>% select(genre_broad) %>% distinct() %>% kable()
```

| genre\_broad |
|:-------------|
| professional |
| non-fiction  |
| conversation |
| grammar      |
| fiction      |

Genre narrow:

``` r
clc_file %>% select(genre_narrow) %>% distinct() %>% kable()
```

| genre\_narrow               |
|:----------------------------|
| official\_documents         |
| oral\_tradition             |
| religion                    |
| spontaneous\_speeches       |
| NA                          |
| prepared\_speeches          |
| face-to-face\_conversations |
| general\_fiction            |
| written\_tradition          |

# Get genre info from the file folder structure

Select the `genre_narrow` and `genre_broad` categories as encoded in the
file folder structure.

``` r
file_folders <- clc_file %>% select(corpus_id, genre_broad, genre_narrow) %>% distinct()
corpus_names <- clc_corpus %>% select(id, name)
file_folders <- left_join(file_folders, corpus_names, by=c("corpus_id"="id"))
file_folders <- file_folders %>% select(name, genre_broad, genre_narrow)

write_csv(file_folders, 'genres_in_file_folders.csv')
kable(file_folders)
```

| name                        | genre\_broad | genre\_narrow               |
|:----------------------------|:-------------|:----------------------------|
| Abkhaz\_abk                 | professional | official\_documents         |
| Acoma\_kjq                  | non-fiction  | oral\_tradition             |
| Alamblak\_amp               | non-fiction  | religion                    |
| Amele\_aey                  | non-fiction  | religion                    |
| Apurina\_apu                | non-fiction  | religion                    |
| Arabic\_Egyptian\_arz       | non-fiction  | religion                    |
| Arapesh\_Mountain\_ape      | non-fiction  | religion                    |
| Asmat\_tml                  | conversation | spontaneous\_speeches       |
| Bagirmi\_bmi                | grammar      | NA                          |
| Barasano\_bsn               | non-fiction  | religion                    |
| Basque\_eus                 | non-fiction  | religion                    |
| Basque\_eus                 | non-fiction  | prepared\_speeches          |
| Basque\_eus                 | professional | official\_documents         |
| Berber\_MiddleAtlas\_tzm    | professional | official\_documents         |
| Burmese\_mya                | non-fiction  | religion                    |
| Burmese\_mya                | professional | official\_documents         |
| Burushaski\_bsk             | grammar      | NA                          |
| CanelaKraho\_ram            | non-fiction  | religion                    |
| Chamorro\_cha               | non-fiction  | religion                    |
| Chamorro\_cha               | professional | official\_documents         |
| Chukchi\_ckt                | non-fiction  | religion                    |
| Daga\_dgz                   | non-fiction  | religion                    |
| Dani\_LowerGrandValley\_dni | conversation | face-to-face\_conversations |
| English\_eng                | fiction      | general\_fiction            |
| English\_eng                | non-fiction  | religion                    |
| English\_eng                | non-fiction  | prepared\_speeches          |
| English\_eng                | professional | official\_documents         |
| Fijian\_fij                 | non-fiction  | religion                    |
| Fijian\_fij                 | professional | official\_documents         |
| Finnish\_fin                | fiction      | general\_fiction            |
| Finnish\_fin                | non-fiction  | religion                    |
| Finnish\_fin                | non-fiction  | prepared\_speeches          |
| Finnish\_fin                | professional | official\_documents         |
| French\_fra                 | fiction      | general\_fiction            |
| French\_fra                 | non-fiction  | religion                    |
| French\_fra                 | non-fiction  | prepared\_speeches          |
| French\_fra                 | professional | official\_documents         |
| Georgian\_kat               | non-fiction  | religion                    |
| Georgian\_kat               | non-fiction  | prepared\_speeches          |
| Georgian\_kat               | professional | official\_documents         |
| German\_deu                 | fiction      | general\_fiction            |
| German\_deu                 | non-fiction  | religion                    |
| German\_deu                 | non-fiction  | prepared\_speeches          |
| German\_deu                 | professional | official\_documents         |
| Gooniyandi\_gni             | conversation | spontaneous\_speeches       |
| Grebo\_gry                  | non-fiction  | oral\_tradition             |
| Greek\_Modern\_ell          | fiction      | general\_fiction            |
| Greek\_Modern\_ell          | non-fiction  | religion                    |
| Greek\_Modern\_ell          | non-fiction  | prepared\_speeches          |
| Greek\_Modern\_ell          | professional | official\_documents         |
| Greenlandic\_West\_kal      | non-fiction  | religion                    |
| Greenlandic\_West\_kal      | professional | official\_documents         |
| Guarani\_gug                | non-fiction  | religion                    |
| Guarani\_gug                | professional | official\_documents         |
| Hausa\_hau                  | non-fiction  | religion                    |
| Hausa\_hau                  | professional | official\_documents         |
| Hebrew\_Modern\_heb         | fiction      | general\_fiction            |
| Hebrew\_Modern\_heb         | non-fiction  | prepared\_speeches          |
| Hebrew\_Modern\_heb         | professional | official\_documents         |
| Hindi\_hin                  | non-fiction  | religion                    |
| Hindi\_hin                  | non-fiction  | prepared\_speeches          |
| Hindi\_hin                  | professional | official\_documents         |
| Hixkaryana\_hix             | non-fiction  | religion                    |
| HmongNjua\_hnj              | professional | official\_documents         |
| Imonda\_imn                 | non-fiction  | oral\_tradition             |
| Indonesian\_ind             | non-fiction  | religion                    |
| Indonesian\_ind             | non-fiction  | prepared\_speeches          |
| Indonesian\_ind             | professional | official\_documents         |
| Jakaltek\_jac               | non-fiction  | religion                    |
| Japanese\_jpn               | fiction      | general\_fiction            |
| Japanese\_jpn               | non-fiction  | prepared\_speeches          |
| Japanese\_jpn               | professional | official\_documents         |
| Kannada\_kan                | professional | official\_documents         |
| Kayardild\_gyd              | grammar      | NA                          |
| Kewa\_kew                   | non-fiction  | religion                    |
| Khalkha\_khk                | non-fiction  | religion                    |
| Khalkha\_khk                | professional | official\_documents         |
| Khoekhoe\_naq               | non-fiction  | religion                    |
| Kiowa\_kio                  | non-fiction  | oral\_tradition             |
| Korean\_kor                 | non-fiction  | religion                    |
| Korean\_kor                 | non-fiction  | prepared\_speeches          |
| Korean\_kor                 | professional | official\_documents         |
| Kutenai\_kut                | non-fiction  | oral\_tradition             |
| Lango\_laj                  | non-fiction  | religion                    |
| Lavukaleve\_lvk             | non-fiction  | oral\_tradition             |
| Luvale\_lue                 | professional | official\_documents         |
| Makah\_myh                  | conversation | spontaneous\_speeches       |
| Makah\_myh                  | non-fiction  | oral\_tradition             |
| Malagasy\_plt               | non-fiction  | religion                    |
| Malagasy\_plt               | professional | official\_documents         |
| Mandarin\_cmn               | fiction      | general\_fiction            |
| Mandarin\_cmn               | non-fiction  | prepared\_speeches          |
| Mandarin\_cmn               | professional | official\_documents         |
| Mapudungun\_arn             | non-fiction  | religion                    |
| Mapudungun\_arn             | professional | official\_documents         |
| Martuthunira\_vma           | conversation | spontaneous\_speeches       |
| Maung\_mph                  | non-fiction  | religion                    |
| Maybrat\_ayz                | non-fiction  | written\_tradition          |
| Mixtec\_Chalcatongo\_mig    | non-fiction  | religion                    |
| Ngiyambaa\_wyb              | conversation | spontaneous\_speeches       |
| Ngiyambaa\_wyb              | non-fiction  | oral\_tradition             |
| Oromo\_Harar\_hae           | non-fiction  | religion                    |
| Otomi\_Mezquital\_ote       | grammar      | NA                          |
| Otomi\_Mezquital\_ote       | non-fiction  | written\_tradition          |
| Otomi\_Mezquital\_ote       | professional | official\_documents         |
| Paiwan\_pwn                 | conversation | spontaneous\_speeches       |
| Paiwan\_pwn                 | conversation | face-to-face\_conversations |
| Paiwan\_pwn                 | non-fiction  | oral\_tradition             |
| Persian\_pes                | fiction      | general\_fiction            |
| Persian\_pes                | non-fiction  | religion                    |
| Persian\_pes                | non-fiction  | prepared\_speeches          |
| Persian\_pes                | professional | official\_documents         |
| Piraha\_myp                 | conversation | spontaneous\_speeches       |
| Quechua\_Imbabura\_qvi      | non-fiction  | religion                    |
| Rama\_rma                   | grammar      | NA                          |
| Rama\_rma                   | non-fiction  | oral\_tradition             |
| Rapanui\_rap                | non-fiction  | oral\_tradition             |
| Russian\_rus                | fiction      | general\_fiction            |
| Russian\_rus                | non-fiction  | religion                    |
| Russian\_rus                | non-fiction  | prepared\_speeches          |
| Russian\_rus                | professional | official\_documents         |
| Sango\_sag                  | non-fiction  | religion                    |
| Sango\_sag                  | professional | official\_documents         |
| Sanuma\_xsu                 | non-fiction  | religion                    |
| Spanish\_spa                | fiction      | general\_fiction            |
| Spanish\_spa                | non-fiction  | religion                    |
| Spanish\_spa                | non-fiction  | prepared\_speeches          |
| Spanish\_spa                | professional | official\_documents         |
| Swahili\_swh                | non-fiction  | religion                    |
| Swahili\_swh                | non-fiction  | prepared\_speeches          |
| Swahili\_swh                | professional | official\_documents         |
| Tagalog\_tgl                | fiction      | general\_fiction            |
| Tagalog\_tgl                | non-fiction  | religion                    |
| Tagalog\_tgl                | non-fiction  | prepared\_speeches          |
| Tagalog\_tgl                | professional | official\_documents         |
| Thai\_tha                   | non-fiction  | religion                    |
| Thai\_tha                   | non-fiction  | prepared\_speeches          |
| Thai\_tha                   | professional | official\_documents         |
| Tiwi\_tiw                   | non-fiction  | oral\_tradition             |
| Turkish\_tur                | non-fiction  | religion                    |
| Turkish\_tur                | non-fiction  | prepared\_speeches          |
| Turkish\_tur                | professional | official\_documents         |
| Vietnamese\_vie             | non-fiction  | religion                    |
| Vietnamese\_vie             | non-fiction  | prepared\_speeches          |
| Vietnamese\_vie             | professional | official\_documents         |
| Warao\_wba                  | non-fiction  | oral\_tradition             |
| Wari\_pav                   | conversation | spontaneous\_speeches       |
| Wichi\_mzh                  | non-fiction  | religion                    |
| Wichita\_wic                | conversation | oral\_tradition             |
| Yagua\_yad                  | non-fiction  | religion                    |
| Yagua\_yad                  | professional | official\_documents         |
| Yaqui\_yaq                  | non-fiction  | religion                    |
| Yoruba\_yor                 | non-fiction  | religion                    |
| Yoruba\_yor                 | professional | official\_documents         |
| Zoque\_Copainala\_zoc       | non-fiction  | oral\_tradition             |
| Zulu\_zul                   | professional | official\_documents         |

Get the unique values.

Genre broad:

``` r
clc_file %>% select(genre_broad) %>% distinct() %>% kable()
```

| genre\_broad |
|:-------------|
| professional |
| non-fiction  |
| conversation |
| grammar      |
| fiction      |

Genre narrow:

``` r
clc_file %>% select(genre_narrow) %>% distinct() %>% kable()
```

| genre\_narrow               |
|:----------------------------|
| official\_documents         |
| oral\_tradition             |
| religion                    |
| spontaneous\_speeches       |
| NA                          |
| prepared\_speeches          |
| face-to-face\_conversations |
| general\_fiction            |
| written\_tradition          |
