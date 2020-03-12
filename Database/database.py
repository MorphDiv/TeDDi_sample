""" Database model for the 100 LC project """

import sys
import pathlib

import sqlalchemy as sa

from sqlalchemy import Text, Column, Integer, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import text

ENGINE = sa.create_engine('sqlite:///test.sqlite3', echo=False)


def create_all(engine=ENGINE):
    file = pathlib.Path(engine.url.database)
    if file.exists():
        file.unlink()
    Base.metadata.create_all(engine)


Base = declarative_base()

class Language(Base):
    """ Languages in the sample """
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)

    # Add language level metadata (see "langInfo_100LC.csv")
    # name = Column(text, unique=True, nullable=False) # https://github.com/glottolog/treedb/blob/master/treedb/models.py#L89
    # glottocode = Column(Text) # constraint on the code format, e.g. xxxx1234 https://github.com/glottolog/treedb/blob/master/treedb/models.py#L87
    # iso_639_3 = Column(Text) # https://github.com/glottolog/treedb/blob/master/treedb/models.py#L96
    # TODO: add FK one-to-n mapping with Corpus

class Corpus(Base):
    """ Collection of files """
    __tablename__ = 'corpus'
    id = sa.Column(Integer, primary_key=True)
    # corpus_id = Column(Integer, ForeignKey('language.id'))
    directory = Column(sa.Text, nullable=False)

class File(Base):
    """ Table for each text """
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id'))

    # These are the current metadata fields in each text
    language_name_wals = Column(sa.Text, nullable=False)
    language_name_glotto = Column(sa.Text, nullable=False)
    ISO_6393 = Column(sa.Text, nullable=False)
    year_composed = Column(sa.Text, nullable=False)
    year_published = Column(sa.Text, nullable=False)
    mode = Column(sa.Text, nullable=False)
    genre_broad = Column(sa.Text, nullable=False)
    genre_narrow = Column(sa.Text, nullable=False)
    writing_system = Column(sa.Text, nullable=False)
    special_characters = Column(sa.Text, nullable=False)
    short_description = Column(sa.Text, nullable=False)
    source = Column(sa.Text, nullable=False)
    copyright_short = Column(sa.Text, nullable=False)
    copyright_long = Column(sa.Text, nullable=False)
    sample_type = Column(sa.Text, nullable=False)
    comments = Column(sa.Text, nullable=False)

    # raw_text = Column(Text, CheckConstraint("raw_text != ''"), nullable=False) # The whole dump

def load(path='../Corpus/', engine=ENGINE):
    create_all(engine)
    with engine.begin() as conn:
        insert_corpus = sa.insert(Corpus, bind=conn).execute
        insert_file = sa.insert(File, bind=conn).execute

        for t in text.Text.from_rglob(path, "*.txt"):
            print(t)
            corpus_id, = insert_corpus(directory=str(t.filename.parent)).inserted_primary_key
            file_id, = insert_file(corpus_id=corpus_id, **t.metadata).inserted_primary_key


if __name__ == "__main__":
    load()