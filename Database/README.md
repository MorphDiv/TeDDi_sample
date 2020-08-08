# 100 LC database generation

## Generating the database

Scripts in this directory deal with generating the 100 LC database from the corpus text files and for converting the data to various formats.

For example, to parse the corpus files and to generate a [SQLite](https://www.sqlite.org/index.html) database, run:

`python3 load-database.py`

The default is set to development mode and will run the database creation pipeline on the in `tests/Corpus`, which contain all of the maximally diverse input file formats (for testing). This file then will generate a SQLite database called `test.sqlite3`.

To run the pipeline on the full database, set the `-f` (full database) flag:

`python3 load-database.py -f`

Beware this takes a few minutes to run on the 25k+ files in the `100LC/Corpus` directory. Note that the current full database is also nearly 3GB.

See `requirements.txt` for the required Python libraries for running the script. 

The actual processing for parsing the input data and generating the database is located in the directory `Database/clc` (named `clc` for "Centennial Language Corpus" because package names / libraries cannot start with numerals). The database schema is encoded in the `Database/clc/models.py` file. This file also contains the constraints on input, so if for example a new corpus file is added in which it contains an invalid value for a metadata field, an error will be thrown when generating the database, e.g.

`sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) CHECK constraint failed: file`

See for example pull request [183](https://github.com/uzling/100LC/pull/182) for details.


## Generating other formats

There are a few other scripts in this directory for generating various formats of the database. For example, to create an [RData](https://bookdown.org/ndphillips/YaRrr/rdata-files.html) from the SQLite database, run the R script:

`sqlite_to_RData.R`

To generate CSV files from the RData file, run:

`to_csv.R`

And to create corpus text files in a unified format, run:

`generate_unified_format.py`


## Other scripts

The `fix-files.py` script can be used to reformat the metadata headers in the `Corpus` files and to clean up aspects of the body.


## Errors

When adding *new* languages to the `Corpus` directory, run the `merge_sources.Rmd` script in that directory before running the `load-database.py` pipeline, or you will get the following error:

```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: corpus.language_id
[SQL: INSERT INTO corpus (language_id, name, genre_broad, mode) VALUES (?, ?, ?, ?)]
[parameters: (None, 'Piraha_myp', 'non-fiction', 'spoken')]
(Background on this error at: http://sqlalche.me/e/13/gkpj)
```

This is because the database generation pipeline needs as input the data in the `langInfo_100LC.csv` language index. For more information, see the README.md in the `100LC/LangInfo` directory.

