"""
Postprocessing of the files crawled from Gutenberg and OpenSubtitles:
    Fixes meta (tab after each tag; replace multiple tabs and spaces)
    Fixes broken lines in meta
    Replaces tabs and spaces to a single space in body

"""

import os
import re
import codecs


root_path = '../Corpus'

for root, dirs, files in os.walk(root_path):
    for file in files:
        with codecs.open(os.path.join(root, file), 'r', 'utf-8') as f:
            text = f.readlines()
            fixed_text = []

            # Change only crawled from Gutenberg and OpenSubtitles
            if 'gutenberg' in text[12] or 'gutenberg' in text[14] \
                    or 'opensubtitles' in text[12]:
                print(file)
                i = 0
                while i < len(text):
                    line = text[i]
                    if line.startswith('#'):

                        # Replace space(s) to a single tab in meta
                        line = re.sub('(.*?): +', '\\g<1>:\t', line)

                        # Replace multiple tabs to a single tab in meta
                        line = re.sub('\t{2,}', '\t', line)

                        # Fix broken lines
                        if 'short_description' in line:
                            if not text[i+1].startswith('#'):
                                j = 1
                                line = text[i].strip()
                                while not text[i+j].startswith('#'):
                                    if text[i+j] == '\n':
                                        line += ','
                                    else:
                                        line += ' ' + text[i+j].strip()
                                    j += 1

                                line += '\n'
                                i += j-1

                        # Replace tab in copyright_long (OpenSubtitles)
                        line = re.sub('\t+Extracting', ' Extracting', line)

                        # Replace multiple spaces
                        line = re.sub(' {2,}', ' ', line)
                        fixed_text.append(line)

                    else:

                        # Replace tabs and multiple spaces in body to a single space
                        line = re.sub('[ \t]+', ' ', line)
                        fixed_text.append(line)

                    i += 1

                with codecs.open(os.path.join(root, file), 'w', 'utf-8') as fixed_f:
                    for line in fixed_text:
                        fixed_f.write(line)

