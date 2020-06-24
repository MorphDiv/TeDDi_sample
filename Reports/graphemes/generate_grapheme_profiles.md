Generate initial orthography profiles
================
Steven Moran
24 June, 2020

# Overview

In its simpliest form, an orthography profile (Moran & Cysouw, 2018) is
a Unicode character or Unicode grapheme unigram model, i.e. a CSV file
where each row represents a character or grapheme in a writing system
with additional information such as its frequency of occurrence in a
text. This report generates orthography profiles from each corpus in the
100LC database.

I use the 100LC test data set for corpora for illustration purposes. The
output for each corpus is written to the `orthography_profiles` folder
in this directory.

``` r
load('../../Database/test-100LC.Rdata')
```

There are multiple languages in the data frame – each row is a word
(with a bunch of other metadata that’s simply repeated). For example:

``` r
head(df) %>% kable()
```

| word\_id | line\_id | file\_id | corpus\_id | language\_id | word\_text      | line\_text                                                                                                                                                                | writing\_system | file\_genre\_broad | file\_genre\_narrow | genre\_broad | genre\_narrow | name        |
| -------: | -------: | -------: | ---------: | -----------: | :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------- | :----------------- | :------------------ | :----------- | :------------ | :---------- |
|        1 |        1 |        1 |          1 |            1 | Ауаҩытәыҩса     | Ауаҩытәыҩса изинқәа Зегьеицырзеиҧшу Адекларациа                                                                                                                           | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |
|        2 |        1 |        1 |          1 |            1 | изинқәа         | Ауаҩытәыҩса изинқәа Зегьеицырзеиҧшу Адекларациа                                                                                                                           | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |
|        3 |        1 |        1 |          1 |            1 | Зегьеицырзеиҧшу | Ауаҩытәыҩса изинқәа Зегьеицырзеиҧшу Адекларациа                                                                                                                           | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |
|        4 |        1 |        1 |          1 |            1 | Адекларациа     | Ауаҩытәыҩса изинқәа Зегьеицырзеиҧшу Адекларациа                                                                                                                           | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |
|        5 |        2 |        1 |          1 |            1 | Алагалажәа      | Алагалажәа                                                                                                                                                                | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |
|        6 |        3 |        1 |          1 |            1 | Дызусҭзаалак,   | Дызусҭзаалак, ауаатәыҩсатә ҭаацәара иалахәу иҳаҭыри, иара иузиҟәымҭхо имоу изинқәеи, ахақәиҭреи, аиашареи, адунеижәларбжьаратәи аҭынчреи шьаҭас ишрымоу хшыҩзышьҭра азуа, | Cyrl            | professional       | official\_documents | professional | NA            | Abkhaz\_abk |

Here are the frequency counts (word counts) per corpus.

``` r
table(df$name) %>% kable()
```

| Var1                        |   Freq |
| :-------------------------- | -----: |
| Abkhaz\_abk                 |   1325 |
| Acoma\_kjq                  |   2433 |
| Alamblak\_amp               | 268933 |
| Arabic\_Egyptian\_arz       | 528641 |
| Asmat\_tml                  |     53 |
| Bagirmi\_bmi                |     70 |
| Basque\_eus                 |   8832 |
| CanelaKraho\_ram            |  40181 |
| Dani\_LowerGrandValley\_dni |    298 |
| English\_eng                | 842657 |
| Finnish\_fin                |  39088 |
| Kayardild\_gyd              |     28 |
| Lavukaleve\_lvk             |   2109 |
| Vietnamese\_vie             |   4545 |

Here’s how we generate an initial orthography profile (a linguistically
correct orthography profile usually requires expert analysis of elements
such as bigraphs; see Moran & Cysouw, 2018 for detailed discussion).

``` r
Abkhaz_abk <- df %>% filter(name == "Abkhaz_abk")
op <- write.profile(Abkhaz_abk$word_text)
op$Frequency <- as.integer(op$Frequency)
op %>% arrange(desc(Frequency)) %>% kable()
```

| Grapheme | Frequency | Codepoint | UnicodeName                                        |
| :------- | --------: | :-------- | :------------------------------------------------- |
| а        |      2463 | U+0430    | CYRILLIC SMALL LETTER A                            |
| и        |       791 | U+0438    | CYRILLIC SMALL LETTER I                            |
| р        |       746 | U+0440    | CYRILLIC SMALL LETTER ER                           |
| ы        |       531 | U+044B    | CYRILLIC SMALL LETTER YERU                         |
| ә        |       487 | U+04D9    | CYRILLIC SMALL LETTER SCHWA                        |
| у        |       368 | U+0443    | CYRILLIC SMALL LETTER U                            |
| з        |       349 | U+0437    | CYRILLIC SMALL LETTER ZE                           |
| л        |       315 | U+043B    | CYRILLIC SMALL LETTER EL                           |
| н        |       315 | U+043D    | CYRILLIC SMALL LETTER EN                           |
| х        |       291 | U+0445    | CYRILLIC SMALL LETTER HA                           |
| е        |       270 | U+0435    | CYRILLIC SMALL LETTER IE                           |
| м        |       227 | U+043C    | CYRILLIC SMALL LETTER EM                           |
| ҭ        |       202 | U+04AD    | CYRILLIC SMALL LETTER TE WITH DESCENDER            |
| ь        |       199 | U+044C    | CYRILLIC SMALL LETTER SOFT SIGN                    |
| о        |       172 | U+043E    | CYRILLIC SMALL LETTER O                            |
| к        |       166 | U+043A    | CYRILLIC SMALL LETTER KA                           |
| г        |       162 | U+0433    | CYRILLIC SMALL LETTER GHE                          |
| ш        |       158 | U+0448    | CYRILLIC SMALL LETTER SHA                          |
| қ        |       151 | U+049B    | CYRILLIC SMALL LETTER KA WITH DESCENDER            |
| ,        |       142 | U+002C    | COMMA                                              |
| д        |       133 | U+0434    | CYRILLIC SMALL LETTER DE                           |
| б        |       118 | U+0431    | CYRILLIC SMALL LETTER BE                           |
| с        |       118 | U+0441    | CYRILLIC SMALL LETTER ES                           |
| т        |       115 | U+0442    | CYRILLIC SMALL LETTER TE                           |
| ҧ        |       102 | U+04A7    | CYRILLIC SMALL LETTER PE WITH MIDDLE HOOK          |
| ҩ        |        90 | U+04A9    | CYRILLIC SMALL LETTER ABKHASIAN HA                 |
| п        |        84 | U+043F    | CYRILLIC SMALL LETTER PE                           |
| ц        |        82 | U+0446    | CYRILLIC SMALL LETTER TSE                          |
| ҵ        |        73 | U+04B5    | CYRILLIC SMALL LIGATURE TE TSE                     |
| .        |        66 | U+002E    | FULL STOP                                          |
| А        |        66 | U+0410    | CYRILLIC CAPITAL LETTER A                          |
| ҟ        |        66 | U+049F    | CYRILLIC SMALL LETTER KA WITH STROKE               |
| ҳ        |        56 | U+04B3    | CYRILLIC SMALL LETTER HA WITH DESCENDER            |
| ӡ        |        44 | U+04E1    | CYRILLIC SMALL LETTER ABKHASIAN DZE                |
| ҷ        |        40 | U+04B7    | CYRILLIC SMALL LETTER CHE WITH DESCENDER           |
| Д        |        39 | U+0414    | CYRILLIC CAPITAL LETTER DE                         |
| ж        |        35 | U+0436    | CYRILLIC SMALL LETTER ZHE                          |
| ҿ        |        28 | U+04BF    | CYRILLIC SMALL LETTER ABKHASIAN CHE WITH DESCENDER |
| ч        |        19 | U+0447    | CYRILLIC SMALL LETTER CHE                          |
| ҕ        |        14 | U+0495    | CYRILLIC SMALL LETTER GHE WITH MIDDLE HOOK         |
| 1        |        13 | U+0031    | DIGIT ONE                                          |
| 2        |        13 | U+0032    | DIGIT TWO                                          |
| ‐        |        10 | U+2010    | HYPHEN                                             |
| ҽ        |         9 | U+04BD    | CYRILLIC SMALL LETTER ABKHASIAN CHE                |
| џ        |         8 | U+045F    | CYRILLIC SMALL LETTER DZHE                         |
| Е        |         6 | U+0415    | CYRILLIC CAPITAL LETTER IE                         |
| Р        |         6 | U+0420    | CYRILLIC CAPITAL LETTER ER                         |
| 3        |         4 | U+0033    | DIGIT THREE                                        |
| 4        |         4 | U+0034    | DIGIT FOUR                                         |
| ;        |         3 | U+003B    | SEMICOLON                                          |
| 0        |         3 | U+0030    | DIGIT ZERO                                         |
| 5        |         3 | U+0035    | DIGIT FIVE                                         |
| 6        |         3 | U+0036    | DIGIT SIX                                          |
| 7        |         3 | U+0037    | DIGIT SEVEN                                        |
| 8        |         3 | U+0038    | DIGIT EIGHT                                        |
| 9        |         3 | U+0039    | DIGIT NINE                                         |
| З        |         3 | U+0417    | CYRILLIC CAPITAL LETTER ZE                         |
| У        |         3 | U+0423    | CYRILLIC CAPITAL LETTER U                          |
| ф        |         3 | U+0444    | CYRILLIC SMALL LETTER EF                           |
| –        |         2 | U+2013    | EN DASH                                            |
| И        |         2 | U+0418    | CYRILLIC CAPITAL LETTER I                          |
| в        |         1 | U+0432    | CYRILLIC SMALL LETTER VE                           |
| Н        |         1 | U+041D    | CYRILLIC CAPITAL LETTER EN                         |
| Х        |         1 | U+0425    | CYRILLIC CAPITAL LETTER HA                         |

For the input to the `write.profile` function, we first turn rows into a
list using the `purrrlyr` library.

``` r
# For testing:
# df <- df %>% filter(name %in% c('Abkhaz_abk', 'Acoma_kjq'))

x <- df %>% 
  slice_rows("name") %>% 
  by_slice(function(x) as.vector(t(x[6])), .to = "words")
```

Now we write each language’s profile to a CSV file.

``` r
for (i in 1:nrow(x)) {
  row <- x[i,]
  op <- write.profile(row$words[[1]])
  op$Frequency <- as.integer(op$Frequency)
  op <- op %>% arrange(desc(Frequency))
  fname <- paste0("orthography_profiles/", row$name, ".csv")
  write.csv(op, file=fname, row.names=FALSE)
}
```

# References

  - Moran, Steven and Michael Cysouw. 2018. The Unicode Cookbook for
    Linguists: Managing writing systems using orthography profiles.
    Translation and Multilingual Natural Language Process- ing series in
    Language Science Press. DOI:
    <https://doi.org/10.5281/zenodo.1296780>. Online:
    <http://langsci-press.org/catalog/book/176>.
