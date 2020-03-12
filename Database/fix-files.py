""" Fix the formatting of the corpus files  """

import text

for text in text.Text.from_rglob('../Corpus/', "*.txt"):
    print(text)
    text.to_file()
