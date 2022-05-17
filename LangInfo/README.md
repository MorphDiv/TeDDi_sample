# LangInfo

## Data sources

This `langInfo_TeDDi.csv` file contains information on the languages of the WALS 100 language sample from both WALS and Glottolog 3.3. It was created by downloading the following files (which reside under the `Sources` directory):

* `Glottolog3.3/languages_and_dialects_geo.csv` - (Version 3.3, from https://glottolog.org/meta/downloads; accessed on 10/10/2018)
* `Glottolog3.3/glottolog_languoid.csv` - (Version 3.3, at https://glottolog.org/meta/downloads; accessed on 10/10/2018)   
* `WALS/Wals_languages.csv` - (WALS 2014, at https://wals.info/languoid by choosing the "tab" option for downloads; accessed on accessed on 10/10/2018)
* `UNESCO/unesco_atlas_languages_limited_dataset.ods` - UNESCO endangerement scale (http://www.unesco.org/languages-atlas/, accessed on 28/02/2019)

Wals_languages.csv was amended by removing the comma in "(West Papuan, Indonesia)" in order to enable saving it as a csv file. Also, four deprecated glottocodes were replaced: 

* old glottocode -> new glottocode
* huam1250 -> hmon1264
* kew1250 -> west2599
* slav1253 -> nort2942
* tuka1247 -> tuka1249

Note that WALS gives two ISO-639-3 codes for overall 6 languages in the 100 language sample. In cases where the difference is due to the existence of two varieties according to Glottolog, the first iso code represents both:

* bhq, khc -> Tukang Besi South, Tukang Besi North -> bhq 
* kew, kjs -> West Kewa, East Kewa -> kew
* scs, xsl -> North Slavey, South Slavey -> scs

In cases where one of the ISO codes is considered a "Bookkeeping" languoid by Glottolog (see https://glottolog.org/glottolog/glottologinformation for a definition), the other code is given:

* cqd, hnj -> hnj

In cases where one of the ISO codes is not registered with Glottolog, the other is given:

* ram, xra -> ram
* jac, jai -> jac

This leaves the number of languages defined by unique ISO-639-3 and glottocodes at 100.


## Rcode

The R code used to process and merge the three data files is given in `merge_sources.Rmd` script. The report produces a markdown file `merge_sources.md`, which can be view in the browser on GitHub.

Language status: The status of languages according to Glottolog was found to be erroneous in some cases (e.g. Russian and Modern Greek are endangered). The UNESCO endangerment was used instead. It was manually assigned under "status" for languages where it is available, "NA" was assigned otherwise. Note that this endangerement ranking does not include a category for safe languages. We assigned the status "safe" to large languages of which we definitely know at this point that they are safe (e.g. English, French, Swahili, Tagalog).


## Generating the index

It is important to note that the `langInfo_TeDDi.csv` is generated from the above mentioned sources, but it adds and populates the columns for:

* name
* folder_language_name

from the `Corpus` directory itself. This was requested because if data does not exists in a particular language folder, then that is clearly shown in the `langInfo_TeDDi.csv` index. In other words, for languages in TeDDi that do not yet have data, these two fields are "NA".

An issue arrises here, however, when running the `load-database.py` script in the `Database` directory on *new* data. For example, when adding Piraha data, the `load-database.py` script will correctly fail, e.g.:

```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: corpus.language_id
[SQL: INSERT INTO corpus (language_id, name, genre_broad, mode) VALUES (?, ?, ?, ?)]
[parameters: (None, 'Piraha_myp', 'non-fiction', 'spoken')]
(Background on this error at: http://sqlalche.me/e/13/gkpj)
```

if the `merge_sources.Rmd` script is not run first to populate the `name` and `folder_language_name` fields. Basically, the `load-database.py` pipeline goes to parse the new file(s), but sees in the `langInfo_TeDDi.csv` index that there is no `corpus.language_id` specified in the index (i.e. the `folder_language_name`). We could pre-populate the `langInfo_TeDDi.csv` by adding all folders to the `Corpus` directory, but then we would lack information about which languages are still to be added.

In sum, when adding *new* languages to the `Corpus` directory, run the `merge_sources.Rmd` script in this directory before running the `load-database.py` pipeline, or you will get the error above.

## Plot with WALS feature coverage

The script in `WALSChapterCoverage.Rmd' loads information on WALS features (`WALS_languages_chapters.csv'), and information on the TeDDi languages (`langInfo_TeDDi.csv'). These are merged to then calculate and plot the coverage (in percentages) of WALS features for the respective languages in the TeDDi sample. The `coverage.plot' is a barplot with the height of bars reflecting the coverage percentage. Additionally, a heatmap is generated with the presence/absence of each feature for a given language. 
