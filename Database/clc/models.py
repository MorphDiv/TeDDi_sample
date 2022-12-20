""" Database model for the TeDDi project """

import csv
import pathlib
import sys

import sqlalchemy as sa

from sqlalchemy import Text, String, Column, Integer, Float, Boolean, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from . import (texts as _texts,
               bodies as _bodies)

from . import CORPUS_ROOT

__all__ = ['load']

ENGINE = sa.create_engine('sqlite:///test.sqlite3', echo=False)


Model = declarative_base()


GENRE_BROAD = {'professional', 'non-fiction', 'conversation', 'grammar', 'fiction', 'technical'}

MODE = {'written', 'spoken', 'NA'}

GENRE_NARROW = {'official_documents', 'oral_tradition', 'religion', 'spontaneous_speeches', 'spoken', 'prepared_speeches', 'face-to-face_conversations', 'general_fiction', 'written_tradition', 'NA'}

MACROAREA = ('North America', 'South America', 'Eurasia', 'Africa', 'Australia', 'Papunesia')

ENDANGERMENT_STATUS = ('critically endangered', 'definitely endangered', 'extinct', 'safe', 'severely endangered', 'vulnerable')

# TODO: update these when we switch to Glottolog 4.x
# ENDANGERMENT_STATUS = {'not endangered', 'threatened', 'shifting', 'moribund', 'nearly extinct', 'extinct'}

SAMPLE_TYPE = {'whole', 'part'}


def create_all(engine=ENGINE, metadata=Model.metadata):
    file = pathlib.Path(engine.url.database)
    if file.exists():
        file.unlink()
    metadata.create_all(engine)


class Language(Model):
    """ Languages in the sample """

    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)

    # name = Column(text, unique=True, nullable=False) # https://github.com/glottolog/treedb/blob/master/treedb/models.py#L89
    name = Column(Text)
    iso639_3 = Column(String(3), CheckConstraint('length(iso639_3) = 3'), nullable=False)
    glottocode = Column(String(8), CheckConstraint('length(glottocode) = 8'), nullable=False)
    wals_code = Column(String(3), CheckConstraint('length(wals_code) = 3'), nullable=False)
    name_glotto = Column(Text, nullable=False)
    name_wals = Column(Text, nullable=False)
    level = Column(Text)
    status = Column(Enum(*sorted(ENDANGERMENT_STATUS)), nullable=False)
    family_id = Column(Text) # TODO: when None is inserted, set Glottocode constraint
    top_level_family = Column(Text)
    genus_wals = Column(Text, nullable=False)
    family_wals = Column(Text, nullable=False)
    macroarea_glotto = Column(Enum(*sorted(MACROAREA)), nullable=False)
    macroarea_wals = Column(Enum(*sorted(MACROAREA)), nullable=False)
    latitude_glotto = Column(Float, CheckConstraint('latitude_glotto BETWEEN -90 AND 90'), nullable=False)
    longitude_glotto = Column(Float, CheckConstraint('longitude_glotto BETWEEN -180 AND 180'), nullable=False)
    latitude_wals = Column(Float, CheckConstraint('latitude_wals BETWEEN -90 AND 90'), nullable=False)
    longitude_wals = Column(Float, CheckConstraint('longitude_wals BETWEEN -180 AND 180'), nullable=False)
    folder_language_name = Column(Text)


class Corpus(Model):
    """ Collection of files """

    __tablename__ = 'corpus'

    id = sa.Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey('language.id'), nullable=False)
    name = Column(String, CheckConstraint("name != ''"), nullable=False)

    # These fields are taken directly from the corpus directory structure
    genre_broad = Column(Enum(*sorted(GENRE_BROAD)), nullable=False)
    mode = Column(Enum(*sorted(MODE)))


class File(Model):
    """ Table for each text """

    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    corpus_id = Column(Integer, ForeignKey('corpus.id'), nullable=False)
    filename = Column(sa.Text, nullable=False)

    # These are the current metadata fields in each text
    language_name_wals = Column(sa.Text, nullable=False)
    language_name_glotto = Column(sa.Text, nullable=False)
    iso639_3 = Column(String(3), CheckConstraint('length(iso639_3) = 3'), nullable=False)
    year_composed = Column(sa.Text, nullable=False)
    year_published = Column(sa.Text, nullable=False)
    mode = Column(Enum(*sorted(MODE)), nullable=False)
    genre_broad = Column(Enum(*sorted(GENRE_BROAD)), nullable=False)
    genre_narrow =  Column(Enum(*sorted(GENRE_NARROW)))
    writing_system = Column(String(4), CheckConstraint('length(writing_system) = 4'), nullable=False)
    special_characters = Column(sa.Text, nullable=False)
    short_description = Column(sa.Text, nullable=False)
    source = Column(sa.Text, nullable=False)
    copyright_short = Column(sa.Text, nullable=False)
    copyright_long = Column(sa.Text, nullable=False)
    sample_type = Column(Enum(*sorted(SAMPLE_TYPE)), nullable=False)
    comments = Column(sa.Text, nullable=False)


class Line(Model):
    """ Table for each line """

    __tablename__ = 'line'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('file.id'), nullable=False)
    text_raw = Column(sa.Text, nullable=False)
    label = Column(sa.Text)
    text = Column(sa.Text)
    translation = Column(sa.Text)
    glossing = Column(sa.Text)
    segmentation = Column(sa.Text)
    phonological = Column(sa.Text)
    morphomic = Column(sa.Text)
    comment = Column(sa.Text)
    footnote = Column(sa.Text)


def load(path=CORPUS_ROOT, engine=ENGINE):
    create_all(engine)
    with engine.begin() as conn:
        select_language_id = sa.select([Language.id], bind=conn)\
            .where(Language.name == sa.bindparam('name')).scalar
        insert_language = sa.insert(Language, bind=conn).execute
        insert_corpus = sa.insert(Corpus, bind=conn).execute
        insert_file = sa.insert(File, bind=conn).execute
        insert_line = sa.insert(Line, bind=conn).execute

        class CorpusMap(dict):

            @staticmethod
            def params_to_key(params):
                return tuple(sorted(params.items()))

            def __missing__(self, key):
                params = dict(key)
                corpus_id, = insert_corpus(**params).inserted_primary_key
                self[key] = corpus_id
                return corpus_id

        corpus_map = CorpusMap()

        with open('../LangInfo/langInfo_TeDDi.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # R writes 'NA' for NULL; here we switch it to Python None, so that it is inserted NULL in SQL
                for k, v in row.items():
                    if v == 'NA':
                        row[k] = None
                insert_language(**row)

        # TODO: fix denylist
        #denylist = ['crk_nfi_1']
        denylist = []

        for t in _texts.Text.from_rglob(path, "*.txt"):
            # TODO: remove denylist
            if any(bad_file in str(t.filename) for bad_file in denylist):
                continue

            print(t)

            # Look up the language name and get id to assign to corpus foreign key
            language_id = select_language_id(name=t.corpus)

            # Create the dictionary of values for the corpus table
            corpus_path_metadata = dict(language_id=language_id, name=t.corpus, genre_broad=t.genre_broad,
                                        mode=t.mode)

            # Insert only non-duplicated corpus entries
            params = corpus_map.params_to_key(corpus_path_metadata)
            corpus_id = corpus_map[params]

            # Insert file metadata and then loop through lines in the file and insert
            file_id, = insert_file(corpus_id=corpus_id, filename=t.filename, **t.metadata).inserted_primary_key
            for line in _bodies.Body.load(t.body):
                line_id = insert_line(file_id=file_id, **line).inserted_primary_key
