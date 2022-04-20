Generate initial orthography profiles
================
Steven Moran
23 August, 2020

Overview
========

In its simpliest form, an orthography profile (Moran & Cysouw, 2018) is
a Unicode character or Unicode grapheme unigram model, i.e. a CSV file
where each row represents a character or grapheme in a writing system
with additional information such as its frequency of occurrence in a
text. This report generates orthography profiles from each corpus in the
TeDDi database.

I use the TeDDi test data set for corpora for illustration purposes. The
output for each corpus is written to the `orthography_profiles` folder
in this directory. To run on the full database, load `TeDDi.Rdata`.

    # load('../../Database/test.RData')
    load('../../Database/TeDDi.Rdata')

First, we need to merge in the corpus IDs with the lines table.

    lines <- clc_line %>% select(file_id, text)
    corpus_ids <- clc_file %>% select(id, corpus_id) %>% distinct()
    lines <- left_join(corpus_ids, lines, by=c("id"="file_id"))

    # corpus_names <- tidyr::unite(clc_corpus, corpus, c(name, genre_broad))
    # corpus_ids <- corpus_names %>% select(id, corpus) %>% distinct()
    # lines <- left_join(corpus_ids, lines, by=c("id"="file_id"))
    glimpse(lines)

    ## Rows: 19,883,566
    ## Columns: 3
    ## $ id        <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,…
    ## $ corpus_id <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,…
    ## $ text      <chr> "Ауаҩытәыҩса изинқәа Зегьеицырзеиҧшу Адекларациа", "Алагала…

Here are the frequency counts (word counts) per corpus. Recall that we
need to do deal with languages that have multiple writing systems in the
same folder. TODO.

    table(lines$corpus_id) %>% kable()

| Var1 |    Freq |
|:-----|--------:|
| 1    |      91 |
| 2    |     266 |
| 3    |    7945 |
| 4    |    9477 |
| 5    |    7958 |
| 6    |   31174 |
| 7    |    7958 |
| 8    |      28 |
| 9    |       9 |
| 10   |    7956 |
| 11   |  585635 |
| 12   |      93 |
| 13   |      92 |
| 14   |   30997 |
| 15   |      91 |
| 16   |      54 |
| 17   |    1056 |
| 18   |    7925 |
| 19   |      92 |
| 20   |    1151 |
| 21   |    7954 |
| 22   |      22 |
| 23   |  494919 |
| 24   |  880307 |
| 25   |      92 |
| 26   |    7917 |
| 27   |      96 |
| 28   |  653116 |
| 29   | 1257089 |
| 30   |      96 |
| 31   |  531889 |
| 32   |  794207 |
| 33   |      91 |
| 34   |  156707 |
| 35   |      91 |
| 36   |  626298 |
| 37   |  890769 |
| 38   |      92 |
| 39   |      19 |
| 40   |  540205 |
| 41   |  932903 |
| 42   |     184 |
| 43   |    6287 |
| 44   |      91 |
| 45   |    7897 |
| 46   |      83 |
| 47   |    7931 |
| 48   |     182 |
| 49   |    8733 |
| 50   |  988784 |
| 51   |      89 |
| 52   |  137599 |
| 53   |      94 |
| 54   |    1232 |
| 55   |      91 |
| 56   |      51 |
| 57   | 1081625 |
| 58   |      92 |
| 59   |    7958 |
| 60   |   23015 |
| 61   |  833667 |
| 62   |      91 |
| 63   |      89 |
| 64   |       5 |
| 65   |    9448 |
| 66   |    7933 |
| 67   |      90 |
| 68   |    7958 |
| 69   |      13 |
| 70   |  799404 |
| 71   |      92 |
| 72   |      10 |
| 73   |    7958 |
| 74   |     226 |
| 75   |      90 |
| 76   |      46 |
| 77   |       3 |
| 78   |   31454 |
| 79   |      86 |
| 80   |  214838 |
| 81   |  758884 |
| 82   |     184 |
| 83   |    7958 |
| 84   |     144 |
| 85   |     634 |
| 86   |     676 |
| 87   |      64 |
| 88   |    7958 |
| 89   |       5 |
| 90   |    7958 |
| 91   |       1 |
| 92   |       2 |
| 93   |      91 |
| 94   |    1018 |
| 95   |  996810 |
| 96   |      90 |
| 97   |    7786 |
| 98   |     127 |
| 99   |      36 |
| 100  |     186 |
| 101  |    5826 |
| 102  | 1006147 |
| 103  |      92 |
| 104  |    7958 |
| 105  |      93 |
| 106  |    7958 |
| 107  |  555446 |
| 108  |  899563 |
| 109  |      92 |
| 110  |    7944 |
| 111  |      93 |
| 112  |  108206 |
| 113  |   42763 |
| 114  |      96 |
| 115  |  820750 |
| 116  |      90 |
| 117  | 1168920 |
| 118  |      92 |
| 119  |  721697 |
| 120  |     186 |
| 121  |      42 |
| 122  |   31157 |
| 123  |     144 |
| 124  |    7957 |
| 125  |      92 |
| 126  |    7957 |
| 127  |   30819 |
| 128  |      90 |
| 129  |     146 |
| 130  |      92 |

Here’s how we generate an initial orthography profile (a linguistically
correct orthography profile usually requires expert analysis of elements
such as bigraphs; see Moran & Cysouw, 2018 for detailed discussion).

    test <- lines %>% filter(id == 1)
    op <- write.profile(test$text)
    # Since we're working with lines, let's remove the spaces counted
    op <- op %>% filter(Grapheme!=" ")
    op$Frequency <- as.integer(op$Frequency)
    op %>% arrange(desc(Frequency)) %>% kable()

| Grapheme | Frequency | Codepoint | UnicodeName                                        |
|:---------|----------:|:----------|:---------------------------------------------------|
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

    corpus_names <- tidyr::unite(clc_corpus, corpus, c(name, genre_broad))

    x <- lines %>% 
      slice_rows("corpus_id") %>% 
      by_slice(function(x) as.vector(t(x[2])), .to = "words")

    for (i in 1:nrow(x)) {
      row <- x[i,]
      op <- write.profile(row$words[[1]])
      op$Frequency <- as.integer(op$Frequency)
      op <- op %>% filter(Grapheme!=" ")
      op <- op %>% arrange(desc(Frequency))
      # Create the corpus name
      filename <- corpus_names %>% filter(id == i) %>% select(corpus)
      fname <- paste0("orthography_profiles/", filename$corpus, ".csv")
      write.csv(op, file=fname, row.names=FALSE)
    }

References
==========

-   Moran, Steven and Michael Cysouw. 2018. The Unicode Cookbook for
    Linguists: Managing writing systems using orthography profiles.
    Translation and Multilingual Natural Language Process- ing series in
    Language Science Press. DOI:
    <a href="https://doi.org/10.5281/zenodo.1296780" class="uri">https://doi.org/10.5281/zenodo.1296780</a>.
    Online:
    <a href="http://langsci-press.org/catalog/book/176" class="uri">http://langsci-press.org/catalog/book/176</a>.
