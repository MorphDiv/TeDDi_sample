""" Text (body) object for the 100 LC files """

import sys
import pathlib
import text


class Body:

    @classmethod
    def clean(cls, text):
        text = text.splitlines()
        text = [l.strip() for l in text if l.strip() != ""]
        return cls(text)

    def __init__(self, text):
        self.text = text

    def __iter__(self):
        for line in self.text:
            # Base case (raw lines, no annotation)
            d = {"line_raw": line, "line": line}
            # Extended case (e.g. multi-level annotation)
            if line.__contains__("\t"):
                d = self._determine_file_type(d, line)
            yield d
        raise StopIteration()

    @staticmethod
    def _determine_file_type(d, line):
        label, s = line.split("\t")
        d["label"] = label
        d["line"] = s
        return d

if __name__ == "__main__":
    for t in text.Text.from_rglob('../Corpus/', "*.txt"):
        body = Body.clean(t.body)
        print(t)
        for i in body:
            print(i)

