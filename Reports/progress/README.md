# Progress reports (pre-database)

These scripts should NOT be used for extracting any counts for analyses, but only as a means of tracking progress at the pre-database stage. They are Python scripts that run on the raw input text files in the [corpus](../../Corpus/) directory.

The [progress.py](progress.py) script loops through the corpus files and reports the number of: 

* texts
* genres covered
* unique characters per language

It returns zero values for languages that are not yet covered. (See also the [langInfo.csv](../../LangInfo/langInfo_100LC.csv) index file for more information.) 

The output format for [progress.py](progress.py) is a `CSV` file with the following columns:

* language
* number_texts
* number_genres
* number_characters

The output is saved in [progress.csv](progress.csv).

Note that the character counts from [progress.py](progress.py) do not distinguish between corpora that include different writing systems in the 100LC corpus. This is because files with different writing systems are not taken into account. For a report on which corpora have multiple writing systems, see [this report](../writing_systems/get_writing_systems.md).

The [line_counts.py](line_counts.py) script loops through the corpus files and reports the number of:

* total lines per corpus
* total files per corpus
* total lines per genre per corpus
* total files per genre per corpus

It writes the results to [line_counts.csv](line_counts.csv). A report of line and file counts that uses the database is provided in the [line counts report](../line_counts/line_counts.md), which also run a comparison with the results extracted in this directory.
