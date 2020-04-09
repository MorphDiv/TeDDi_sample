# Reports

## Overview

This directory contains short scientific data reports needed for monitoring the progress in building the 100LC corpus (for an example of a scientific data report workflow, see [A Reproducible Data Analysis Workflow with R Markdown, Git, Make, and Docker](https://psyarxiv.com/8xzqy/). 

We collect the report in this folder for the ease of browsing, access, and sharing. In particular, these reports should help us assess: 

* how much data still needs to be added in each of the target categories (e.g. for a particular language or genre)
* how large is each language sample in terms of corpus size (e.g. files, lines, tokens)

Future reports will be added to this directory and explained in detail below.


## Reports in this directory

### File counts

The [file_counts](file_counts) is an [R markdown](https://rmarkdown.rstudio.com/articles_intro.html) file that shows the number of corpus files per directory. The R markdown file can be produced by running  `knitr` in R Studio ([an example here](https://rmarkdown.rstudio.com/articles_integration.html)). The report in R markdown can be viewed in the browser because GitHub renders markdown (`md`) files. In addition to this, `knitr` produces a `CSV` file, written to the same directory as the R markdown report.

### Line counts

The [line_counts](line_counts) directory contains a Python script that loops through the corpus files and reports their number of lines and files per language per genre and outputs this data in a `CSV` file. This report can be produced by running the command line command `python line_counts.py`. The `CSV` file will be written to the same directory as the script. It also contains a R version that reads from the database and reports the number of lines, etc., to be compared with the Python script.

### Progress

The [progress](progress) directory contains a Python script that loops through the corpus files and reports the number of texts, genres covered, unique characters and number of tokens per language. 

### World maps

The [maps](maps) report is an [R markdown](https://rmarkdown.rstudio.com/articles_intro.html) report that produces world maps from the 100LC language sample. The R markdown report can be produced by running `knitr` in R Studio ([an example here](https://rmarkdown.rstudio.com/articles_integration.html)). The report can be viewed in the browser because GitHub renders markdown (`md`) files.
