# Dump RData as CSV

library(readr)

load('test.RData')

write_csv(clc_corpus, "corpus.csv")
write_csv(clc_file, "file.csv")
write_csv(clc_line, "line.csv")
write_csv(clc_language, "language.csv")