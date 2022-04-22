""" Generate TeDDi text files in Chris Bentz unified format. Make sure to create output/ directory. """

from clc import models as db
import sqlalchemy as sa

engine = None
conn = None


def setup():
    """Setup the sqlite DB connection."""
    url = "sqlite:///test.sqlite3"
    global engine, conn
    engine = sa.create_engine(url)
    conn = engine.connect()


def get_file_ids():
    """Return a list of file IDs."""
    q = sa.select([db.File.id]).order_by(db.File.id)
    query = conn.execute(q)
    file_ids = [row[0] for row in query]
    return file_ids


def get_metadata(id=1):
    """Select the metadata given a file ID."""
    q = sa.select([db.File.language_name_wals,
                    db.File.language_name_glotto,
                    db.File.iso639_3,
                    db.File.year_composed,
                    db.File.year_published,
                    db.File.mode,
                    db.File.genre_broad,
                    db.File.genre_narrow,
                    db.File.writing_system,
                    db.File.special_characters,
                    db.File.short_description,
                    db.File.source,
                    db.File.copyright_short,
                    db.File.copyright_long,
                    db.File.sample_type,
                    db.File.comments]).where(db.File.id==id)
    query = conn.execute(q)
    return query


def get_lines(id=1):
    """Select the lines in a file given a file ID."""
    q = sa.select([db.Line.text,
                   db.Line.glossing,
                   db.Line.phonological,
                   db.Line.translation,
                   db.Line.segmentation,
                   db.Line.morphomic,
                   db.Line.footnote,
                   db.Line.comment]).where(db.Line.file_id==id).order_by(db.Line.id)
    query = conn.execute(q)
    return query


def get_file_name(id=1):
    """ Return the filename."""
    q = sa.select([db.File.filename]).where(db.File.id==id).limit(1)
    query = conn.execute(q)
    filename = query.fetchone()
    return filename[0]


def output_metadata(query_results):
    """Convert the metadata query results to formatted a list."""
    results = []
    for row in query_results:
        results.append("# language_name_wals:"+"\t"+row.language_name_wals)
        results.append("# language_name_glotto:"+"\t"+row.language_name_glotto)
        results.append("# iso639_3:"+"\t"+row.iso639_3)
        results.append("# year_composed:"+"\t"+row.year_composed)
        results.append("# year_published:"+"\t"+row.year_published)
        results.append("# mode:"+"\t"+row.mode)
        results.append("# genre_broad:"+"\t"+row.genre_broad)
        results.append("# genre_narrow:"+"\t"+row.genre_narrow)
        results.append("# writing_system:"+"\t"+row.writing_system)
        results.append("# special_characters:"+"\t"+row.special_characters)
        results.append("# short_description:"+"\t"+row.short_description)
        results.append("# source:"+"\t"+row.source)
        results.append("# copyright_short:"+"\t"+row.copyright_short)
        results.append("# copyright_long:"+"\t"+row.copyright_long)
        results.append("# sample_type:"+"\t"+row.sample_type)
        results.append("# comments:"+"\t"+row.comments)
    return results


def output_lines(query_results):
    """Convert the lines query results to formatted a list."""
    line_id = 1
    footnote_id = 1
    results = []
    for row in query_results:
        line_break = False
        if row.text:
            results.append("<line_"+str(line_id)+">"+"\t"+row.text)
            line_id += 1
        if row.phonological:
            results.append("<phonological>" + "\t" + row.phonological)
            line_break = True
        if row.segmentation:
            results.append("<segmentation>" + "\t" + row.segmentation)
            line_break = True
        if row.morphomic:
            results.append("<morphomic>" + "\t" + row.morphomic)
            line_break = True
        if row.glossing:
            results.append("<glossing>" + "\t" + row.glossing)
            line_break = True
        if row.translation:
            results.append("<translation>" + "\t" + row.translation)
            line_break = True
        if row.footnote:
            results.append("<footnote_" + str(footnote_id) + ">" + "\t" + row.footnote)
            footnote_id += 1
            line_break = True
        if row.comment:
            results.append("<comment>" + "\t" + row.comment)
            line_break = True
        # If not just lines, add a line break between groups (sorry, hacky!)
        if line_break:
            results.append("\n")
    return results


def main():
    setup()
    file_ids = get_file_ids()

    for id in file_ids:
        filename = get_file_name(id)
        print(id, filename)

        query = get_metadata(id)
        metadata = output_metadata(query)

        query = get_lines(id)
        lines = output_lines(query)

        with open('output/'+filename, 'w') as f:
            for row in metadata:
                f.write(row+"\n")
            f.write("\n")
            for row in lines:
                f.write(row.strip()+"\n") # strip() removes extra line break between groups


if __name__ == "__main__":
    main()
