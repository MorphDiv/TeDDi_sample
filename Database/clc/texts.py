""" Text object for the TeDDi files """

import pathlib
import re

__all__ = ['Text']

ENCODING = 'utf-8'


class Text:

    @classmethod
    def from_rglob(cls, dir, glob):
        dir = pathlib.Path(dir)
        return map(cls.from_file, sorted(dir.rglob(glob)))

    @classmethod
    def from_file(cls, filepath):
        metadata = {}
        with filepath.open(encoding=ENCODING) as f:
            for line in f:
                if line.startswith("#"):
                    line = line[1:].strip()
                    key, sep, value = line.partition(":")
                    key, value = (x.strip() for x in (key, value))
                    assert key and sep
                    metadata[key] = value
                else:
                    break
            body = (line + f.read()).strip()
            # Fix files that have multiple tabs (from the crawlers)
            body = re.sub(r"\t+", "\t", body)
        return cls(filepath, metadata, body)

    @staticmethod
    def split_path(path):
        part_indexes = list(enumerate(path.parts))
        i = next((i for i, x in reversed(part_indexes) if x == 'Corpus'), None)
        parts = path.parts[i + 1:]
        corpus, genre_broad, *rest = parts
        if len(rest) == 1:
            mode = None
            filename, = rest
        elif len(rest) == 2:
            mode, filename = rest
        else:
            raise ValueError()
        return corpus, genre_broad, mode, filename

    def __init__(self, filepath, metadata, body):
        self.filepath = filepath
        self.metadata = metadata
        self.body = body
        self.corpus, self.genre_broad, self.mode, self.filename = self.split_path(self.filepath)

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.filepath)!r})'

    def to_file(self):
        with self.filepath.open("w", encoding=ENCODING) as f:
            for k, v in self.metadata.items():
                # If value is empty, replace it with the string "NA"
                if not v.strip():
                    v = "NA"
                # Rename and unify metadata categories
                k = k.replace("(", "")
                k = k.replace(")", "")
                k = k.replace("ISO_6393", "iso639_3")
                v = v.replace("face-to-face conversations", "face-to-face_conversations")
                v = v.replace("official documents", "official_documents")
                v = v.replace("oral tradition", "oral_tradition")
                v = v.replace("spontaneous speeches", "spontaneous_speeches")
                v = v.replace("written tradition", "written_tradition")
                f.write(f"# {k}:\t{v}\n")
            f.write(f"\n{self.body}")
