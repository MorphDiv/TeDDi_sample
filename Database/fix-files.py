""" Fix the formatting of the corpus files."""

import clc


for t in clc.Text.from_rglob(clc.TEST_ROOT, '*.txt'):
    print(t)
    t.to_file()
