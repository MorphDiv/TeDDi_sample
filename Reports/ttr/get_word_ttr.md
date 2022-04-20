Generate word type-token ratios and mean word length for the TeDDi corpora
================
Steven Moran

31 October, 2020

    library(readr)
    library(dplyr)
    library(knitr)
    library(tidytext)

# Overview and analysis

Load the data. Make sure you load the right data source for your
purposes, i.e. development versus analysis (the test database is small
and is meant for code development).

    # load('../../Database/test.RData') # for testing
    load("../../Database/TeDDi.RData") # full database

Genres are represented by corpus IDs in the database (see:
<https://github.com/morphdiv/teddi_sample/blob/master/Reports/genres/get_genres.md>).
This makes it easy to extract the pertinent file(s) per genre and to do
the various type / token counts.

However, the TeDDi corpus contains multiple writing scripts in files
within the same language and genre (see:
<https://github.com/morphdiv/teddi_sample/issues/189>). For example, notice that
Vietnamese (professional) has two files (from UDHR) – one written in
Latin script and the other written in
[Han](https://en.wikipedia.org/wiki/Chinese_characters):

    clc_file %>%
      select(corpus_id, language_name_wals, genre_broad, writing_system) %>%
      group_by(corpus_id, language_name_wals, genre_broad, writing_system) %>%
      distinct() %>%
      filter(language_name_wals %in% c("Hindi", "Khalkha", "Korean", "Mandarin", "Vietnamese")) %>%
      kable()

| corpus\_id | language\_name\_wals | genre\_broad | writing\_system |
|-----------:|:---------------------|:-------------|:----------------|
|         52 | Hindi                | non-fiction  | Deva            |
|         52 | Hindi                | non-fiction  | Latn            |
|         53 | Hindi                | professional | Deva            |
|         66 | Khalkha              | non-fiction  | Latn            |
|         67 | Khalkha              | professional | Cyrl            |
|         70 | Korean               | non-fiction  | Hang            |
|         70 | Korean               | non-fiction  | Kore            |
|         71 | Korean               | professional | Hang            |
|         80 | Mandarin             | fiction      | Hans            |
|         81 | Mandarin             | non-fiction  | Hans            |
|         82 | Mandarin             | professional | Hans            |
|         82 | Mandarin             | professional | Hant            |
|        120 | Vietnamese           | non-fiction  | Latn            |
|        121 | Vietnamese           | professional | Latn            |
|        121 | Vietnamese           | professional | Hani            |

Because the TeDDi corpus design does not distinguish between writing
systems *within* the same genre in these limited cases, we cannot use a
more straightforward approach to calculate the word type-token ratios
for each corpus, i.e.:

    # Merge the corpus IDs into the lines dataframe, so that we can apply tokenization on each corpus / genre.
    lines <- clc_line %>% select(file_id, text)
    corpus_ids <- clc_file %>%
      select(id, corpus_id) %>%
      distinct()
    lines <- left_join(corpus_ids, lines, by = c("id" = "file_id"))

    # Create a results dataframe to append the results to.
    header <- c("corpus_id", "mean_word_length", "types", "tokens")
    results <- as.data.frame(matrix(, 0, length(header)))
    names(results) <- header

    # Loop over each corpus (todo: make this an apply()).
    ids <- clc_corpus %>%
      select(id) %>%
      distinct()
    ids <- as.numeric(ids$id)

    for (i in ids) {
      corpus_words <- lines %>%
        filter(corpus_id == i) %>%
        filter(!is.na(text)) %>%
        unnest_tokens(word, text) %>%
        count(corpus_id, word, sort = TRUE) %>%
        arrange(corpus_id, desc(n)) %>%
        ungroup()
      types_tokes <- corpus_words %>%
        group_by(corpus_id) %>%
        summarize(mean_word_length = mean(nchar(word)), types = n(), tokens = sum(n)) %>%
        ungroup()
      results <- rbind(results, types_tokes)
    }

The above code does work and produces results for each corpus that has a
single writing system, but it will treat corpora like Vietnamese (genre
professional) with two different writing systems as a single corpus.
Note that the corpus information above also needs to be merged together
with the metadata:

    results <- left_join(results, clc_corpus, by = c("corpus_id" = "id"))
    results <- results %>% select(name, genre_broad, types, tokens)
    results$ttr <- (results$types / results$tokens)

To address the issue of multiple writing systems within the same corpus,
we create a composite ID. Then we can identify which files within the
same corpus and genre have different writing systems.

    # Group corpora and genre by specific writing systems
    multiple_writing_systems <- clc_file %>%
      select(id, corpus_id, language_name_wals, genre_broad, writing_system) %>%
      group_by(corpus_id, language_name_wals, genre_broad, writing_system) %>%
      distinct()

    # Create the composite key
    multiple_writing_systems$composite_id <- paste0(multiple_writing_systems$corpus_id, "_", multiple_writing_systems$writing_system)
    multiple_writing_systems %>%
      filter(language_name_wals == "Vietnamese") %>%
      head() %>%
      kable()

|    id | corpus\_id | language\_name\_wals | genre\_broad | writing\_system | composite\_id |
|------:|-----------:|:---------------------|:-------------|:----------------|:--------------|
| 22402 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |
| 22403 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |
| 22404 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |
| 22405 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |
| 22406 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |
| 22407 |        120 | Vietnamese           | non-fiction  | Latn            | 120\_Latn     |

Next, we merge the compositie corpus IDs into the lines dataframe, so
that we can apply tokenization on each corpus / genre / writing system.

    lines <- clc_line %>% select(file_id, text)
    corpus_ids <- multiple_writing_systems %>%
      select(id, corpus_id, composite_id) %>%
      distinct()
    lines <- left_join(corpus_ids, lines, by = c("id" = "file_id"))

Then we create a results dataframe to append the results to.

    header <- c("corpus_id", "mean_word_length", "types", "tokens")
    results <- as.data.frame(matrix(, 0, length(header)))
    names(results) <- header

Now we loop over each corpus (todo: make this an `apply()`).

    ids <- multiple_writing_systems %>%
      ungroup() %>%
      select(composite_id) %>%
      distinct()

    for (i in ids$composite_id) {
      corpus_words <- lines %>%
        filter(composite_id == i) %>%
        filter(!is.na(text)) %>%
        unnest_tokens(word, text) %>%
        count(composite_id, word, sort = TRUE) %>%
        arrange(composite_id, desc(n)) %>%
        ungroup()
      types_tokes <- corpus_words %>%
        group_by(composite_id) %>%
        summarize(mean_word_length = mean(nchar(word)), types = n(), tokens = sum(n)) %>%
        ungroup()
      results <- rbind(results, types_tokes)
    }

How’s it look?

    results %>% kable()

| composite\_id | mean\_word\_length |  types |  tokens |
|:--------------|-------------------:|-------:|--------:|
| 1\_Cyrl       |           7.936468 |    787 |    1332 |
| 2\_Latn       |           5.361602 |    849 |    3341 |
| 3\_Latn       |           8.520930 |  25322 |  229160 |
| 4\_Latn       |           7.803027 |  14139 |  233776 |
| 5\_Latn       |          11.055038 |  14699 |  159164 |
| 6\_Arab       |          10.090800 |  74262 |  434040 |
| 7\_Latn       |           8.194023 |  14890 |  270754 |
| 8\_Latn       |           6.352381 |    105 |     153 |
| 9\_Latn       |           3.067797 |     59 |      79 |
| 10\_Latn      |          10.554567 |  17089 |  221691 |
| 11\_Latn      |           8.990461 | 126640 | 2715508 |
| 12\_Latn      |           7.776521 |    707 |    1407 |
| 13\_Latn      |           6.325373 |    670 |    1869 |
| 14\_Mymr      |           6.412945 |   6381 |  908516 |
| 15\_Mymr      |           5.863158 |    665 |    2966 |
| 16\_Latn      |           5.634146 |    123 |     203 |
| 17\_Latn      |           6.175485 |   3043 |   51061 |
| 18\_Latn      |           8.457371 |   9653 |  198523 |
| 19\_Latn      |           7.248686 |    571 |    1951 |
| 20\_Cyrl      |          10.734592 |   5192 |   16442 |
| 21\_Latn      |           7.214823 |   7839 |  214348 |
| 22\_Latn      |           5.731707 |    164 |     345 |
| 23\_Latn      |           7.790974 |  80966 | 5073103 |
| 24\_Latn      |           7.567638 |  60787 | 5711261 |
| 25\_Latn      |           6.670412 |    534 |    1753 |
| 26\_Latn      |           7.599285 |   3636 |  227543 |
| 27\_Latn      |           6.393939 |    396 |    2096 |
| 28\_Latn      |          10.676729 | 366900 | 5021399 |
| 29\_Latn      |          10.467545 | 340673 | 5549590 |
| 30\_Latn      |           8.993932 |    824 |    1400 |
| 31\_Latn      |           8.232076 | 133702 | 4814508 |
| 32\_Latn      |           8.119468 |  97156 | 5436716 |
| 33\_Latn      |           7.211747 |    647 |    1946 |
| 34\_Geor      |           7.567129 |  81798 |  827965 |
| 35\_Geor      |           8.674157 |    712 |    1410 |
| 36\_Latn      |           9.909626 | 233110 | 5074046 |
| 37\_Latn      |           9.683386 | 135986 | 5696371 |
| 38\_Latn      |           8.250779 |    642 |    1642 |
| 39\_Latn      |           8.640625 |     64 |      84 |
| 40\_Grek      |           8.959064 | 289990 | 5054722 |
| 41\_Grek      |           8.469943 | 174685 | 5738930 |
| 42\_Grek      |           7.535151 |   1394 |    3822 |
| 43\_Latn      |          14.349478 |  27006 |   62436 |
| 44\_Latn      |          15.782913 |    714 |    1071 |
| 45\_Latn      |           8.584286 |  12766 |  141501 |
| 46\_Latn      |           7.313015 |    607 |    1189 |
| 47\_Latn      |           6.865696 |   6865 |  177554 |
| 48\_Latn      |           5.571429 |    602 |    5444 |
| 49\_Hebr      |           5.242953 |  27281 |  114252 |
| 50\_Hebr      |           6.077782 | 162005 | 5021329 |
| 51\_Hebr      |           5.120865 |    786 |    1278 |
| 52\_Deva      |           6.163156 |  34985 | 1252888 |
| 52\_Latn      |           7.384408 |  20395 |  792187 |
| 53\_Deva      |           5.358346 |    653 |    2076 |
| 54\_Latn      |           9.282690 |   3732 |   43568 |
| 55\_Latn      |           4.047325 |    486 |    2801 |
| 56\_Latn      |           5.480663 |    181 |     296 |
| 57\_Latn      |           8.008065 |  82826 | 5719697 |
| 58\_Latn      |           7.302867 |    558 |    1726 |
| 59\_Latn      |           8.974069 |  11762 |  220787 |
| 60\_Jpan      |           2.588794 |  26967 |  955184 |
| 61\_Jpan      |           3.549388 |  53221 | 5213332 |
| 62\_Jpan      |           2.076046 |    526 |    2161 |
| 63\_Knda      |           9.282518 |    715 |    1081 |
| 64\_Latn      |          10.080000 |     25 |      27 |
| 65\_Latn      |           7.288460 |  10147 |  272299 |
| 66\_Latn      |           8.096519 |  15945 |  138743 |
| 67\_Cyrl      |           6.741401 |    785 |    1548 |
| 68\_Latn      |           7.200598 |  10030 |  181370 |
| 69\_Latn      |           3.382716 |     81 |     154 |
| 70\_Hang      |           3.817717 |  62831 |  455182 |
| 70\_Kore      |           4.284915 | 379629 | 2917163 |
| 71\_Hang      |           3.199088 |    658 |    1186 |
| 72\_Latn      |           4.268293 |     41 |      66 |
| 73\_Latn      |           5.458857 |   7316 |  174637 |
| 74\_Latn      |           5.567376 |    564 |    1537 |
| 75\_Latn      |           8.178876 |    587 |    1216 |
| 76\_Latn      |           9.933333 |    120 |     145 |
| 77\_Latn      |           8.684211 |     19 |      33 |
| 78\_Latn      |           8.985914 |  30456 |  679065 |
| 79\_Latn      |           7.512618 |    634 |    1857 |
| 80\_Hans      |           2.028486 |  58133 | 4618542 |
| 81\_Hans      |           3.981496 |  83494 | 4458428 |
| 82\_Hans      |           1.876076 |    581 |    1606 |
| 82\_Hant      |           1.915285 |    543 |    1488 |
| 83\_Latn      |          10.679315 |  16630 |  193538 |
| 84\_Latn      |           7.037915 |    422 |    2620 |
| 85\_Latn      |          11.778830 |   1162 |    3157 |
| 86\_Latn      |          10.126772 |   2540 |   22452 |
| 87\_Latn      |           3.703125 |    192 |     737 |
| 88\_Latn      |           6.412488 |   3988 |  226957 |
| 89\_Latn      |           9.895792 |    499 |     635 |
| 90\_Latn      |           8.490843 |  15944 |  163318 |
| 91\_Latn      |           4.285714 |      7 |       9 |
| 92\_Latn      |           3.647059 |     17 |      17 |
| 93\_Latn      |           4.247839 |    347 |    1849 |
| 94\_Arab      |           5.273291 |   6129 |   23201 |
| 95\_Arab      |           6.847123 | 166755 | 5189444 |
| 96\_Arab      |           5.026521 |    641 |    1821 |
| 97\_Latn      |           4.944359 |    647 |    6300 |
| 98\_Latn      |          11.212927 |  18288 |  142011 |
| 99\_Latn      |           7.121771 |    271 |     400 |
| 100\_Latn     |           6.670213 |     94 |     169 |
| 101\_Latn     |           4.553134 |    367 |    2535 |
| 102\_Cyrl     |           6.927666 |  13576 |   54202 |
| 103\_Cyrl     |           8.416240 | 221031 | 5577162 |
| 104\_Cyrl     |           8.085906 |    745 |    1611 |
| 105\_Latn     |           5.513897 |   1691 |  265302 |
| 106\_Latn     |           4.752500 |    400 |    2257 |
| 107\_Latn     |           7.334711 |   7983 |  408796 |
| 108\_Latn     |           8.339513 | 141762 | 5057876 |
| 109\_Latn     |           8.186790 | 105675 | 5709621 |
| 110\_Latn     |           7.407654 |    601 |    1927 |
| 111\_Latn     |           8.828032 |  16317 |  128853 |
| 112\_Latn     |           6.568998 |    529 |    1786 |
| 113\_Latn     |           8.731317 |  83392 |  949474 |
| 114\_Latn     |           8.694287 |  29737 |  891858 |
| 115\_Latn     |           7.813875 |    591 |    2083 |
| 116\_Thai     |           5.771105 |  57096 | 6662914 |
| 117\_Thai     |           4.505576 |    538 |    2331 |
| 118\_Latn     |           9.618920 | 300142 | 5468060 |
| 119\_Latn     |           7.515775 |    729 |    1364 |
| 120\_Latn     |           5.839708 |  34381 | 5865544 |
| 121\_Latn     |           4.077617 |    554 |    2502 |
| 121\_Hani     |           1.435626 |    567 |    1990 |
| 122\_Latn     |           6.616216 |    185 |     351 |
| 123\_Latn     |           9.125226 |  24348 |  720572 |
| 124\_Latn     |          13.215517 |    348 |     529 |
| 125\_Latn     |          12.003390 |  21829 |  142301 |
| 126\_Latn     |           8.679245 |    636 |    1180 |
| 127\_Latn     |           8.900378 |  14013 |  240424 |
| 128\_Latn     |           5.748823 |  12744 |  790879 |
| 129\_Latn     |           5.050781 |    512 |    2548 |
| 130\_Latn     |           7.616667 |    420 |     846 |
| 131\_Latn     |           8.998591 |    710 |    1077 |

Let’s add the metadata to the results and generate the TTR.

    metadata <- multiple_writing_systems %>%
      select(corpus_id, language_name_wals, genre_broad, writing_system, composite_id) %>%
      distinct()
    results <- left_join(results, metadata, by = c("composite_id" = "composite_id"))
    results <- results %>% select(language_name_wals, genre_broad, writing_system, types, tokens, mean_word_length)
    results$ttr <- (results$types / results$tokens)

Reports use the TeDDi language names because those are NULL for
languages not yet in the corpus. Let’s merge them back in.

    language_names <- clc_language %>% select(name, name_wals)
    results <- left_join(results, language_names, by = c("language_name_wals" = "name_wals"))
    results <- results %>% select(name, genre_broad, writing_system, types, tokens, mean_word_length, ttr)

Now how does it look?

    results %>% kable()

| name                        | genre\_broad | writing\_system |  types |  tokens | mean\_word\_length |       ttr |
|:----------------------------|:-------------|:----------------|-------:|--------:|-------------------:|----------:|
| Abkhaz\_abk                 | professional | Cyrl            |    787 |    1332 |           7.936468 | 0.5908408 |
| Acoma\_kjq                  | non-fiction  | Latn            |    849 |    3341 |           5.361602 | 0.2541155 |
| Alamblak\_amp               | non-fiction  | Latn            |  25322 |  229160 |           8.520930 | 0.1104992 |
| Amele\_aey                  | non-fiction  | Latn            |  14139 |  233776 |           7.803027 | 0.0604810 |
| Apurina\_apu                | non-fiction  | Latn            |  14699 |  159164 |          11.055038 | 0.0923513 |
| Arabic\_Egyptian\_arz       | non-fiction  | Arab            |  74262 |  434040 |          10.090800 | 0.1710948 |
| Arapesh\_Mountain\_ape      | non-fiction  | Latn            |  14890 |  270754 |           8.194023 | 0.0549946 |
| Asmat\_tml                  | conversation | Latn            |    105 |     153 |           6.352381 | 0.6862745 |
| Bagirmi\_bmi                | grammar      | Latn            |     59 |      79 |           3.067797 | 0.7468354 |
| Barasano\_bsn               | non-fiction  | Latn            |  17089 |  221691 |          10.554567 | 0.0770848 |
| Basque\_eus                 | non-fiction  | Latn            | 126640 | 2715508 |           8.990461 | 0.0466358 |
| Basque\_eus                 | professional | Latn            |    707 |    1407 |           7.776521 | 0.5024876 |
| Berber\_MiddleAtlas\_tzm    | professional | Latn            |    670 |    1869 |           6.325373 | 0.3584805 |
| Burmese\_mya                | non-fiction  | Mymr            |   6381 |  908516 |           6.412945 | 0.0070235 |
| Burmese\_mya                | professional | Mymr            |    665 |    2966 |           5.863158 | 0.2242077 |
| Burushaski\_bsk             | grammar      | Latn            |    123 |     203 |           5.634146 | 0.6059113 |
| CanelaKraho\_ram            | non-fiction  | Latn            |   3043 |   51061 |           6.175485 | 0.0595954 |
| Chamorro\_cha               | non-fiction  | Latn            |   9653 |  198523 |           8.457371 | 0.0486241 |
| Chamorro\_cha               | professional | Latn            |    571 |    1951 |           7.248686 | 0.2926704 |
| Chukchi\_ckt                | non-fiction  | Cyrl            |   5192 |   16442 |          10.734592 | 0.3157767 |
| Daga\_dgz                   | non-fiction  | Latn            |   7839 |  214348 |           7.214823 | 0.0365714 |
| Dani\_LowerGrandValley\_dni | conversation | Latn            |    164 |     345 |           5.731707 | 0.4753623 |
| English\_eng                | fiction      | Latn            |  80966 | 5073103 |           7.790974 | 0.0159599 |
| English\_eng                | non-fiction  | Latn            |  60787 | 5711261 |           7.567638 | 0.0106434 |
| English\_eng                | professional | Latn            |    534 |    1753 |           6.670412 | 0.3046207 |
| Fijian\_fij                 | non-fiction  | Latn            |   3636 |  227543 |           7.599285 | 0.0159794 |
| Fijian\_fij                 | professional | Latn            |    396 |    2096 |           6.393939 | 0.1889313 |
| Finnish\_fin                | fiction      | Latn            | 366900 | 5021399 |          10.676729 | 0.0730673 |
| Finnish\_fin                | non-fiction  | Latn            | 340673 | 5549590 |          10.467545 | 0.0613871 |
| Finnish\_fin                | professional | Latn            |    824 |    1400 |           8.993932 | 0.5885714 |
| French\_fra                 | fiction      | Latn            | 133702 | 4814508 |           8.232076 | 0.0277706 |
| French\_fra                 | non-fiction  | Latn            |  97156 | 5436716 |           8.119468 | 0.0178703 |
| French\_fra                 | professional | Latn            |    647 |    1946 |           7.211747 | 0.3324769 |
| Georgian\_kat               | non-fiction  | Geor            |  81798 |  827965 |           7.567129 | 0.0987940 |
| Georgian\_kat               | professional | Geor            |    712 |    1410 |           8.674157 | 0.5049645 |
| German\_deu                 | fiction      | Latn            | 233110 | 5074046 |           9.909626 | 0.0459416 |
| German\_deu                 | non-fiction  | Latn            | 135986 | 5696371 |           9.683386 | 0.0238724 |
| German\_deu                 | professional | Latn            |    642 |    1642 |           8.250779 | 0.3909866 |
| Gooniyandi\_gni             | conversation | Latn            |     64 |      84 |           8.640625 | 0.7619048 |
| Greek\_Modern\_ell          | fiction      | Grek            | 289990 | 5054722 |           8.959064 | 0.0573701 |
| Greek\_Modern\_ell          | non-fiction  | Grek            | 174685 | 5738930 |           8.469943 | 0.0304386 |
| Greek\_Modern\_ell          | professional | Grek            |   1394 |    3822 |           7.535151 | 0.3647305 |
| Greenlandic\_West\_kal      | non-fiction  | Latn            |  27006 |   62436 |          14.349478 | 0.4325389 |
| Greenlandic\_West\_kal      | professional | Latn            |    714 |    1071 |          15.782913 | 0.6666667 |
| NA                          | non-fiction  | Latn            |  12766 |  141501 |           8.584286 | 0.0902184 |
| Guarani\_gug                | professional | Latn            |    607 |    1189 |           7.313015 | 0.5105130 |
| Hausa\_hau                  | non-fiction  | Latn            |   6865 |  177554 |           6.865696 | 0.0386643 |
| Hausa\_hau                  | professional | Latn            |    602 |    5444 |           5.571429 | 0.1105805 |
| Hebrew\_Modern\_heb         | fiction      | Hebr            |  27281 |  114252 |           5.242953 | 0.2387792 |
| Hebrew\_Modern\_heb         | non-fiction  | Hebr            | 162005 | 5021329 |           6.077782 | 0.0322634 |
| Hebrew\_Modern\_heb         | professional | Hebr            |    786 |    1278 |           5.120865 | 0.6150235 |
| Hindi\_hin                  | non-fiction  | Deva            |  34985 | 1252888 |           6.163156 | 0.0279235 |
| Hindi\_hin                  | non-fiction  | Latn            |  20395 |  792187 |           7.384408 | 0.0257452 |
| Hindi\_hin                  | professional | Deva            |    653 |    2076 |           5.358346 | 0.3145472 |
| Hixkaryana\_hix             | non-fiction  | Latn            |   3732 |   43568 |           9.282690 | 0.0856592 |
| HmongNjua\_hnj              | professional | Latn            |    486 |    2801 |           4.047325 | 0.1735095 |
| Imonda\_imn                 | non-fiction  | Latn            |    181 |     296 |           5.480663 | 0.6114865 |
| Indonesian\_ind             | non-fiction  | Latn            |  82826 | 5719697 |           8.008065 | 0.0144808 |
| Indonesian\_ind             | professional | Latn            |    558 |    1726 |           7.302867 | 0.3232908 |
| Jakaltek\_jac               | non-fiction  | Latn            |  11762 |  220787 |           8.974069 | 0.0532731 |
| Japanese\_jpn               | fiction      | Jpan            |  26967 |  955184 |           2.588794 | 0.0282323 |
| Japanese\_jpn               | non-fiction  | Jpan            |  53221 | 5213332 |           3.549388 | 0.0102086 |
| Japanese\_jpn               | professional | Jpan            |    526 |    2161 |           2.076046 | 0.2434058 |
| Kannada\_kan                | professional | Knda            |    715 |    1081 |           9.282518 | 0.6614246 |
| Kayardild\_gyd              | grammar      | Latn            |     25 |      27 |          10.080000 | 0.9259259 |
| Kewa\_kew                   | non-fiction  | Latn            |  10147 |  272299 |           7.288460 | 0.0372642 |
| Khalkha\_khk                | non-fiction  | Latn            |  15945 |  138743 |           8.096519 | 0.1149247 |
| Khalkha\_khk                | professional | Cyrl            |    785 |    1548 |           6.741401 | 0.5071059 |
| Khoekhoe\_naq               | non-fiction  | Latn            |  10030 |  181370 |           7.200598 | 0.0553013 |
| Kiowa\_kio                  | non-fiction  | Latn            |     81 |     154 |           3.382716 | 0.5259740 |
| Korean\_kor                 | non-fiction  | Hang            |  62831 |  455182 |           3.817717 | 0.1380349 |
| Korean\_kor                 | non-fiction  | Kore            | 379629 | 2917163 |           4.284915 | 0.1301364 |
| Korean\_kor                 | professional | Hang            |    658 |    1186 |           3.199088 | 0.5548061 |
| Kutenai\_kut                | non-fiction  | Latn            |     41 |      66 |           4.268293 | 0.6212121 |
| Lango\_laj                  | non-fiction  | Latn            |   7316 |  174637 |           5.458857 | 0.0418926 |
| Lavukaleve\_lvk             | non-fiction  | Latn            |    564 |    1537 |           5.567376 | 0.3669486 |
| Luvale\_lue                 | professional | Latn            |    587 |    1216 |           8.178876 | 0.4827303 |
| Makah\_myh                  | conversation | Latn            |    120 |     145 |           9.933333 | 0.8275862 |
| Makah\_myh                  | non-fiction  | Latn            |     19 |      33 |           8.684211 | 0.5757576 |
| Malagasy\_plt               | non-fiction  | Latn            |  30456 |  679065 |           8.985914 | 0.0448499 |
| Malagasy\_plt               | professional | Latn            |    634 |    1857 |           7.512618 | 0.3414109 |
| Mandarin\_cmn               | fiction      | Hans            |  58133 | 4618542 |           2.028486 | 0.0125869 |
| Mandarin\_cmn               | non-fiction  | Hans            |  83494 | 4458428 |           3.981496 | 0.0187272 |
| Mandarin\_cmn               | professional | Hans            |    581 |    1606 |           1.876076 | 0.3617684 |
| Mandarin\_cmn               | professional | Hant            |    543 |    1488 |           1.915285 | 0.3649194 |
| Mapudungun\_arn             | non-fiction  | Latn            |  16630 |  193538 |          10.679315 | 0.0859263 |
| Mapudungun\_arn             | professional | Latn            |    422 |    2620 |           7.037915 | 0.1610687 |
| Martuthunira\_vma           | conversation | Latn            |   1162 |    3157 |          11.778830 | 0.3680710 |
| Maung\_mph                  | non-fiction  | Latn            |   2540 |   22452 |          10.126772 | 0.1131302 |
| Maybrat\_ayz                | non-fiction  | Latn            |    192 |     737 |           3.703125 | 0.2605156 |
| Mixtec\_Chalcatongo\_mig    | non-fiction  | Latn            |   3988 |  226957 |           6.412488 | 0.0175716 |
| Ngiyambaa\_wyb              | conversation | Latn            |    499 |     635 |           9.895792 | 0.7858268 |
| Oromo\_Harar\_hae           | non-fiction  | Latn            |  15944 |  163318 |           8.490843 | 0.0976255 |
| Otomi\_Mezquital\_ote       | grammar      | Latn            |      7 |       9 |           4.285714 | 0.7777778 |
| Otomi\_Mezquital\_ote       | non-fiction  | Latn            |     17 |      17 |           3.647059 | 1.0000000 |
| NA                          | professional | Latn            |    347 |    1849 |           4.247839 | 0.1876690 |
| Persian\_pes                | fiction      | Arab            |   6129 |   23201 |           5.273291 | 0.2641696 |
| Persian\_pes                | non-fiction  | Arab            | 166755 | 5189444 |           6.847123 | 0.0321335 |
| Persian\_pes                | professional | Arab            |    641 |    1821 |           5.026521 | 0.3520044 |
| Piraha\_myp                 | non-fiction  | Latn            |    647 |    6300 |           4.944359 | 0.1026984 |
| Quechua\_Imbabura\_qvi      | non-fiction  | Latn            |  18288 |  142011 |          11.212927 | 0.1287788 |
| Rama\_rma                   | grammar      | Latn            |    271 |     400 |           7.121771 | 0.6775000 |
| Rama\_rma                   | non-fiction  | Latn            |     94 |     169 |           6.670213 | 0.5562130 |
| Rapanui\_rap                | non-fiction  | Latn            |    367 |    2535 |           4.553134 | 0.1447732 |
| Russian\_rus                | fiction      | Cyrl            |  13576 |   54202 |           6.927666 | 0.2504705 |
| Russian\_rus                | non-fiction  | Cyrl            | 221031 | 5577162 |           8.416240 | 0.0396314 |
| Russian\_rus                | professional | Cyrl            |    745 |    1611 |           8.085906 | 0.4624457 |
| Sango\_sag                  | non-fiction  | Latn            |   1691 |  265302 |           5.513897 | 0.0063739 |
| Sango\_sag                  | professional | Latn            |    400 |    2257 |           4.752500 | 0.1772264 |
| Sanuma\_xsu                 | non-fiction  | Latn            |   7983 |  408796 |           7.334711 | 0.0195281 |
| Spanish\_spa                | fiction      | Latn            | 141762 | 5057876 |           8.339513 | 0.0280280 |
| Spanish\_spa                | non-fiction  | Latn            | 105675 | 5709621 |           8.186790 | 0.0185082 |
| Spanish\_spa                | professional | Latn            |    601 |    1927 |           7.407654 | 0.3118838 |
| Swahili\_swh                | non-fiction  | Latn            |  16317 |  128853 |           8.828032 | 0.1266327 |
| Swahili\_swh                | professional | Latn            |    529 |    1786 |           6.568998 | 0.2961926 |
| Tagalog\_tgl                | fiction      | Latn            |  83392 |  949474 |           8.731317 | 0.0878297 |
| Tagalog\_tgl                | non-fiction  | Latn            |  29737 |  891858 |           8.694287 | 0.0333428 |
| Tagalog\_tgl                | professional | Latn            |    591 |    2083 |           7.813875 | 0.2837254 |
| Thai\_tha                   | non-fiction  | Thai            |  57096 | 6662914 |           5.771105 | 0.0085692 |
| Thai\_tha                   | professional | Thai            |    538 |    2331 |           4.505576 | 0.2308022 |
| Turkish\_tur                | non-fiction  | Latn            | 300142 | 5468060 |           9.618920 | 0.0548900 |
| Turkish\_tur                | professional | Latn            |    729 |    1364 |           7.515775 | 0.5344575 |
| Vietnamese\_vie             | non-fiction  | Latn            |  34381 | 5865544 |           5.839708 | 0.0058615 |
| Vietnamese\_vie             | professional | Latn            |    554 |    2502 |           4.077617 | 0.2214229 |
| Vietnamese\_vie             | professional | Hani            |    567 |    1990 |           1.435626 | 0.2849246 |
| Warao\_wba                  | non-fiction  | Latn            |    185 |     351 |           6.616216 | 0.5270655 |
| Wichi\_mzh                  | non-fiction  | Latn            |  24348 |  720572 |           9.125226 | 0.0337898 |
| Wichita\_wic                | conversation | Latn            |    348 |     529 |          13.215517 | 0.6578450 |
| Yagua\_yad                  | non-fiction  | Latn            |  21829 |  142301 |          12.003390 | 0.1534002 |
| Yagua\_yad                  | professional | Latn            |    636 |    1180 |           8.679245 | 0.5389831 |
| Yaqui\_yaq                  | non-fiction  | Latn            |  14013 |  240424 |           8.900378 | 0.0582845 |
| Yoruba\_yor                 | non-fiction  | Latn            |  12744 |  790879 |           5.748823 | 0.0161137 |
| Yoruba\_yor                 | professional | Latn            |    512 |    2548 |           5.050781 | 0.2009419 |
| Zoque\_Copainala\_zoc       | non-fiction  | Latn            |    420 |     846 |           7.616667 | 0.4964539 |
| Zulu\_zul                   | professional | Latn            |    710 |    1077 |           8.998591 | 0.6592386 |

Lastly, write the results to disk.

    write_csv(results, "word_ttr.csv")

# Future

For the languages that contain the same writing systems within their
genre folders, getting the counts is straightforward. However, because
the TeDDi corpus is so large, we can’t (yet) simply create the word TTR
in one pass, e.g.:

    # Merge the corpus IDs into the lines dataframe, so that we can apply tokenization on each corpus / genre
    # lines <- clc_line %>% select(file_id, text)
    # corpus_ids <- clc_file %>% select(id, corpus_id)
    # lines <- left_join(corpus_ids, lines, by=c("id"="file_id"))

    # Generate the TTRs per corpus -- this crashes due to memory issues!!
    # corpus_words <- lines %>% unnest_tokens(word, text) %>% count(corpus_id, word, sort = TRUE) %>% ungroup()
    # types_tokes <- corpus_words %>% group_by(corpus_id) %>% summarize(types=n(), tokens=sum(n)) %>% ungroup()

Maybe something for the future.
