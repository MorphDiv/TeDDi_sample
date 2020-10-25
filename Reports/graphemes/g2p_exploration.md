Grapheme to phoneme exploration
================
Steven Moran
07 September, 2020

Overview
========

First, this report investigates various resources on writing systems and
what the coverage of those resources are on the 100LC language sample.
Second, in light of a potential novel model of g2p conversion using
neural networks at the level of phonetic features, I investigate the
coverage of [PHOIBLE](https://phoible.org/) on the data in the
[SIGMORPHON 2020 shared task for g2p
conversion](https://www.aclweb.org/anthology/2020.sigmorphon-1.2/).

Writing system coverage of 100LC data
-------------------------------------

This is the 100LC language info index file (planned languages, not
actual languages in the corpus).

    index <- read.csv('../../LangInfo/langInfo_100LC.csv')

    head(index) %>% kable()

| iso639\_3 | glottocode | wals\_code | name\_glotto    | name\_wals | level    | status                | family\_id | top\_level\_family       | genus\_wals         | family\_wals        | macroarea\_glotto | macroarea\_wals | latitude\_glotto | longitude\_glotto | latitude\_wals | longitude\_wals | name          | folder\_language\_name |
|:----------|:-----------|:-----------|:----------------|:-----------|:---------|:----------------------|:-----------|:-------------------------|:--------------------|:--------------------|:------------------|:----------------|-----------------:|------------------:|---------------:|----------------:|:--------------|:-----------------------|
| abk       | abkh1244   | abk        | Abkhazian       | Abkhaz     | language | vulnerable            | abkh1242   | Abkhaz-Adyge             | Northwest Caucasian | Northwest Caucasian | Eurasia           | Eurasia         |         43.05622 |          41.15911 |     43.0833333 |        41.00000 | Abkhaz\_abk   | Abkhaz                 |
| amp       | alam1246   | ala        | Alamblak        | Alamblak   | language | definitely endangered | sepi1257   | Sepik                    | Sepik Hill          | Sepik               | Papunesia         | Papunesia       |         -4.66307 |         143.31600 |     -4.6666667 |       143.33333 | Alamblak\_amp | Alamblak               |
| aey       | amel1241   | ame        | Amele           | Amele      | language | vulnerable            | nucl1709   | Nuclear Trans New Guinea | Madang              | Trans-New Guinea    | Papunesia         | Papunesia       |         -5.29126 |         145.68700 |     -5.2500000 |       145.58333 | Amele\_aey    | Amele                  |
| apu       | apur1254   | apu        | Apurinã         | Apurinã    | language | definitely endangered | araw1281   | Arawakan                 | Purus               | Arawakan            | South America     | South America   |         -8.21692 |         -66.77140 |     -9.0000000 |       -67.00000 | Apurina\_apu  | Apurina                |
| bmi       | bagi1246   | bag        | Bagirmi         | Bagirmi    | language | safe                  | cent2225   | Central Sudanic          | Bongo-Bagirmi       | Central Sudanic     | Africa            | Africa          |         11.52392 |          14.76949 |     11.6666667 |        16.00000 | Bagirmi\_bmi  | Bagirmi                |
| bsn       | bara1380   | brs        | Barasana-Eduria | Barasano   | language | definitely endangered | tuca1253   | Tucanoan                 | Tucanoan            | Tucanoan            | South America     | South America   |          0.02193 |         -70.80800 |     -0.1666667 |       -70.66667 | Barasano\_bsn | Barasano               |

Which languages in 100LC are covered by Epitran, a tool for
transliterating orthographic text as IPA:

-   <a href="https://pypi.org/project/epitran/" class="uri">https://pypi.org/project/epitran/</a>

Looks like 16 languages (but this depends on the script, which isn’t
indicated in the 100LC language info index):

    # This table was derived by hand from the project website above
    epitran <- read.csv('epitran_data.csv')

    table(index$iso639_3 %in% epitran$ISO6393) %>% kable()

| Var1  | Freq |
|:------|-----:|
| FALSE |   84 |
| TRUE  |   16 |

    epitran.lgs <- index[which(index$iso639_3 %in% epitran$ISO6393),] %>% select(iso639_3, name) %>% arrange(name)
    epitran.lgs %>% kable()

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

Which languages have grapheme-to-phoneme coverage in The World Writing
System Database
(<a href="https://agricolamz.github.io/wwsd/" class="uri">https://agricolamz.github.io/wwsd/</a>)?
What’s the overlap between the two sources? (Note: we’ll have to take
into account whether the scripts are the same.)

    # wwsd tables (TODO: update these URLs to point to the online resource once my PRs are merged)
    bib <- read.csv('~/Github/wwsd/bibliography.tsv', sep="\t", stringsAsFactors = FALSE)
    db <- read.csv('~/Github/wwsd/database.csv', stringsAsFactors = FALSE)

    table(index$glottocode %in% bib$glottocode) %>% kable()

| Var1  | Freq |
|:------|-----:|
| FALSE |   80 |
| TRUE  |   20 |

    wwsd.lgs <- index[which(index$glottocode %in% bib$glottocode),] %>% select(iso639_3, name)  %>% arrange(name)
    wwsd.lgs %>% kable()

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

    message('There are ', nrow(full_join(epitran.lgs, wwsd.lgs)), ' languages in both epitran and wwsd.')

    ## Joining, by = c("iso639_3", "name")

    ## There are 26 languages in both epitran and wwsd.

    full_join(epitran.lgs, wwsd.lgs) %>% arrange(name) %>% kable()

    ## Joining, by = c("iso639_3", "name")

| iso639\_3 | name                |
|:----------|:--------------------|
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

    message('There are ', nrow(inner_join(epitran.lgs, wwsd.lgs)), ' languages in both epitran and wwsd.')

    ## Joining, by = c("iso639_3", "name")

    ## There are 10 languages in both epitran and wwsd.

    inner_join(epitran.lgs, wwsd.lgs) %>% arrange(name) %>% kable()

    ## Joining, by = c("iso639_3", "name")

| iso639\_3 | name            |
|:----------|:----------------|
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

PHOIBLE coverage for potential NN models with phonetic features
---------------------------------------------------------------

First load PHOIBLE.

    phoible <- read_csv(url('https://github.com/phoible/dev/blob/master/data/phoible.csv?raw=true'), col_types = c(InventoryID='i', Marginal='l', .default='c'))

These are the languages available in the [SIGMORPHON g2p
task](https://sigmorphon.github.io/sharedtasks/2020/task1/):

-   Adyghe (ady)
-   Armenian (arm)
-   Bulgarian (bul)
-   Dutch (dut)
-   French (fre)
-   Georgian (geo)
-   Hindi (hin)
-   Hungarian (hun)
-   Icelandic (ice)
-   Japanese hiragana (jpn)
-   Korean (kor)
-   Lithuanian (lit)
-   Modern Greek (gre)
-   Romanian (rum)
-   Vietnamese (vie)

Are their phonological inventories all present in PHOIBLE? First, create
a vector of their ISO 639-3 codes for lookup. Note that the codes above
are ISO 639-2 and there are [some
discrepencies](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes),
e.g. “fre” vs “fra” for these languages:

-   Armenian (arm) -&gt; hye
-   Dutch (dut) -&gt; nld
-   French (fre) -&gt; fra
-   Georgian (geo) -&gt; kat
-   Icelandic (ice) -&gt; isl
-   Modern Greek (gre) -&gt; ell
-   Romanian (rum) -&gt; ron

So I update them accordingly.

    iso <- c('ady', 'hye', 'bul', 'nld', 'fra', 'kat', 'hin', 'hun', 'isl', 'jpn', 'kor', 'lit', 'ell', 'ron', 'vie')

Check against PHOIBLE. All languages have phoneme coverage.

    iso %in% phoible$ISO6393

    ##  [1] TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE TRUE

Let’s extract just those languages.

    task_lgs <- phoible %>% filter(ISO6393 %in% iso)

PHOIBLE can have more than one inventory for a particular language
(e.g. when two doculects describe the same language variety). How about
in this sample? Quite a bit.

    task_lgs %>% select(InventoryID, ISO6393) %>% distinct() %>% group_by(ISO6393) %>% summarize(inventories=n()) %>% kable()

    ## `summarise()` ungrouping output (override with `.groups` argument)

| ISO6393 | inventories |
|:--------|------------:|
| ady     |           1 |
| bul     |           4 |
| ell     |           5 |
| fra     |           4 |
| hin     |           5 |
| hun     |           4 |
| hye     |           2 |
| isl     |           2 |
| jpn     |           3 |
| kat     |           4 |
| kor     |           4 |
| lit     |           6 |
| nld     |           8 |
| ron     |           3 |
| vie     |           4 |

Let’s use `ady` as a test case.

    ady <- task_lgs %>% filter(ISO6393=="ady")

[Adyghe](https://en.wikipedia.org/wiki/Adyghe_language)
\[[adyg1241](https://glottolog.org/resource/languoid/id/adyg1241)\] is a
Northwest Caucasian language belong to the Circassian language family.

It’s phoneme inventory consists of:

    ady_phonemes <- ady %>% select(Phoneme)
    ady_phonemes %>% kable()

| Phoneme |
|:--------|
| b       |
| d       |
| dz      |
| dʑ      |
| d̠ʓʷ     |
| f       |
| h       |
| j       |
| k       |
| kʷ      |
| kʷʼ     |
| kʼ      |
| m       |
| n       |
| p       |
| pʷʼ     |
| pʼ      |
| q       |
| qʷ      |
| r       |
| s       |
| t       |
| ts      |
| tsʼ     |
| tɕ      |
| tɕʼ     |
| tʷʼ     |
| tʼ      |
| t̠ʃ      |
| t̠ʃʼ     |
| t̠ʆʷ     |
| w       |
| x       |
| xʷ      |
| z       |
| ɕ       |
| ɡʷ      |
| ɣ       |
| ɬ       |
| ɬʼ      |
| ɮ       |
| ʁ       |
| ʁʷ      |
| ʃ       |
| ʆ       |
| ʆʷ      |
| ʆʷʼ     |
| ʆʼ      |
| ʑ       |
| ʒ       |
| ʓ       |
| ʓʷ      |
| ʔʷʼ     |
| ʔʼ      |
| χ       |
| χʷ      |
| a       |
| e       |
| ə       |

The frequency of phonemes cross-lingustically in phoible is:

    freq <- phoible %>% select(Phoneme) %>% group_by(Phoneme) %>% summarize(count=n())

    ## `summarise()` ungrouping output (override with `.groups` argument)

    freq$frequency <- freq$count/nrow(freq)
    freq %>% arrange(desc(count)) %>% head() %>% kable()

| Phoneme | count | frequency |
|:--------|------:|----------:|
| m       |  2915 | 0.9210111 |
| i       |  2779 | 0.8780411 |
| k       |  2729 | 0.8622433 |
| j       |  2716 | 0.8581359 |
| u       |  2646 | 0.8360190 |
| a       |  2600 | 0.8214850 |

Let’s add this to the Adyghe data:

    ady_phonemes <- left_join(ady_phonemes, freq)

    ## Joining, by = "Phoneme"

    ady_phonemes %>% arrange(desc(count)) %>% kable()

| Phoneme | count | frequency |
|:--------|------:|----------:|
| m       |  2915 | 0.9210111 |
| k       |  2729 | 0.8622433 |
| j       |  2716 | 0.8581359 |
| a       |  2600 | 0.8214850 |
| p       |  2593 | 0.8192733 |
| w       |  2483 | 0.7845182 |
| n       |  2350 | 0.7424961 |
| t       |  2064 | 0.6521327 |
| s       |  2021 | 0.6385466 |
| b       |  1906 | 0.6022117 |
| e       |  1841 | 0.5816746 |
| h       |  1703 | 0.5380727 |
| d       |  1376 | 0.4347551 |
| r       |  1332 | 0.4208531 |
| f       |  1330 | 0.4202212 |
| t̠ʃ      |  1218 | 0.3848341 |
| ʃ       |  1104 | 0.3488152 |
| z       |   893 | 0.2821485 |
| ə       |   675 | 0.2132701 |
| ts      |   667 | 0.2107425 |
| x       |   574 | 0.1813586 |
| ʒ       |   478 | 0.1510269 |
| ɣ       |   436 | 0.1377567 |
| kʷ      |   372 | 0.1175355 |
| dz      |   312 | 0.0985782 |
| q       |   256 | 0.0808847 |
| kʼ      |   243 | 0.0767773 |
| χ       |   215 | 0.0679305 |
| ɡʷ      |   190 | 0.0600316 |
| t̠ʃʼ     |   185 | 0.0584518 |
| pʼ      |   179 | 0.0565561 |
| tʼ      |   157 | 0.0496051 |
| ʁ       |   155 | 0.0489731 |
| ɬ       |   149 | 0.0470774 |
| tsʼ     |   129 | 0.0407583 |
| tɕ      |   121 | 0.0382306 |
| ɕ       |   116 | 0.0366509 |
| kʷʼ     |    84 | 0.0265403 |
| dʑ      |    77 | 0.0243286 |
| xʷ      |    77 | 0.0243286 |
| ʑ       |    74 | 0.0233807 |
| χʷ      |    63 | 0.0199052 |
| qʷ      |    50 | 0.0157978 |
| ɮ       |    48 | 0.0151659 |
| ʁʷ      |    34 | 0.0107425 |
| ɬʼ      |     8 | 0.0025276 |
| tʷʼ     |     5 | 0.0015798 |
| ʆ       |     4 | 0.0012638 |
| ʓ       |     4 | 0.0012638 |
| d̠ʓʷ     |     3 | 0.0009479 |
| tɕʼ     |     3 | 0.0009479 |
| ʆʼ      |     3 | 0.0009479 |
| pʷʼ     |     2 | 0.0006319 |
| ʆʷ      |     2 | 0.0006319 |
| ʓʷ      |     2 | 0.0006319 |
| t̠ʆʷ     |     1 | 0.0003160 |
| ʆʷʼ     |     1 | 0.0003160 |
| ʔʷʼ     |     1 | 0.0003160 |
| ʔʼ      |     1 | 0.0003160 |

As shown, most phoneme occur in other languages.

For each phoneme, we can extract its features:

    ady %>% select(-1,-2,-3,-4,-5,-6,-8,-9,-11) %>% kable()

| Phoneme | SegmentClass | tone | stress | syllabic | short | long | consonantal | sonorant | continuant | delayedRelease | approximant | tap | trill | nasal | lateral | labial | round | labiodental | coronal | anterior | distributed | strident | dorsal | high | low | front | back | tense | retractedTongueRoot | advancedTongueRoot | periodicGlottalSource | epilaryngealSource | spreadGlottis | constrictedGlottis | fortis | raisedLarynxEjective | loweredLarynxImplosive | click |
|:--------|:-------------|:-----|:-------|:---------|:------|:-----|:------------|:---------|:-----------|:---------------|:------------|:----|:------|:------|:--------|:-------|:------|:------------|:--------|:---------|:------------|:---------|:-------|:-----|:----|:------|:-----|:------|:--------------------|:-------------------|:----------------------|:-------------------|:--------------|:-------------------|:-------|:---------------------|:-----------------------|:------|
| b       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \-    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| d       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| dz      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| dʑ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | -,+        | -,+            | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | -,+         | -,+      | -,+    | \+   | \-  | \+    | \-   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| d̠ʓʷ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | -,+        | -,+            | \-          | \-  | \-    | \-    | \-      | -,+    | \+    | \-          | \+      | +,-      | -,+         | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| f       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \-    | \+          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| h       | consonant    | 0    | \-     | \-       | \-    | \-   | \-          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \+            | \-                 | \-     | \-                   | \-                     | \-    |
| j       | consonant    | 0    | \-     | \-       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \+    | \-   | \+    | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| k       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| kʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| kʷʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| kʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| m       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \+       | \-         | 0              | \-          | \-  | \-    | \+    | \-      | \+     | \-    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| n       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \+       | \-         | 0              | \-          | \-  | \-    | \+    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| p       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \-    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| pʷʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| pʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \-    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| q       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| qʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| r       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \+       | \+         | 0              | \+          | \-  | \+    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| s       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| t       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ts      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| tsʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| tɕ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | -,+        | -,+            | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | -,+         | -,+      | -,+    | \+   | \-  | \+    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| tɕʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | -,+        | -,+            | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | -,+         | -,+      | -,+    | \+   | \-  | \+    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | -,+                | \-     | -,+                  | \-                     | \-    |
| tʷʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| tʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| t̠ʃ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| t̠ʃʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| t̠ʆʷ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | -,+        | -,+            | \-          | \-  | \-    | \-    | \-      | -,+    | \+    | \-          | \+      | +,-      | -,+         | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| w       | consonant    | 0    | \-     | \-       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \+   | \+    | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| x       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| xʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| z       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ɕ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \+          | \+       | \+     | \+   | \-  | \+    | \-   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ɡʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ɣ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \-    | \-   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ɬ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \+      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ɬʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \+      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| ɮ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \+      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʁ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʁʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʃ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʆ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʆʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʆʷʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| ʆʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| ʑ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \+          | \+       | \+     | \+   | \-  | \+    | \-   | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʒ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \+       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʓ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʓʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \+      | \-       | \+          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| ʔʷʼ     | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| ʔʼ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \+                 | \-     | \+                   | \-                     | \-    |
| χ       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| χʷ      | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \+         | \+             | \-          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| a       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \+  | \-    | \-   | 0     | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |
| e       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \+    | \-   | \+    | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |
| ə       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \-   | \-    | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |

And use these as input to our NN.

Another example would be something like extracting the features for
segments as per the Romanian example in the g2p task (see my notes in
OpenBIS):

-   antonim a n t o n i m

<!-- -->

    r_ex <- c('a', 'n', 't', 'o', 'n', 'i', 'm')
    r_ex <- unique(r_ex)
    phonemes <- phoible %>% select(-1,-2,-3,-4,-5,-6,-8,-9,-11) %>% distinct()
    phonemes %>% filter(Phoneme %in% r_ex) %>% kable()

| Phoneme | SegmentClass | tone | stress | syllabic | short | long | consonantal | sonorant | continuant | delayedRelease | approximant | tap | trill | nasal | lateral | labial | round | labiodental | coronal | anterior | distributed | strident | dorsal | high | low | front | back | tense | retractedTongueRoot | advancedTongueRoot | periodicGlottalSource | epilaryngealSource | spreadGlottis | constrictedGlottis | fortis | raisedLarynxEjective | loweredLarynxImplosive | click |
|:--------|:-------------|:-----|:-------|:---------|:------|:-----|:------------|:---------|:-----------|:---------------|:------------|:----|:------|:------|:--------|:-------|:------|:------------|:--------|:---------|:------------|:---------|:-------|:-----|:----|:------|:-----|:------|:--------------------|:-------------------|:----------------------|:-------------------|:--------------|:-------------------|:-------|:---------------------|:-----------------------|:------|
| m       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \+       | \-         | 0              | \-          | \-  | \-    | \+    | \-      | \+     | \-    | \-          | \-      | 0        | 0           | 0        | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| n       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \+       | \-         | 0              | \-          | \-  | \-    | \+    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \+                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| t       | consonant    | 0    | \-     | \-       | \-    | \-   | \+          | \-       | \-         | \-             | \-          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \+      | \+       | \-          | \-       | \-     | 0    | 0   | 0     | 0    | 0     | 0                   | 0                  | \-                    | \-                 | \-            | \-                 | \-     | \-                   | \-                     | \-    |
| a       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \-   | \+  | \-    | \-   | 0     | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |
| i       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \-     | 0     | 0           | \-      | 0        | 0           | 0        | \+     | \+   | \-  | \+    | \-   | \+    | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |
| o       | vowel        | 0    | \-     | \+       | \-    | \-   | \-          | \+       | \+         | 0              | \+          | \-  | \-    | \-    | \-      | \+     | \+    | \-          | \-      | 0        | 0           | 0        | \+     | \-   | \-  | \-    | \+   | \+    | \-                  | \-                 | \+                    | \-                 | \-            | \-                 | 0      | \-                   | \-                     | 0     |

    r_ex_phonemes <- phonemes %>% filter(Phoneme %in% r_ex)

Let’s take a subset for illustration purposes, since Romanian doesn’t
have clicks, etc.

    r_ex_phonemes %>% select(Phoneme, consonantal, sonorant, continuant, delayedRelease, nasal, labial, round) %>% kable()

| Phoneme | consonantal | sonorant | continuant | delayedRelease | nasal | labial | round |
|:--------|:------------|:---------|:-----------|:---------------|:------|:-------|:------|
| m       | \+          | \+       | \-         | 0              | \+    | \+     | \-    |
| n       | \+          | \+       | \-         | 0              | \+    | \-     | 0     |
| t       | \+          | \-       | \-         | \-             | \-    | \-     | 0     |
| a       | \-          | \+       | \+         | 0              | \-    | \-     | 0     |
| i       | \-          | \+       | \+         | 0              | \-    | \-     | 0     |
| o       | \-          | \+       | \+         | 0              | \-    | \+     | \+    |

Of course these features can also be combined in various ways to add
additional data on natural classes.
