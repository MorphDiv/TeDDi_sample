Graphemes exploration
================
Steven Moran
25 May, 2020

This is the 100LC language info index file (planned languages, not actual languages in the corpus).

``` r
index <- read.csv('../../LangInfo/langInfo_100LC.csv')
```

Which languages in 100LC are covered by Epitran, a tool for transliterating orthographic text as IPA:

-   <https://pypi.org/project/epitran/>

Looks like 16 languages (but this depends on the script, which isn't indicated in the 100LC language info index):

``` r
# This table was derived by hand from the project website above
epitran <- read.csv('epitran_data.csv')

table(index$iso639_3 %in% epitran$ISO6393) %>% kable()
```

| Var1  |  Freq|
|:------|-----:|
| FALSE |    84|
| TRUE  |    16|

``` r
index[which(index$iso639_3 %in% epitran$ISO6393),] %>% select(iso639_3, name) %>% arrange(name) %>% kable()
```

| iso639\_3 | name            |
|:----------|:----------------|
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

Which languages have grapheme-to-phoneme coverage in The World Writing System Database (<https://agricolamz.github.io/wwsd/>)? What's the overlap between the two sources? (Note: we'll have to take into account whether the scripts are the same.)

``` r
# wwsd tables
bib <- read.csv('~/Github/wwsd/bibliography.tsv', sep="\t", stringsAsFactors = FALSE)
db <- read.csv('~/Github/wwsd/database.csv', stringsAsFactors = FALSE)

table(index$glottocode %in% bib$glottocode) %>% kable()
```

| Var1  |  Freq|
|:------|-----:|
| FALSE |    80|
| TRUE  |    20|

``` r
index[which(index$glottocode %in% bib$glottocode),] %>% select(iso639_3, name)  %>% arrange(name) %>% kable()
```

| iso639\_3 | name                |
|:----------|:--------------------|
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
