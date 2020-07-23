Generate word frequency counts per file
================
Steven Moran
23 July, 2020

Load the `clc` package R library (named this because R package names
cannot start with numbers).

TODO: work in progress.

``` r
library(clc)
```

    ## Loading required package: tidyverse

    ## ── Attaching packages ────────────────────────────────────────────────────────────────────────── tidyverse 1.3.0 ──

    ## ✓ ggplot2 3.3.2     ✓ purrr   0.3.4
    ## ✓ tibble  3.0.3     ✓ dplyr   1.0.0
    ## ✓ tidyr   1.1.0     ✓ stringr 1.4.0
    ## ✓ readr   1.3.1     ✓ forcats 0.5.0

    ## ── Conflicts ───────────────────────────────────────────────────────────────────────────── tidyverse_conflicts() ──
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

    ## Loading required package: tidytext

``` r
library(readr)
```

Get a list of file IDs from the 100LC database.

``` r
file_ids <- clc::get_file_ids()
```

Here’s an example of how to get the word count frequencies for one file.

``` r
# Get the word frequency counts
df <- clc::get_word_counts(file_ids[1])
# Look up the file name
filename <- clc::clc_file %>% filter(id == file_ids[1]) %>% select(filename)
# Strip its extension
filename <- sub('\\.txt$', '', filename)
# Write the results to CSV
readr::write_csv(df, paste0('csv/', filename, '_freq.csv'))
```

Loop through the file IDs, generate word frequency counts per file,
write the output to disk.

``` r
lapply(file_ids, function(i){
  df <- clc::get_word_counts(file_ids[i])
  filename <- clc::clc_file %>% filter(id == file_ids[i]) %>% select(filename)
  filename <- sub('\\.txt$', '', filename) 
  readr::write_csv(df, paste0('csv/', filename, '_freq.csv'))
})
```

Here’s an example of the output.

``` r
library(knitr)
df %>% head(n=50) %>% kable()
```

| word                 |  n | rank |
| :------------------- | -: | ---: |
| ауаҩы                | 45 |    1 |
| дарбанзаалак         | 36 |    2 |
| азин                 | 31 |    3 |
| иара                 | 30 |    4 |
| ахәҭаҷ               | 29 |    5 |
| имоуп                | 23 |    6 |
| ма                   | 18 |    7 |
| насгьы               | 11 |    8 |
| зегь                 |  9 |    9 |
| мамзаргьы            |  9 |   10 |
| изинқәа              |  8 |   11 |
| убас                 |  8 |   12 |
| ҳәа                  |  8 |   13 |
| азакәан              |  7 |   14 |
| азинқәеи             |  7 |   15 |
| азуа                 |  7 |   16 |
| ауаа                 |  7 |   17 |
| ахақәиҭрақәеи        |  7 |   18 |
| ихы                  |  7 |   19 |
| рзин                 |  7 |   20 |
| хшыҩзышьҭра          |  7 |   21 |
| абри                 |  6 |   22 |
| амилаҭқәа            |  6 |   23 |
| аҭаацәара            |  6 |   24 |
| зегьы                |  6 |   25 |
| аара                 |  5 |   26 |
| адунеижәларбжьаратәи |  5 |   27 |
| азы                  |  5 |   28 |
| аиура                |  5 |   29 |
| аус                  |  5 |   30 |
| еиҧш                 |  5 |   31 |
| изинқәеи             |  5 |   32 |
| имоу                 |  5 |   33 |
| ҟалом                |  5 |   34 |
| рзы                  |  5 |   35 |
| убасгьы              |  5 |   36 |
| абарҭ                |  4 |   37 |
| адекларациа          |  4 |   38 |
| ала                  |  4 |   39 |
| ауаажәларратә        |  4 |   40 |
| аҵара                |  4 |   41 |
| еиду                 |  4 |   42 |
| еиуеиҧшым            |  4 |   43 |
| иалахәу              |  4 |   44 |
| иарбан               |  4 |   45 |
| иҟоу                 |  4 |   46 |
| илшоит               |  4 |   47 |
| имазароуп            |  4 |   48 |
| ихадароу             |  4 |   49 |
| ҧсыхәа               |  4 |   50 |
