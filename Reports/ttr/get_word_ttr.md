Generate word TTR for 100 LC corpora
================
Steven Moran
23 August, 2020

    library(readr)
    library(dplyr)
    library(knitr)
    library(tidytext)

Load the data. Make sure you load the right data source for your
purposes.

    # load('../../Database/test.RData') # for testing
    load('../../Database/100LC.RData') # full database

Genres are represented by corpus IDs in the database (see:
<a href="https://github.com/uzling/100LC/blob/master/Reports/genres/get_genres.md" class="uri">https://github.com/uzling/100LC/blob/master/Reports/genres/get_genres.md</a>).
This makes it easy to extract the pertinent file(s) per genre and to do
the various type / token counts.

However, the 100 LC corpus contains multiple writing scripts in files
within the same language and genre (see:
<a href="https://github.com/uzling/100LC/issues/189" class="uri">https://github.com/uzling/100LC/issues/189</a>).
For example notice that Vietnames (professional) has two files (from
UDHR) – one written in Latin script and the other written in
[Han](https://en.wikipedia.org/wiki/Chinese_characters):

    clc_file %>% 
      select(corpus_id, language_name_wals, genre_broad, writing_system) %>%
      group_by(corpus_id, language_name_wals, genre_broad, writing_system) %>%
      distinct() %>% 
      filter(language_name_wals %in% c('Hindi', 'Khalkha', 'Korean', 'Mandarin', 'Vietnamese')) %>%
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
|        119 | Vietnamese           | non-fiction  | Latn            |
|        120 | Vietnamese           | professional | Latn            |
|        120 | Vietnamese           | professional | Hani            |

For the languages that contain the same writing systems within their
genre folders, getting the counts is straightforward. However, because
the 100 LC corpus is so large, we can’t (yet) simply create the word TTR
in one pass, e.g.:

    # Merge the corpus IDs into the lines dataframe, so that we can apply tokenization on each corpus / genre
    # lines <- clc_line %>% select(file_id, text)
    # corpus_ids <- clc_file %>% select(id, corpus_id)
    # lines <- left_join(corpus_ids, lines, by=c("id"="file_id"))

    # Generate the TTRs per corpus -- this crashes due to memory issues!!
    # corpus_words <- lines %>% unnest_tokens(word, text) %>% count(corpus_id, word, sort = TRUE) %>% ungroup()
    # types_tokes <- corpus_words %>% group_by(corpus_id) %>% summarize(types=n(), tokens=sum(n)) %>% ungroup()

So insted, we apply tokenization and get the word TTRs to each corpus
individually and then we glue together the results into a dataframe.

    # Merge the corpus IDs into the lines dataframe, so that we can apply tokenization on each corpus / genre.
    lines <- clc_line %>% select(file_id, text)
    corpus_ids <- clc_file %>% select(id, corpus_id) %>% distinct()
    lines <- left_join(corpus_ids, lines, by=c("id"="file_id"))

    # Create a results dataframe to append the results to.
    header <- c("corpus_id", "mean_word_length", "types", "tokens")
    results <- as.data.frame(matrix(,0,length(header)))
    names(results) <- header

    # Loop over each corpus (todo: make this an apply()).
    ids <- clc_corpus %>% select(id) %>% distinct()
    ids <- as.numeric(ids$id)

    for(i in ids) {
      corpus_words <- lines %>% filter(corpus_id == i) %>% filter(!is.na(text)) %>% unnest_tokens(word, text) %>% count(corpus_id, word, sort = TRUE) %>% arrange(corpus_id, desc(n)) %>% ungroup()
      types_tokes <- corpus_words %>% group_by(corpus_id) %>% summarize(mean_word_length = mean(nchar(word)), types = n(), tokens = sum(n)) %>% ungroup()
      results <- rbind(results, types_tokes)
      }

How’s it look?

    results %>% kable()

| corpus\_id | mean\_word\_length |  types |  tokens |
|-----------:|-------------------:|-------:|--------:|
|          1 |           7.936468 |    787 |    1332 |
|          2 |           5.361602 |    849 |    3341 |
|          3 |           8.520930 |  25322 |  229160 |
|          4 |           7.803027 |  14139 |  233776 |
|          5 |          11.055038 |  14699 |  159164 |
|          6 |          10.090800 |  74262 |  434040 |
|          7 |           8.194023 |  14890 |  270754 |
|          8 |           6.363636 |     99 |     141 |
|          9 |           3.132076 |     53 |      71 |
|         10 |          10.554567 |  17089 |  221691 |
|         11 |           8.990461 | 126640 | 2715508 |
|         12 |           7.776521 |    707 |    1407 |
|         13 |           6.325373 |    670 |    1869 |
|         14 |           6.412945 |   6381 |  908516 |
|         15 |           5.863158 |    665 |    2966 |
|         16 |           5.634146 |    123 |     198 |
|         17 |           6.175485 |   3043 |   51061 |
|         18 |           8.457371 |   9653 |  198523 |
|         19 |           7.248686 |    571 |    1951 |
|         20 |          10.734592 |   5192 |   16442 |
|         21 |           7.214823 |   7839 |  214348 |
|         22 |           5.750000 |    160 |     337 |
|         23 |           7.790974 |  80966 | 5073103 |
|         24 |           7.567638 |  60787 | 5711261 |
|         25 |           6.670412 |    534 |    1753 |
|         26 |           7.599285 |   3636 |  227543 |
|         27 |           6.393939 |    396 |    2096 |
|         28 |          10.676729 | 366900 | 5021399 |
|         29 |          10.467545 | 340673 | 5549590 |
|         30 |           8.993932 |    824 |    1400 |
|         31 |           8.232076 | 133702 | 4814508 |
|         32 |           8.119468 |  97156 | 5436716 |
|         33 |           7.211747 |    647 |    1946 |
|         34 |           7.567129 |  81798 |  827965 |
|         35 |           8.674157 |    712 |    1410 |
|         36 |           9.909626 | 233110 | 5074046 |
|         37 |           9.683386 | 135986 | 5696371 |
|         38 |           8.250779 |    642 |    1642 |
|         39 |           8.650000 |     60 |      79 |
|         40 |           8.959064 | 289990 | 5054722 |
|         41 |           8.469943 | 174685 | 5738930 |
|         42 |           7.535151 |   1394 |    3822 |
|         43 |          14.349478 |  27006 |   62436 |
|         44 |          15.782913 |    714 |    1071 |
|         45 |           8.584286 |  12766 |  141501 |
|         46 |           7.313015 |    607 |    1189 |
|         47 |           6.865696 |   6865 |  177554 |
|         48 |           5.571429 |    602 |    5444 |
|         49 |           5.242953 |  27281 |  114252 |
|         50 |           6.077782 | 162005 | 5021329 |
|         51 |           5.120865 |    786 |    1278 |
|         52 |           6.625016 |  55189 | 2045075 |
|         53 |           5.358346 |    653 |    2076 |
|         54 |           9.282690 |   3732 |   43568 |
|         55 |           4.047325 |    486 |    2801 |
|         56 |           5.468927 |    177 |     289 |
|         57 |           8.008065 |  82826 | 5719697 |
|         58 |           7.302867 |    558 |    1726 |
|         59 |           8.974069 |  11762 |  220787 |
|         60 |           2.588794 |  26967 |  955184 |
|         61 |           3.549388 |  53221 | 5213332 |
|         62 |           2.076046 |    526 |    2161 |
|         63 |           9.282518 |    715 |    1081 |
|         64 |          10.000000 |     21 |      22 |
|         65 |           7.288460 |  10147 |  272299 |
|         66 |           8.096519 |  15945 |  138743 |
|         67 |           6.741401 |    785 |    1548 |
|         68 |           7.200598 |  10030 |  181370 |
|         69 |           3.386667 |     75 |     148 |
|         70 |           4.266655 | 425846 | 3372345 |
|         71 |           3.199088 |    658 |    1186 |
|         72 |           4.108108 |     37 |      60 |
|         73 |           5.458857 |   7316 |  174637 |
|         74 |           5.569395 |    562 |    1524 |
|         75 |           8.178876 |    587 |    1216 |
|         76 |          10.008772 |    114 |     138 |
|         77 |           8.684211 |     19 |      29 |
|         78 |           8.985914 |  30456 |  679065 |
|         79 |           7.512618 |    634 |    1857 |
|         80 |           2.028486 |  58133 | 4618542 |
|         81 |           3.981496 |  83494 | 4458428 |
|         82 |           1.904142 |    845 |    3094 |
|         83 |          10.679315 |  16630 |  193538 |
|         84 |           7.037915 |    422 |    2620 |
|         85 |          11.766234 |   1155 |    3133 |
|         86 |          10.126772 |   2540 |   22452 |
|         87 |           3.706806 |    191 |     726 |
|         88 |           6.412488 |   3988 |  226957 |
|         89 |           7.444444 |     18 |      22 |
|         90 |           8.490843 |  15944 |  163318 |
|         93 |           4.247839 |    347 |    1849 |
|         94 |           5.273291 |   6129 |   23201 |
|         95 |           6.847123 | 166755 | 5189444 |
|         96 |           5.026521 |    641 |    1821 |
|         97 |          11.212927 |  18288 |  142011 |
|         98 |           7.129630 |    270 |     396 |
|         99 |           6.695652 |     92 |     164 |
|        100 |           4.533149 |    362 |    2464 |
|        101 |           6.927666 |  13576 |   54202 |
|        102 |           8.416240 | 221031 | 5577162 |
|        103 |           8.085906 |    745 |    1611 |
|        104 |           5.513897 |   1691 |  265302 |
|        105 |           4.752500 |    400 |    2257 |
|        106 |           7.334711 |   7983 |  408796 |
|        107 |           8.339513 | 141762 | 5057876 |
|        108 |           8.186790 | 105675 | 5709621 |
|        109 |           7.407654 |    601 |    1927 |
|        110 |           8.828032 |  16317 |  128853 |
|        111 |           6.568998 |    529 |    1786 |
|        112 |           8.731317 |  83392 |  949474 |
|        113 |           8.694287 |  29737 |  891858 |
|        114 |           7.813875 |    591 |    2083 |
|        115 |           5.771105 |  57096 | 6662914 |
|        116 |           4.505576 |    538 |    2331 |
|        117 |           9.618920 | 300142 | 5468060 |
|        118 |           7.515775 |    729 |    1364 |
|        119 |           5.839708 |  34381 | 5865544 |
|        120 |           2.768382 |   1088 |    4492 |
|        121 |           6.595628 |    183 |     346 |
|        122 |           9.125226 |  24348 |  720572 |
|        123 |          13.121739 |    345 |     525 |
|        124 |          12.003390 |  21829 |  142301 |
|        125 |           8.679245 |    636 |    1180 |
|        126 |           8.900378 |  14013 |  240424 |
|        127 |           5.748823 |  12744 |  790879 |
|        128 |           5.050781 |    512 |    2548 |
|        129 |           7.594724 |    417 |     839 |
|        130 |           8.998591 |    710 |    1077 |

Let’s merge in the language names and clean it up a bit.

    results <- left_join(results, clc_corpus, by=c("corpus_id"="id"))
    results <- results %>% select(name, genre_broad, types, tokens)
    results$ttr <- (results$types / results$tokens)

Now how does it look?

    results %>% kable()

| name                        | genre\_broad |  types |  tokens |       ttr |
|:----------------------------|:-------------|-------:|--------:|----------:|
| Abkhaz\_abk                 | professional |    787 |    1332 | 0.5908408 |
| Acoma\_kjq                  | non-fiction  |    849 |    3341 | 0.2541155 |
| Alamblak\_amp               | non-fiction  |  25322 |  229160 | 0.1104992 |
| Amele\_aey                  | non-fiction  |  14139 |  233776 | 0.0604810 |
| Apurina\_apu                | non-fiction  |  14699 |  159164 | 0.0923513 |
| Arabic\_Egyptian\_arz       | non-fiction  |  74262 |  434040 | 0.1710948 |
| Arapesh\_Mountain\_ape      | non-fiction  |  14890 |  270754 | 0.0549946 |
| Asmat\_tml                  | conversation |     99 |     141 | 0.7021277 |
| Bagirmi\_bmi                | grammar      |     53 |      71 | 0.7464789 |
| Barasano\_bsn               | non-fiction  |  17089 |  221691 | 0.0770848 |
| Basque\_eus                 | non-fiction  | 126640 | 2715508 | 0.0466358 |
| Basque\_eus                 | professional |    707 |    1407 | 0.5024876 |
| Berber\_MiddleAtlas\_tzm    | professional |    670 |    1869 | 0.3584805 |
| Burmese\_mya                | non-fiction  |   6381 |  908516 | 0.0070235 |
| Burmese\_mya                | professional |    665 |    2966 | 0.2242077 |
| Burushaski\_bsk             | grammar      |    123 |     198 | 0.6212121 |
| CanelaKraho\_ram            | non-fiction  |   3043 |   51061 | 0.0595954 |
| Chamorro\_cha               | non-fiction  |   9653 |  198523 | 0.0486241 |
| Chamorro\_cha               | professional |    571 |    1951 | 0.2926704 |
| Chukchi\_ckt                | non-fiction  |   5192 |   16442 | 0.3157767 |
| Daga\_dgz                   | non-fiction  |   7839 |  214348 | 0.0365714 |
| Dani\_LowerGrandValley\_dni | conversation |    160 |     337 | 0.4747774 |
| English\_eng                | fiction      |  80966 | 5073103 | 0.0159599 |
| English\_eng                | non-fiction  |  60787 | 5711261 | 0.0106434 |
| English\_eng                | professional |    534 |    1753 | 0.3046207 |
| Fijian\_fij                 | non-fiction  |   3636 |  227543 | 0.0159794 |
| Fijian\_fij                 | professional |    396 |    2096 | 0.1889313 |
| Finnish\_fin                | fiction      | 366900 | 5021399 | 0.0730673 |
| Finnish\_fin                | non-fiction  | 340673 | 5549590 | 0.0613871 |
| Finnish\_fin                | professional |    824 |    1400 | 0.5885714 |
| French\_fra                 | fiction      | 133702 | 4814508 | 0.0277706 |
| French\_fra                 | non-fiction  |  97156 | 5436716 | 0.0178703 |
| French\_fra                 | professional |    647 |    1946 | 0.3324769 |
| Georgian\_kat               | non-fiction  |  81798 |  827965 | 0.0987940 |
| Georgian\_kat               | professional |    712 |    1410 | 0.5049645 |
| German\_deu                 | fiction      | 233110 | 5074046 | 0.0459416 |
| German\_deu                 | non-fiction  | 135986 | 5696371 | 0.0238724 |
| German\_deu                 | professional |    642 |    1642 | 0.3909866 |
| Gooniyandi\_gni             | conversation |     60 |      79 | 0.7594937 |
| Greek\_Modern\_ell          | fiction      | 289990 | 5054722 | 0.0573701 |
| Greek\_Modern\_ell          | non-fiction  | 174685 | 5738930 | 0.0304386 |
| Greek\_Modern\_ell          | professional |   1394 |    3822 | 0.3647305 |
| Greenlandic\_West\_kal      | non-fiction  |  27006 |   62436 | 0.4325389 |
| Greenlandic\_West\_kal      | professional |    714 |    1071 | 0.6666667 |
| Guarani\_gug                | non-fiction  |  12766 |  141501 | 0.0902184 |
| Guarani\_gug                | professional |    607 |    1189 | 0.5105130 |
| Hausa\_hau                  | non-fiction  |   6865 |  177554 | 0.0386643 |
| Hausa\_hau                  | professional |    602 |    5444 | 0.1105805 |
| Hebrew\_Modern\_heb         | fiction      |  27281 |  114252 | 0.2387792 |
| Hebrew\_Modern\_heb         | non-fiction  | 162005 | 5021329 | 0.0322634 |
| Hebrew\_Modern\_heb         | professional |    786 |    1278 | 0.6150235 |
| Hindi\_hin                  | non-fiction  |  55189 | 2045075 | 0.0269863 |
| Hindi\_hin                  | professional |    653 |    2076 | 0.3145472 |
| Hixkaryana\_hix             | non-fiction  |   3732 |   43568 | 0.0856592 |
| HmongNjua\_hnj              | professional |    486 |    2801 | 0.1735095 |
| Imonda\_imn                 | non-fiction  |    177 |     289 | 0.6124567 |
| Indonesian\_ind             | non-fiction  |  82826 | 5719697 | 0.0144808 |
| Indonesian\_ind             | professional |    558 |    1726 | 0.3232908 |
| Jakaltek\_jac               | non-fiction  |  11762 |  220787 | 0.0532731 |
| Japanese\_jpn               | fiction      |  26967 |  955184 | 0.0282323 |
| Japanese\_jpn               | non-fiction  |  53221 | 5213332 | 0.0102086 |
| Japanese\_jpn               | professional |    526 |    2161 | 0.2434058 |
| Kannada\_kan                | professional |    715 |    1081 | 0.6614246 |
| Kayardild\_gyd              | grammar      |     21 |      22 | 0.9545455 |
| Kewa\_kew                   | non-fiction  |  10147 |  272299 | 0.0372642 |
| Khalkha\_khk                | non-fiction  |  15945 |  138743 | 0.1149247 |
| Khalkha\_khk                | professional |    785 |    1548 | 0.5071059 |
| Khoekhoe\_naq               | non-fiction  |  10030 |  181370 | 0.0553013 |
| Kiowa\_kio                  | non-fiction  |     75 |     148 | 0.5067568 |
| Korean\_kor                 | non-fiction  | 425846 | 3372345 | 0.1262759 |
| Korean\_kor                 | professional |    658 |    1186 | 0.5548061 |
| Kutenai\_kut                | non-fiction  |     37 |      60 | 0.6166667 |
| Lango\_laj                  | non-fiction  |   7316 |  174637 | 0.0418926 |
| Lavukaleve\_lvk             | non-fiction  |    562 |    1524 | 0.3687664 |
| Luvale\_lue                 | professional |    587 |    1216 | 0.4827303 |
| Makah\_myh                  | conversation |    114 |     138 | 0.8260870 |
| Makah\_myh                  | non-fiction  |     19 |      29 | 0.6551724 |
| Malagasy\_plt               | non-fiction  |  30456 |  679065 | 0.0448499 |
| Malagasy\_plt               | professional |    634 |    1857 | 0.3414109 |
| Mandarin\_cmn               | fiction      |  58133 | 4618542 | 0.0125869 |
| Mandarin\_cmn               | non-fiction  |  83494 | 4458428 | 0.0187272 |
| Mandarin\_cmn               | professional |    845 |    3094 | 0.2731092 |
| Mapudungun\_arn             | non-fiction  |  16630 |  193538 | 0.0859263 |
| Mapudungun\_arn             | professional |    422 |    2620 | 0.1610687 |
| Martuthunira\_vma           | conversation |   1155 |    3133 | 0.3686562 |
| Maung\_mph                  | non-fiction  |   2540 |   22452 | 0.1131302 |
| Maybrat\_ayz                | non-fiction  |    191 |     726 | 0.2630854 |
| Mixtec\_Chalcatongo\_mig    | non-fiction  |   3988 |  226957 | 0.0175716 |
| Ngiyambaa\_wyb              | conversation |     18 |      22 | 0.8181818 |
| Oromo\_Harar\_hae           | non-fiction  |  15944 |  163318 | 0.0976255 |
| Otomi\_Mezquital\_ote       | professional |    347 |    1849 | 0.1876690 |
| Persian\_pes                | fiction      |   6129 |   23201 | 0.2641696 |
| Persian\_pes                | non-fiction  | 166755 | 5189444 | 0.0321335 |
| Persian\_pes                | professional |    641 |    1821 | 0.3520044 |
| Quechua\_Imbabura\_qvi      | non-fiction  |  18288 |  142011 | 0.1287788 |
| Rama\_rma                   | grammar      |    270 |     396 | 0.6818182 |
| Rama\_rma                   | non-fiction  |     92 |     164 | 0.5609756 |
| Rapanui\_rap                | non-fiction  |    362 |    2464 | 0.1469156 |
| Russian\_rus                | fiction      |  13576 |   54202 | 0.2504705 |
| Russian\_rus                | non-fiction  | 221031 | 5577162 | 0.0396314 |
| Russian\_rus                | professional |    745 |    1611 | 0.4624457 |
| Sango\_sag                  | non-fiction  |   1691 |  265302 | 0.0063739 |
| Sango\_sag                  | professional |    400 |    2257 | 0.1772264 |
| Sanuma\_xsu                 | non-fiction  |   7983 |  408796 | 0.0195281 |
| Spanish\_spa                | fiction      | 141762 | 5057876 | 0.0280280 |
| Spanish\_spa                | non-fiction  | 105675 | 5709621 | 0.0185082 |
| Spanish\_spa                | professional |    601 |    1927 | 0.3118838 |
| Swahili\_swh                | non-fiction  |  16317 |  128853 | 0.1266327 |
| Swahili\_swh                | professional |    529 |    1786 | 0.2961926 |
| Tagalog\_tgl                | fiction      |  83392 |  949474 | 0.0878297 |
| Tagalog\_tgl                | non-fiction  |  29737 |  891858 | 0.0333428 |
| Tagalog\_tgl                | professional |    591 |    2083 | 0.2837254 |
| Thai\_tha                   | non-fiction  |  57096 | 6662914 | 0.0085692 |
| Thai\_tha                   | professional |    538 |    2331 | 0.2308022 |
| Turkish\_tur                | non-fiction  | 300142 | 5468060 | 0.0548900 |
| Turkish\_tur                | professional |    729 |    1364 | 0.5344575 |
| Vietnamese\_vie             | non-fiction  |  34381 | 5865544 | 0.0058615 |
| Vietnamese\_vie             | professional |   1088 |    4492 | 0.2422084 |
| Warao\_wba                  | non-fiction  |    183 |     346 | 0.5289017 |
| Wichi\_mzh                  | non-fiction  |  24348 |  720572 | 0.0337898 |
| Wichita\_wic                | conversation |    345 |     525 | 0.6571429 |
| Yagua\_yad                  | non-fiction  |  21829 |  142301 | 0.1534002 |
| Yagua\_yad                  | professional |    636 |    1180 | 0.5389831 |
| Yaqui\_yaq                  | non-fiction  |  14013 |  240424 | 0.0582845 |
| Yoruba\_yor                 | non-fiction  |  12744 |  790879 | 0.0161137 |
| Yoruba\_yor                 | professional |    512 |    2548 | 0.2009419 |
| Zoque\_Copainala\_zoc       | non-fiction  |    417 |     839 | 0.4970203 |
| Zulu\_zul                   | professional |    710 |    1077 | 0.6592386 |

TODO: go through the languages with multiple writing systems
individually.

Lastly, write the results to disk.

    write_csv(results, 'word_ttr.csv')
