""" Text (body) object for the 100 LC files """

# FIXME: cleanup/refactor (consider using subclasses)

import pathlib
import re

__all__ = ['Body']


class Body:

    @classmethod
    def load(cls, text):
        text = text.splitlines()
        text = [l.strip() for l in text]
        return cls(text)

    def get_records(self, text):
        # Return file type and records

        # TODO
        # return file_type, self._parse_transkribus(text)

        file_type = self._determine_file_type(text)
        if file_type == "PBC":
            return self._parse_pbc(text)
        elif file_type == "Grammar":
            return self._parse_grammar(text)
        elif file_type == "Bible":
            return self._parse_bible(text)
        elif file_type == "Transkribus":
            return self._parse_transkribus(text)
        elif file_type == "Text":
            return self._parse_text(text)
        else:
            raise ValueError("There is no file type for this file")

    @staticmethod
    def _determine_file_type(text):
        # Tabbed files
        if text[0].__contains__("\t"):
            tokens = text[0].split("\t")
            # PBC format contains and 8 digit number \t text
            if re.match(r"(\#)?(\d{8})", tokens[0]):
                return "PBC"
            # Hand-added grammars contain some number of annotation levels beginning with <line_1>
            if tokens[0].__contains__("line_1"):
                return "Grammar"
            raise ValueError("Line contains tab, but doesn't match PBC or Grammar format.")
        # Hand-added bibles
        elif text[0].__contains__("book_1"):
            return "Bible"
        # Transkripus created file
        elif text[0].__contains__("page_1"):
            return "Transkribus"
        # Plain text (Opensubtitles, UDHR, Gutenberg, etc.)
        else:
            return "Text"

    @staticmethod
    def _parse_text(text):
        # Text is simply free flowing text with no inherent structure and \n between "lines"
        text = [l.strip() for l in text if not l == ""]
        records = []
        for line in text:
            d = {}
            if line is None or line == "":
                raise ValueError("No None or empty values are allowed")
            d["text_raw"] = line
            d["text"] = line
            records.append(d)
        return records

    @staticmethod
    def _parse_pbc(text):
        # PBC should have an 8 digit passage number \t verse (but some verses may be missing)
        records = []
        for line in text:
            d = {}
            # Some lines are only the passage number without an text; just return all the same
            if not line.__contains__("\t"):
                d["text_raw"] = line.strip()
                d["label"] = line.strip()
                d["text"] = None
                records.append(d)
            else:
                key, value = line.split("\t")
                key, value = (x.strip() for x in (key, value))
                d["text_raw"] = line.strip()
                d["label"] = key
                d["text"] = value
                records.append(d)
        return records

    @staticmethod
    def _parse_bible(text):
        # Bible format appears in two files, is hand annotated, starts with title, etc., followed by tabbed passages
        text = [l.strip() for l in text if not l == ""]
        records = []
        for line in text:
            d = {}
            # Some lines are only page or chapter labels
            if not line.__contains__("\t"):
                d["text_raw"] = line.strip()
                d["label"] = line.strip()
                d["text"] = None
                records.append(d)
            else:
                key, value = line.split("\t")
                key, value = (x.strip() for x in (key, value))
                d["text_raw"] = line.strip()
                d["label"] = key
                d["text"] = value
                records.append(d)
        return records

    @staticmethod
    def _parse_transkribus(text):
        # Parse Transkribus format, i.e. <page_1> followed by <line_n> \n text
        text = [l.strip() for l in text if not l == ""]
        records = []
        for line in text:
            d = {}
            # Some lines are only page numbers
            if not line.__contains__("\t"):
                d["text_raw"] = line.strip()
                d["label"] = line.strip()
                d["text"] = None
                records.append(d)
            else:
                key, value = line.split("\t")
                key, value = (x.strip() for x in (key, value))
                d["text_raw"] = line.strip()
                d["label"] = key
                d["text"] = value
                records.append(d)
        return records

    @staticmethod
    def _get_chunks(text):
        # Chunk records by new line
        chunks = []
        temp = []
        for i in text:
            if not i == "":
                temp.append(i.strip())
            else:
                chunks.append(temp)
                temp = []
        return chunks

    def _parse_grammar(self, text):
        # Grammars are any set of interlinear glossed texts, each entry separated by \n, so we chunk them first
        chunks = self._get_chunks(text)
        records = []
        for c in chunks:
            d = {}
            for i in c:
                key, value = i.split("\t")
                key, value = (x.strip() for x in (key, value))

                # Populate line categories
                if key.__contains__("translation"):
                    d["translation"] = value
                if key.__contains__("footnote"):
                    d["footnote"] = value
                if key.__contains__("glossing"):
                    d["glossing"] = value
                if key.__contains__("segmentation"):
                    d["segmentation"] = value
                if key.__contains__("comment"):
                    d["comment"] = value
                if key.__contains__("phonological"):
                    d["phonological"] = value
                if key.__contains__("morphomic"):
                    d["morphomic"] = value
                if key.__contains__("line"):
                    d["text_raw"] = i
                    d["label"] = key
                    d["text"] = value
            records.append(d)
        return records

    def __init__(self, text):
        self.text = text
        # TODO
        # self.file_type, self.records = self.get_records(text)
        self.records = self.get_records(text)

    def __iter__(self):
        return iter(self.records)
