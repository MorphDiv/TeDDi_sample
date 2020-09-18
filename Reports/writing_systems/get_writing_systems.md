Identify which languages in 100LC have multiple scripts
================
Steven Moran
15 September, 2020

    library(tidyverse)
    library(knitr)

Load the R serialized version of the 100 LC database.

    # load('../../Database/test.RData') # for testing
    load('../../Database/100LC.Rdata') # full database

Identify which languages have more than one writing system as indicated
in their files.

    langs_ws <- clc_file %>% select(language_name_wals, writing_system) %>% group_by(language_name_wals, writing_system) %>% distinct()
    langs_ws %>% group_by(language_name_wals) %>% filter(n() > 1) %>% kable()

| language\_name\_wals | writing\_system |
|:---------------------|:----------------|
| Hindi                | Deva            |
| Hindi                | Latn            |
| Khalkha              | Latn            |
| Khalkha              | Cyrl            |
| Korean               | Hang            |
| Korean               | Kore            |
| Mandarin             | Hans            |
| Mandarin             | Hant            |
| Vietnamese           | Latn            |
| Vietnamese           | Hani            |
