Get the bibliographic references encoded in the 100LC input files
================
Steven Moran
29 July, 2020

Load the `clc` package R library and generate a table of references per
file and per unique reference.

Note this package is a work in progress.

First load the 100LC RData object.

    # TODO: we should put this online somewhere because I can't get it to load as part of the clc package
    load('../../../clc/clc.RData')

    library(clc)

    ## Loading required package: tidyverse

    ## ── Attaching packages ─────────────────────────────────────────────────────────────────────────── tidyverse 1.3.0 ──

    ## ✓ ggplot2 3.3.2     ✓ purrr   0.3.4
    ## ✓ tibble  3.0.3     ✓ dplyr   1.0.0
    ## ✓ tidyr   1.1.0     ✓ stringr 1.4.0
    ## ✓ readr   1.3.1     ✓ forcats 0.5.0

    ## ── Conflicts ────────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

    ## Loading required package: tidytext

    library(knitr)
    library(readr)

Get the references from the 100LC `file` database table.

    references <- clc::get_references()

Let’s have a look at the results.

    references %>% head(n = 50) %>% kable()

| language\_name\_glotto | filename          | source                                                                                                                                                                      |
|:-----------------------|:------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Abkhazian              | abk\_pro\_1.txt   | <a href="https://unicode.org/udhr/d/udhr_abk.txt" class="uri">https://unicode.org/udhr/d/udhr_abk.txt</a> (30/01/2019)                                                      |
| Alamblak               | amp\_nfi\_1.txt   | <a href="http://pngscriptures.org/amp/copyright.htm" class="uri">http://pngscriptures.org/amp/copyright.htm</a>                                                             |
| Amele                  | aey\_nfi\_1.txt   | <a href="http://pngscriptures.org/aey/index.htm" class="uri">http://pngscriptures.org/aey/index.htm</a>                                                                     |
| Apurinã                | apu\_nfi\_1.txt   | <a href="http://www.scriptureearth.org/data/apu" class="uri">http://www.scriptureearth.org/data/apu</a>                                                                     |
| Bagirmi                | bmi\_gre\_1.txt   | Keegan, J. M., and Djibrine, M. I. (2016). Bagirmi lexicon, Bagirmi-French, French-Bagirmi, with grammatical introduction in English. Second Edition, Morkeg Books, Cuenca. |
| Barasana-Eduria        | bsn\_nfi\_1.txt   | <a href="http://www.scriptureearth.org/data/bsn" class="uri">http://www.scriptureearth.org/data/bsn</a>                                                                     |
| Basque                 | eus\_nfi\_1.txt   | <a href="https://www.bible.com/de/bible/56/gen.1.eab" class="uri">https://www.bible.com/de/bible/56/gen.1.eab</a>                                                           |
| Basque                 | eus\_nfi\_10.txt  | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_100.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_101.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_102.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_103.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_104.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_105.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_106.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_107.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_108.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_109.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_11.txt  | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_110.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_111.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_112.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_113.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_114.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_115.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_116.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_117.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_118.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_119.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_12.txt  | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_120.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_121.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_122.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_123.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_124.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_125.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_126.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_127.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_128.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_129.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_13.txt  | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_130.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_131.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_132.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_133.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_134.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_135.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_136.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_137.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                 | eus\_nfi\_138.txt | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |

Let’s write these to a CSV file for easier inspection.

    write_csv(references, 'files-references.csv')

Now we get the unique language name and their bibliographic sources for
corpora above, like Basque, which have lots of input text files from the
same source, e.g. Open Subtitles.

    unique.references <- references %>% select(language_name_glotto, source) %>% distinct()

This leaves us with 1010 observations instead of a row for each file in
the database.

    unique.references %>% head(n=20) %>% kable()

| language\_name\_glotto  | source                                                                                                                                                                      |
|:------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Abkhazian               | <a href="https://unicode.org/udhr/d/udhr_abk.txt" class="uri">https://unicode.org/udhr/d/udhr_abk.txt</a> (30/01/2019)                                                      |
| Alamblak                | <a href="http://pngscriptures.org/amp/copyright.htm" class="uri">http://pngscriptures.org/amp/copyright.htm</a>                                                             |
| Amele                   | <a href="http://pngscriptures.org/aey/index.htm" class="uri">http://pngscriptures.org/aey/index.htm</a>                                                                     |
| Apurinã                 | <a href="http://www.scriptureearth.org/data/apu" class="uri">http://www.scriptureearth.org/data/apu</a>                                                                     |
| Bagirmi                 | Keegan, J. M., and Djibrine, M. I. (2016). Bagirmi lexicon, Bagirmi-French, French-Bagirmi, with grammatical introduction in English. Second Edition, Morkeg Books, Cuenca. |
| Barasana-Eduria         | <a href="http://www.scriptureearth.org/data/bsn" class="uri">http://www.scriptureearth.org/data/bsn</a>                                                                     |
| Basque                  | <a href="https://www.bible.com/de/bible/56/gen.1.eab" class="uri">https://www.bible.com/de/bible/56/gen.1.eab</a>                                                           |
| Basque                  | <a href="https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip" class="uri">https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/raw/eu.zip</a>                   |
| Basque                  | <a href="https://unicode.org/udhr/d/udhr_eus.txt" class="uri">https://unicode.org/udhr/d/udhr_eus.txt</a> (30/01/2019)                                                      |
| Bukiyip                 | <a href="http://pngscriptures.org/ape/copyright.htm" class="uri">http://pngscriptures.org/ape/copyright.htm</a>                                                             |
| Burmese                 | <a href="https://www.bible.com/de/bible/404/gen.1.bcl" class="uri">https://www.bible.com/de/bible/404/gen.1.bcl</a>                                                         |
| Burmese                 | <a href="https://unicode.org/udhr/d/udhr_mya.txt" class="uri">https://unicode.org/udhr/d/udhr_mya.txt</a> (30/01/2019)                                                      |
| Burushaski              | Anderson, G. D. S., and Eggert, R. (2001). A typology of verb agreement in Burushaski. Linguistics of the Tibeto-Burman Area, Volume 24.2.                                  |
| Canela-Krahô            | <a href="https://scriptureearth.org/data/ram/PDF/00-PBram-web.pdf" class="uri">https://scriptureearth.org/data/ram/PDF/00-PBram-web.pdf</a>                                 |
| Central Moroccan Berber | <a href="https://unicode.org/udhr/d/udhr_tzm.txt" class="uri">https://unicode.org/udhr/d/udhr_tzm.txt</a> (30/01/2019)                                                      |
| Chamorro                | NA                                                                                                                                                                          |
| Chamorro                | <a href="https://unicode.org/udhr/d/udhr_cha.txt" class="uri">https://unicode.org/udhr/d/udhr_cha.txt</a> (30/01/2019)                                                      |
| Chukchi                 | <a href="http://ibtrussia.org/en/text" class="uri">http://ibtrussia.org/en/text</a> ?m=CHK                                                                                  |
| Copainalá Zoque         | Harrison, W. R. (1952). The Mason: A Zoque Text. Tlalocan, A Journal of Source Materials on the Native Cultures of Mexico, Volume III, Number 3, p. 193-204.                |
| Daga                    | <a href="http://pngscriptures.org/dgz/copyright.htm" class="uri">http://pngscriptures.org/dgz/copyright.htm</a>                                                             |

Let’s write these to CSV as well.

    write_csv(unique.references, 'sources-references.csv')

Upon visual inspection, we see that some files have no source.

    unique.references %>% filter(source == "NA")

    ##   language_name_glotto source
    ## 1             Chamorro     NA
    ## 2          Kalaallisut     NA

And others are quite limited in scope.

    unique.references %>% filter(language_name_glotto == "Wichita") %>% kable()

| language\_name\_glotto | source        |
|:-----------------------|:--------------|
| Wichita                | David S. Rood |

These should be udpated if they can, see:

-   <a href="https://github.com/uzling/100LC/issues/163" class="uri">https://github.com/uzling/100LC/issues/163</a>
