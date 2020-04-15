Compare word token counts from the 100LC corpus database and progress.py
================
Steven Moran
15 April, 2020

``` r
library(dplyr)
library(testthat)
library(knitr)
```

Normnally, we would load and query the SQLite database with an R library like `RSQLite` or dump it first as an `Rdata` object and query that directly. For example:

``` r
# Load the R serialized version of the 100 LC database
load('../../Database/100LC.Rdata')

# No NAs allows in the word.word_text field
expect_false(any(is.na(df$word_text)))

# Get word token and type counts per corpus and per writing system
db.token.counts <- df %>% select(name, writing_system, word_text) %>% group_by(name, writing_system) %>% summarize(db_tokens = n())
db.token.counts
```

However, when the current 100 LC corpus files are loaded into the database to the word level, there are 125,146,947 rows in the word table. Converting this on my laptop at the moment runs into memory issues.

As such, we can create a database view in SQLite that denormalizes the database tables into a 125,146,947 row table with pertinent metadata:

    CREATE VIEW IF NOT EXISTS v_words
    AS
    SELECT 
    word.id as word_id,
    line.id as line_id,
    line.file_id,
    corpus.id as corpus_id,
    language.id as language_id,
    word.text as word_text,
    line.text as line_text,
    file.writing_system,
    file.genre_broad as file_genre_broad,
    file.genre_narrow as file_genre_narrow,
    corpus.genre_broad,
    corpus.genre_narrow,
    language.name
    FROM word
    LEFT JOIN line ON word.line_id = line.id
    LEFT JOIN file ON line.file_id = file.id
    LEFT JOIN corpus ON file.corpus_id = corpus.id
    LEFT JOIN language on corpus.language_id = language.id;

and then do the word token counts per folder:

`select name, count(*) from v_words group by name`

or do the word token counts per corpus and writing system:

`select name, writing_system, count(*) from v_words group by name, writing_system`

The result is saved to a CSV file (one row is one corpus and its counts) called `results_db_word_token_counts.csv` and `results_db_word_token_counts-ws.csv`, respectively. We can use this to compare with the output from the `progress.py` tokenization script (simple tokenization counts).

``` r
# Read and rename
df <- read.csv('results_db_word_token_counts.csv')
df <- df %>% rename(db_tokens = "count...")

df.ws <- read.csv('results_db_word_token_counts-ws.csv')
df.ws <- df.ws %>% rename(db_tokens = "count...")
```

``` r
# Load simple tokenization counts from progres.py
simple <- read.csv('progress_simple.csv')
simple <- simple %>% select(language, number_tokens) %>% rename(name=language, simple_number_tokens=number_tokens)
```

``` r
# Combine language folder level
combined <- left_join(df, simple)
```

    ## Joining, by = "name"

    ## Warning: Column `name` joining factors with different levels, coercing to
    ## character vector

``` r
combined$delta <- abs(combined$db_tokens-combined$simple_number_tokens)
combined$diff <- round((combined$delta/combined$simple_number_tokens)*100, digits=2)
```

``` r
# Combine writing systems level
combined.ws <- left_join(df.ws, simple)
```

    ## Joining, by = "name"

    ## Warning: Column `name` joining factors with different levels, coercing to
    ## character vector

``` r
combined.ws$delta <- abs(combined.ws$db_tokens-combined.ws$simple_number_tokens)
combined.ws$diff <- round((combined.ws$delta/combined.ws$simple_number_tokens)*100, digits=2)
```

Here is when word tokens are counted at the folder level:

``` r
kable(combined)
```

| name                        |  db\_tokens|  simple\_number\_tokens|    delta|   diff|
|:----------------------------|-----------:|-----------------------:|--------:|------:|
| Abkhaz\_abk                 |        1325|                    2650|     1325|  50.00|
| Acoma\_kjq                  |        2433|                    2189|      244|  11.15|
| Alamblak\_amp               |      268933|                  276878|     7945|   2.87|
| Amele\_aey                  |      272657|                  282106|     9449|   3.35|
| Apurina\_apu                |      208147|                  216105|     7958|   3.68|
| Arabic\_Egyptian\_arz       |      528641|                  559809|    31168|   5.57|
| Arapesh\_Mountain\_ape      |      305611|                  313569|     7958|   2.54|
| Asmat\_tml                  |         198|                     736|      538|  73.10|
| Bagirmi\_bmi                |          70|                      67|        3|   4.48|
| Barasano\_bsn               |      293923|                  301879|     7956|   2.64|
| Basque\_eus                 |     2759182|                 2766143|     6961|   0.25|
| Berber\_MiddleAtlas\_tzm    |        1822|                    3644|     1822|  50.00|
| Burmese\_mya                |      495908|                  528128|    32220|   6.10|
| Burushaski\_bsk             |         198|                     185|       13|   7.03|
| CanelaKraho\_ram            |       40181|                   39898|      283|   0.71|
| Chamorro\_cha               |      223407|                  233275|     9868|   4.23|
| Chukchi\_ckt                |       21526|                   22677|     1151|   5.08|
| Daga\_dgz                   |      244867|                  252821|     7954|   3.15|
| Dani\_LowerGrandValley\_dni |         298|                      NA|       NA|     NA|
| English\_eng                |    10920747|                15955891|  5035144|  31.56|
| Fijian\_fij                 |      258501|                  268515|    10014|   3.73|
| Finnish\_fin                |    10860610|                15980444|  5119834|  32.04|
| French\_fra                 |    10429207|                15195137|  4765930|  31.36|
| Georgian\_kat               |      830181|                  836482|     6301|   0.75|
| German\_deu                 |    10970912|                16099011|  5128099|  31.85|
| Gooniyandi\_gni             |         130|                     240|      110|  45.83|
| Greek\_Modern\_ell          |    11054196|                16212378|  5158182|  31.82|
| Greenlandic\_West\_kal      |       80775|                   88134|     7359|   8.35|
| Guarani\_gug                |      171360|                  180442|     9082|   5.03|
| Hausa\_hau                  |      218071|                  231356|    13285|   5.74|
| Hebrew\_Modern\_heb         |     5176948|                 5290560|   113612|   2.15|
| Hindi\_hin                  |     2239972|                 2304409|    64437|   2.80|
| Hixkaryana\_hix             |       57024|                   57023|        1|   0.00|
| HmongNjua\_hnj              |        2801|                    5602|     2801|  50.00|
| Imonda\_imn                 |         395|                     354|       41|  11.58|
| Indonesian\_ind             |     5862905|                 5892959|    30054|   0.51|
| Jakaltek\_jac               |      257368|                  265326|     7958|   3.00|
| Japanese\_jpn               |     1264802|                 1290714|    25912|   2.01|
| Kannada\_kan                |        1080|                    2160|     1080|  50.00|
| Karok\_kyh                  |         399|                     379|       20|   5.28|
| Kayardild\_gyd              |          28|                      65|       37|  56.92|
| Kewa\_kew                   |      272925|                  282373|     9448|   3.35|
| Khalkha\_khk                |      163067|                  172549|     9482|   5.50|
| Khoekhoe\_naq               |      201484|                  209442|     7958|   3.80|
| Kiowa\_kio                  |          89|                      80|        9|  11.25|
| Korean\_kor                 |     3406865|                 3436864|    29999|   0.87|
| Kutenai\_kut                |          37|                      32|        5|  15.62|
| Lango\_laj                  |      206006|                  213964|     7958|   3.72|
| Lavukaleve\_lvk             |        2109|                    1905|      204|  10.71|
| Luvale\_lue                 |        1216|                    2432|     1216|  50.00|
| Makah\_myh                  |         245|                     393|      148|  37.66|
| Malagasy\_plt               |      784835|                  817977|    33142|   4.05|
| Mandarin\_cmn               |     1679626|                 1897794|   218168|  11.50|
| Mapudungun\_arn             |      228682|                  239259|    10577|   4.42|
| Martuthunira\_vma           |        4354|                    7658|     3304|  43.14|
| Maung\_mph                  |       25500|                   26176|      676|   2.58|
| Maybrat\_ayz                |         730|                     678|       52|   7.67|
| Mixtec\_Chalcatongo\_mig    |      215835|                  223793|     7958|   3.56|
| Ngiyambaa\_wyb              |          20|                      34|       14|  41.18|
| Oromo\_Harar\_hae           |      197918|                  205876|     7958|   3.87|
| Otomi\_Mezquital\_ote       |        1849|                    3698|     1849|  50.00|
| Persian\_pes                |     5352355|                 5385056|    32701|   0.61|
| Quechua\_Imbabura\_qvi      |      191056|                  198842|     7786|   3.92|
| Rama\_rma                   |         608|                     456|      152|  33.33|
| Rapanui\_rap                |        2817|                    2714|      103|   3.80|
| Russian\_rus                |     5818760|                 5903177|    84417|   1.43|
| Sango\_sag                  |      302257|                  312472|    10215|   3.27|
| Sanuma\_xsu                 |      492569|                  500527|     7958|   1.59|
| Spanish\_spa                |    10911957|                15914725|  5002768|  31.43|
| Swahili\_swh                |      158067|                  167424|     9357|   5.59|
| Tagalog\_tgl                |     1925933|                 2873591|   947658|  32.98|
| Thai\_tha                   |     2358800|                 2381971|    23171|   0.97|
| Turkish\_tur                |     5691421|                 5712949|    21528|   0.38|
| Vietnamese\_vie             |     5970823|                 6003452|    32629|   0.54|
| Warao\_wba                  |         430|                     395|       35|   8.86|
| Wichi\_mzh                  |      853136|                  884293|    31157|   3.52|
| Wichita\_wic                |         525|                     772|      247|  31.99|
| Yagua\_yad                  |      185004|                  194137|     9133|   4.70|
| Yaqui\_yaq                  |      298082|                  306039|     7957|   2.60|
| Yoruba\_yor                 |      909131|                  942404|    33273|   3.53|
| Zoque\_Copainala\_zoc       |        1010|                     872|      138|  15.83|
| Zulu\_zul                   |        1075|                    2150|     1075|  50.00|

Here is when word tokens are counted at the corpus and writing system levels:

``` r
kable(combined.ws)
```

| name                        | writing\_system |  db\_tokens|  simple\_number\_tokens|    delta|    diff|
|:----------------------------|:----------------|-----------:|-----------------------:|--------:|-------:|
| Abkhaz\_abk                 | Cyrl            |        1325|                    2650|     1325|   50.00|
| Acoma\_kjq                  | Latn            |        2433|                    2189|      244|   11.15|
| Alamblak\_amp               | Latn            |      268933|                  276878|     7945|    2.87|
| Amele\_aey                  | Latn            |      272657|                  282106|     9449|    3.35|
| Apurina\_apu                | Latn            |      208147|                  216105|     7958|    3.68|
| Arabic\_Egyptian\_arz       | Arab            |      528641|                  559809|    31168|    5.57|
| Arapesh\_Mountain\_ape      | Latn            |      305611|                  313569|     7958|    2.54|
| Asmat\_tml                  | Latn            |         198|                     736|      538|   73.10|
| Bagirmi\_bmi                | Latn            |          70|                      67|        3|    4.48|
| Barasano\_bsn               | Latn            |      293923|                  301879|     7956|    2.64|
| Basque\_eus                 | Latn            |     2759182|                 2766143|     6961|    0.25|
| Berber\_MiddleAtlas\_tzm    | Latn            |        1822|                    3644|     1822|   50.00|
| Burmese\_mya                | Mymr            |      495908|                  528128|    32220|    6.10|
| Burushaski\_bsk             | Latn            |         198|                     185|       13|    7.03|
| CanelaKraho\_ram            | Latn            |       40181|                   39898|      283|    0.71|
| Chamorro\_cha               | Latn            |      223407|                  233275|     9868|    4.23|
| Chukchi\_ckt                | Cyrl            |       21526|                   22677|     1151|    5.08|
| Daga\_dgz                   | Latn            |      244867|                  252821|     7954|    3.15|
| Dani\_LowerGrandValley\_dni | Latn            |         298|                      NA|       NA|      NA|
| English\_eng                | Latn            |    10920747|                15955891|  5035144|   31.56|
| Fijian\_fij                 | Latn            |      258501|                  268515|    10014|    3.73|
| Finnish\_fin                | Latn            |    10860610|                15980444|  5119834|   32.04|
| French\_fra                 | Latn            |    10429207|                15195137|  4765930|   31.36|
| Georgian\_kat               | Geor            |      830181|                  836482|     6301|    0.75|
| German\_deu                 | Latn            |    10970912|                16099011|  5128099|   31.85|
| Gooniyandi\_gni             | Latn            |         130|                     240|      110|   45.83|
| Greek\_Modern\_ell          | Grek            |    11054196|                16212378|  5158182|   31.82|
| Greenlandic\_West\_kal      | Latn            |       80775|                   88134|     7359|    8.35|
| Guarani\_gug                | Latn            |      171360|                  180442|     9082|    5.03|
| Hausa\_hau                  | Latn            |      218071|                  231356|    13285|    5.74|
| Hebrew\_Modern\_heb         | Hebr            |     5176948|                 5290560|   113612|    2.15|
| Hindi\_hin                  | Deva            |     1360057|                 2304409|   944352|   40.98|
| Hindi\_hin                  | Latn            |      879915|                 2304409|  1424494|   61.82|
| Hixkaryana\_hix             | Latn            |       57024|                   57023|        1|    0.00|
| HmongNjua\_hnj              | Latn            |        2801|                    5602|     2801|   50.00|
| Imonda\_imn                 | Latn            |         395|                     354|       41|   11.58|
| Indonesian\_ind             | Latn            |     5862905|                 5892959|    30054|    0.51|
| Jakaltek\_jac               | Latn            |      257368|                  265326|     7958|    3.00|
| Japanese\_jpn               | Jpan            |     1264802|                 1290714|    25912|    2.01|
| Kannada\_kan                | Knda            |        1080|                    2160|     1080|   50.00|
| Karok\_kyh                  | Latn            |         399|                     379|       20|    5.28|
| Kayardild\_gyd              | Latn            |          28|                      65|       37|   56.92|
| Kewa\_kew                   | Latn            |      272925|                  282373|     9448|    3.35|
| Khalkha\_khk                | Cyrl            |        1549|                  172549|   171000|   99.10|
| Khalkha\_khk                | Latn            |      161518|                  172549|    11031|    6.39|
| Khoekhoe\_naq               | Latn            |      201484|                  209442|     7958|    3.80|
| Kiowa\_kio                  | Latn            |          89|                      80|        9|   11.25|
| Korean\_kor                 | Hang            |      472758|                 3436864|  2964106|   86.24|
| Korean\_kor                 | Kore            |     2934107|                 3436864|   502757|   14.63|
| Kutenai\_kut                | Latn            |          37|                      32|        5|   15.62|
| Lango\_laj                  | Latn            |      206006|                  213964|     7958|    3.72|
| Lavukaleve\_lvk             | Latn            |        2109|                    1905|      204|   10.71|
| Luvale\_lue                 | Latn            |        1216|                    2432|     1216|   50.00|
| Makah\_myh                  | Latn            |         245|                     393|      148|   37.66|
| Malagasy\_plt               | Latn            |      784835|                  817977|    33142|    4.05|
| Mandarin\_cmn               | Hans            |     1679531|                 1897794|   218263|   11.50|
| Mandarin\_cmn               | Hant            |          95|                 1897794|  1897699|   99.99|
| Mapudungun\_arn             | Latn            |      228682|                  239259|    10577|    4.42|
| Martuthunira\_vma           | Latn            |        4354|                    7658|     3304|   43.14|
| Maung\_mph                  | Latn            |       25500|                   26176|      676|    2.58|
| Maybrat\_ayz                | Latn            |         730|                     678|       52|    7.67|
| Mixtec\_Chalcatongo\_mig    | Latn            |      215835|                  223793|     7958|    3.56|
| Ngiyambaa\_wyb              | Latn            |          20|                      34|       14|   41.18|
| Oromo\_Harar\_hae           | Latn            |      197918|                  205876|     7958|    3.87|
| Otomi\_Mezquital\_ote       | Latn            |        1849|                    3698|     1849|   50.00|
| Persian\_pes                | Arab            |     5352355|                 5385056|    32701|    0.61|
| Quechua\_Imbabura\_qvi      | Latn            |      191056|                  198842|     7786|    3.92|
| Rama\_rma                   | Latn            |         608|                     456|      152|   33.33|
| Rapanui\_rap                | Latn            |        2817|                    2714|      103|    3.80|
| Russian\_rus                | Cyrl            |     5818760|                 5903177|    84417|    1.43|
| Sango\_sag                  | Latn            |      302257|                  312472|    10215|    3.27|
| Sanuma\_xsu                 | Latn            |      492569|                  500527|     7958|    1.59|
| Spanish\_spa                | Latn            |    10911957|                15914725|  5002768|   31.43|
| Swahili\_swh                | Latn            |      158067|                  167424|     9357|    5.59|
| Tagalog\_tgl                | Latn            |     1925933|                 2873591|   947658|   32.98|
| Thai\_tha                   | Thai            |     2358800|                 2381971|    23171|    0.97|
| Turkish\_tur                | Latn            |     5691421|                 5712949|    21528|    0.38|
| Vietnamese\_vie             | Hani            |          94|                 6003452|  6003358|  100.00|
| Vietnamese\_vie             | Latn            |     5970729|                 6003452|    32723|    0.55|
| Warao\_wba                  | Latn            |         430|                     395|       35|    8.86|
| Wichi\_mzh                  | Latn            |      853136|                  884293|    31157|    3.52|
| Wichita\_wic                | Latn            |         525|                     772|      247|   31.99|
| Yagua\_yad                  | Latn            |      185004|                  194137|     9133|    4.70|
| Yaqui\_yaq                  | Latn            |      298082|                  306039|     7957|    2.60|
| Yoruba\_yor                 | Latn            |      909131|                  942404|    33273|    3.53|
| Zoque\_Copainala\_zoc       | Latn            |        1010|                     872|      138|   15.83|
| Zulu\_zul                   | Latn            |        1075|                    2150|     1075|   50.00|
