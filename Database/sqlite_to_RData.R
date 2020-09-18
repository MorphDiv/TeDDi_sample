# Query 100 LC SQLite database tables and serialize them to an RData file
# Steven Moran <steven.moran@uzh.ch>
# Command line usage: `Rscript sqlite_to_RData.R`

# First set database file path (default to test database)
db.file <- 'test.sqlite3'
# db.file <- 'full.sqlite3'

# Query the database and return a dataframe
runsql <- function(sql, dbname=db.file){
  require(RSQLite)
  driver <- dbDriver("SQLite")
  connect <- dbConnect(driver, dbname=dbname);
  closeup <- function(){
    sqliteCloseConnection(connect)
    sqliteCloseDriver(driver)
  }
  dd <- tryCatch(dbGetQuery(connect, sql), finally=closeup)
  return(dd)
  dbDisconnect()
}

# Query each table and store as a dataframe (we prefix each with `clc` because `file` and `lines` are functions in base R)
clc_corpus <- runsql('SELECT * FROM corpus')
clc_file <- runsql('SELECT * FROM file')
clc_language <- runsql('SELECT * FROM language')
clc_line <- runsql('SELECT * FROM line')

# Save as a serialized Rdata object (default test data)
save(clc_corpus, clc_file, clc_language, clc_line, file="test.RData")
# save(clc_corpus, clc_file, clc_language, clc_line, file="100LC.RData")


################
# The SQL query returns a de-normalized table as a data frame
# 
# df <- runsql('
#              SELECT 
#              line.id as line_id,
#              line.file_id,
#              corpus.id as corpus_id,
#              language.id as language_id,
#              line.text,
#              file.genre_broad as file_genre_broad,
#              file.genre_narrow as file_genre_narrow,
#              corpus.genre_broad,
#              corpus.genre_narrow,
#              language.name
#              FROM line
#              LEFT JOIN file ON line.file_id = file.id
#              LEFT JOIN corpus ON file.corpus_id = corpus.id
#              LEFT JOIN language on corpus.language_id = language.id;
#              ')
