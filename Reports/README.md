# Reports

## Overview

This directory contains short scientific data reports using the 100LC corpus data. A data science report is explains some type of data analysis and are used to share results of that analysis.

This folder is needed to collect these reports into a single directory in our repository for easy browsing, access, sharing. We produce these reports so that we have an idea of, for example:

* how much data still needs to be added to our language sample
* how large is each language sample in terms of corpus size (e.g. files, lines, tokens)

Future reports will be added to this directory and explained in detail below.


## Reports in this directory

### File counts

The [file_counts](file_counts) report is an [R markdown](https://rmarkdown.rstudio.com/articles_intro.html) report that reports the number of corpus files per directory. The R markdown report can be produced by running  `knitr` in R Studio ([an example here](https://rmarkdown.rstudio.com/articles_integration.html)). The report can be viewed in the browser because GitHub renders markdown (`md`) files. A `CSV` file of the counts is also written to the same directory as the report.

### Line counts

The [line_counts](line_counts) is a Python script that loops through the corpus files and reports their number of lines and files per language per genre and outputs this data in a `CSV` file. This report can be produced by running the command line command `python line_counts.py`. The `CSV` file will be written to the same directory as the script.


### World maps

The [maps](maps) report is an [R markdown](https://rmarkdown.rstudio.com/articles_intro.html) report that produces world maps from the 100LC language sample. The R markdown report can be produced by running  `knitr` in R Studio ([an example here](https://rmarkdown.rstudio.com/articles_integration.html)). The report can be viewed in the browser because GitHub renders markdown (`md`) files.


