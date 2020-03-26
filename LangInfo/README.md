# LangInfo

## Data sources

This `langInfo_100LC.csv` file contains information on the languages of the WALS 100 language sample from both WALS and Glottolog 3.3. It was created by downloading the following files (which reside under the `Sources` directory):

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





