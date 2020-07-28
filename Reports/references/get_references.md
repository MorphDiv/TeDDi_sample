Get the bibliographic references encoded in the 100LC input files
================
Steven Moran
28 July, 2020

Load the `clc` package R library and generate a table of references per
file and per unique reference.

Note this package is a work in progress. For example, it currently only
loads the test version of the 100 LC database, i.e. `test.RData`. If you
want to run the `clc::get_references()` function on the entire dataset,
then you need to load the clc library (below) and then load the full
database into RStudio.

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

Get the references from the 100LC `file` database table.

    references <- clc::get_references()

So let’s write these to a CSV file for inspection.

    write_csv(references, 'files-references.csv')

Now we get the unique language name and their bibliographic sources for
corpora above, like Basque, which have lots of input text files from the
same source, e.g. Open Subtitles.

    unique.references <- references %>% select(language_name_glotto, source) %>% distinct()

This leaves us with 1010 observations instead of all files in the
database.

Let’s write these to CSV as well.

    write_csv(unique.references, 'sources-references.csv')
