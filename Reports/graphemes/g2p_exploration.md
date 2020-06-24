Graphemes exploration
================
Steven Moran
24 June, 2020

# Overview

This report investigates various resources on writing systems and what
the coverage of those resources are on the 100LC language sample.

This is the 100LC language info index file (planned languages, not
actual languages in the corpus).

``` r
index <- read.csv('../../LangInfo/langInfo_100LC.csv')
```

``` r
head(index) %>% kable()
```

| iso639\_3 | glottocode | wals\_code | name\_glotto    | name\_wals | level    | status                | family\_id | top\_level\_family       | genus\_wals         | family\_wals        | macroarea\_glotto | macroarea\_wals | latitude\_glotto | longitude\_glotto | latitude\_wals | longitude\_wals | name          | folder\_language\_name |
| :-------- | :--------- | :--------- | :-------------- | :--------- | :------- | :-------------------- | :--------- | :----------------------- | :------------------ | :------------------ | :---------------- | :-------------- | ---------------: | ----------------: | -------------: | --------------: | :------------ | :--------------------- |
| abk       | abkh1244   | abk        | Abkhazian       | Abkhaz     | language | vulnerable            | abkh1242   | Abkhaz-Adyge             | Northwest Caucasian | Northwest Caucasian | Eurasia           | Eurasia         |         43.05622 |          41.15911 |     43.0833333 |        41.00000 | Abkhaz\_abk   | Abkhaz                 |
| amp       | alam1246   | ala        | Alamblak        | Alamblak   | language | definitely endangered | sepi1257   | Sepik                    | Sepik Hill          | Sepik               | Papunesia         | Papunesia       |        \-4.66307 |         143.31600 |    \-4.6666667 |       143.33333 | Alamblak\_amp | Alamblak               |
| aey       | amel1241   | ame        | Amele           | Amele      | language | vulnerable            | nucl1709   | Nuclear Trans New Guinea | Madang              | Trans-New Guinea    | Papunesia         | Papunesia       |        \-5.29126 |         145.68700 |    \-5.2500000 |       145.58333 | Amele\_aey    | Amele                  |
| apu       | apur1254   | apu        | Apurinã         | Apurinã    | language | definitely endangered | araw1281   | Arawakan                 | Purus               | Arawakan            | South America     | South America   |        \-8.21692 |        \-66.77140 |    \-9.0000000 |      \-67.00000 | Apurina\_apu  | Apurina                |
| bmi       | bagi1246   | bag        | Bagirmi         | Bagirmi    | language | safe                  | cent2225   | Central Sudanic          | Bongo-Bagirmi       | Central Sudanic     | Africa            | Africa          |         11.52392 |          14.76949 |     11.6666667 |        16.00000 | Bagirmi\_bmi  | Bagirmi                |
| bsn       | bara1380   | brs        | Barasana-Eduria | Barasano   | language | definitely endangered | tuca1253   | Tucanoan                 | Tucanoan            | Tucanoan            | South America     | South America   |          0.02193 |        \-70.80800 |    \-0.1666667 |      \-70.66667 | Barasano\_bsn | Barasano               |

# Coverage

Which languages in 100LC are covered by Epitran, a tool for
transliterating orthographic text as IPA:

  - <https://pypi.org/project/epitran/>

Looks like 16 languages (but this depends on the script, which isn’t
indicated in the 100LC language info index):

``` r
# This table was derived by hand from the project website above
epitran <- read.csv('epitran_data.csv')
```

``` r
table(index$iso639_3 %in% epitran$ISO6393) %>% kable()
```

| Var1  | Freq |
| :---- | ---: |
| FALSE |   84 |
| TRUE  |   16 |

``` r
epitran.lgs <- index[which(index$iso639_3 %in% epitran$ISO6393),] %>% select(iso639_3, name) %>% arrange(name)
epitran.lgs %>% kable()
```

| iso639\_3 | name            |
| :-------- | :-------------- |
| mya       | Burmese\_mya    |
| eng       | English\_eng    |
| fra       | French\_fra     |
| deu       | German\_deu     |
| hau       | Hausa\_hau      |
| hin       | Hindi\_hin      |
| ind       | Indonesian\_ind |
| cmn       | Mandarin\_cmn   |
| rus       | Russian\_rus    |
| spa       | Spanish\_spa    |
| tgl       | Tagalog\_tgl    |
| tha       | Thai\_tha       |
| tur       | Turkish\_tur    |
| vie       | Vietnamese\_vie |
| yor       | Yoruba\_yor     |
| zul       | Zulu\_zul       |

Which languages have grapheme-to-phoneme coverage in The World Writing
System Database (<https://agricolamz.github.io/wwsd/>)? What’s the
overlap between the two sources? (Note: we’ll have to take into account
whether the scripts are the same.)

``` r
# wwsd tables (TODO: update these URLs to point to the online resource once my PRs are merged)
bib <- read.csv('~/Github/wwsd/bibliography.tsv', sep="\t", stringsAsFactors = FALSE)
db <- read.csv('~/Github/wwsd/database.csv', stringsAsFactors = FALSE)

table(index$glottocode %in% bib$glottocode) %>% kable()
```

| Var1  | Freq |
| :---- | ---: |
| FALSE |   80 |
| TRUE  |   20 |

``` r
wwsd.lgs <- index[which(index$glottocode %in% bib$glottocode),] %>% select(iso639_3, name)  %>% arrange(name)
wwsd.lgs %>% kable()
```

| iso639\_3 | name                |
| :-------- | :------------------ |
| abk       | Abkhaz\_abk         |
| eng       | English\_eng        |
| fij       | Fijian\_fij         |
| fin       | Finnish\_fin        |
| fra       | French\_fra         |
| kat       | Georgian\_kat       |
| deu       | German\_deu         |
| heb       | Hebrew\_Modern\_heb |
| hin       | Hindi\_hin          |
| jpn       | Japanese\_jpn       |
| kan       | Kannada\_kan        |
| kor       | Korean\_kor         |
| rap       | Rapanui\_rap        |
| rus       | Russian\_rus        |
| spa       | Spanish\_spa        |
| swh       | Swahili\_swh        |
| tur       | Turkish\_tur        |
| vie       | Vietnamese\_vie     |
| yor       | Yoruba\_yor         |
| zul       | Zulu\_zul           |

``` r
message('There are ', nrow(full_join(epitran.lgs, wwsd.lgs)), ' languages in both epitran and wwsd.')
```

    ## Joining, by = c("iso639_3", "name")

    ## There are 26 languages in both epitran and wwsd.

``` r
full_join(epitran.lgs, wwsd.lgs) %>% arrange(name) %>% kable()
```

    ## Joining, by = c("iso639_3", "name")

| iso639\_3 | name                |
| :-------- | :------------------ |
| abk       | Abkhaz\_abk         |
| mya       | Burmese\_mya        |
| eng       | English\_eng        |
| fij       | Fijian\_fij         |
| fin       | Finnish\_fin        |
| fra       | French\_fra         |
| kat       | Georgian\_kat       |
| deu       | German\_deu         |
| hau       | Hausa\_hau          |
| heb       | Hebrew\_Modern\_heb |
| hin       | Hindi\_hin          |
| ind       | Indonesian\_ind     |
| jpn       | Japanese\_jpn       |
| kan       | Kannada\_kan        |
| kor       | Korean\_kor         |
| cmn       | Mandarin\_cmn       |
| rap       | Rapanui\_rap        |
| rus       | Russian\_rus        |
| spa       | Spanish\_spa        |
| swh       | Swahili\_swh        |
| tgl       | Tagalog\_tgl        |
| tha       | Thai\_tha           |
| tur       | Turkish\_tur        |
| vie       | Vietnamese\_vie     |
| yor       | Yoruba\_yor         |
| zul       | Zulu\_zul           |

``` r
message('There are ', nrow(inner_join(epitran.lgs, wwsd.lgs)), ' languages in both epitran and wwsd.')
```

    ## Joining, by = c("iso639_3", "name")

    ## There are 10 languages in both epitran and wwsd.

``` r
inner_join(epitran.lgs, wwsd.lgs) %>% arrange(name) %>% kable()
```

    ## Joining, by = c("iso639_3", "name")

| iso639\_3 | name            |
| :-------- | :-------------- |
| eng       | English\_eng    |
| fra       | French\_fra     |
| deu       | German\_deu     |
| hin       | Hindi\_hin      |
| rus       | Russian\_rus    |
| spa       | Spanish\_spa    |
| tur       | Turkish\_tur    |
| vie       | Vietnamese\_vie |
| yor       | Yoruba\_yor     |
| zul       | Zulu\_zul       |
