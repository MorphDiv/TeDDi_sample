Identify which languages in 100LC have multiple scripts
================
Steven Moran
25 October, 2020

    library(tidyverse)
    library(knitr)

Load the R serialized version of the 100LC database.

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

Write all the languages and their writing systems to a table, so that we
can use it in other reports, such as [creating maps](../maps/maps.md).

    langs_ws <- clc_file %>% select(language_name_wals, iso639_3, writing_system) %>% group_by(language_name_wals, writing_system) %>% distinct()
    write_csv(langs_ws, '100LC_writing_systems.csv')
