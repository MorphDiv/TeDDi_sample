""" Text object for the 100 LC files """

import re
import pathlib

ENCODING = "UTF-8"

class Text:

    @classmethod
    def from_rglob(cls, dir, glob):
        dir = pathlib.Path(dir)
        return map(cls.from_file, sorted(dir.rglob(glob)))

    @classmethod
    def from_file(cls, filename):
        metadata = {}
        with filename.open(encoding=ENCODING) as f:
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
        return cls(filename, metadata, body)

    def __init__(self, filename, metadata, body):
        self.filename = filename
        self.metadata = metadata
        self.body = body

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self.filename)!r})'

    def to_file(self):
        with self.filename.open("w", encoding=ENCODING) as f:
            for k, v in self.metadata.items():
                # If value is empty, replace it with the string "NA"
                if not v.strip():
                    v = "NA"
                # Remove parentheses and minus symbol in metadata keys
                k = k.replace("(", "")
                k = k.replace(")", "")
                k = k.replace("ISO_639-3", "ISO_6393")
                f.write(f"# {k}:\t{v}\n")
            f.write(f"\n{self.body}")
