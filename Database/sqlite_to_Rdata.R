# Serialize normalized sqlite db to R data
# Steven Moran <steven.moran@uzh.ch>

# Set database file path
db.file <- 'full.sqlite3'

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
}

# The SQL query returns a normalized table as a data frame
df <- runsql('
SELECT 
line.id as line_id,
line.file_id,
corpus.id as corpus_id,
language.id as language_id,
line.text,
file.genre_broad as file_genre_broad,
file.genre_narrow as file_genre_narrow,
corpus.genre_broad,
corpus.genre_narrow,
language.name
FROM line
LEFT JOIN file ON line.file_id = file.id
LEFT JOIN corpus ON file.corpus_id = corpus.id
LEFT JOIN language on corpus.language_id = language.id;
')

# Save as a serialized Rdata object
save(df, file="100LC.Rdata")