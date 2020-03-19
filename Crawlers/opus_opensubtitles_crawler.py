# -*- coding: utf-8 -*-

# Crawler for OPUS OpenSubtitles
# Gathers *.zip files, samples from them, stores *.txt and *.xml
# 100 samples
# 50 000 tokens per sample
# if a text has less than 50 000 tokens -> take the whole text

# Dealing with duplicates:
# 1) Go through the files' tree with the step 2 (skip one file)
# 2) In addition to that, check first 50 lines of the current file with all the others downloaded before,
# if >20 lines are the same, then skip the file

import codecs
import random
import shutil
import ssl
import time
import zipfile
from string import punctuation

import os
import re
import requests
import urllib3
from lxml import etree
from nltk.tokenize import word_tokenize as nltk_tokenize
from pythainlp import word_tokenize as thai_tokenize
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
from wordfreq import tokenize

import nltk
nltk.download('punkt')

report = codecs.open('report_subtitles.csv', 'a', 'utf-8')
report.write('folder_name;tokens;txt_files\n')

total_tokens = 0
first_counter = 0

# OPUS code : folder name, iso, name_wals, name_glotto
lang_dic = {
    'eu': ['Basque_eus', 'eus', 'Basque', 'Basque', 'Latn'],
    'en': ['English_eng', 'eng', 'English', 'English', 'Latn'],
    'fi': ['Finnish_fin', 'fin', 'Finnish', 'Finnish', 'Latn'],
    'fr': ['French_fra', 'fra', 'French', 'French', 'Latn'],
    'ka': ['Georgian_kat', 'kat', 'Georgian', 'Georgian', 'Geor'],
    'de': ['German_deu', 'deu', 'German', 'German', 'Latn'],
    'el': ['Greek_Modern_ell', 'ell', 'Greek (Modern)', 'Modern Greek', 'Grek'],
    'he': ['Hebrew_Modern_heb', 'heb', 'Hebrew (Modern)', 'Modern Hebrew', 'Hebr'],
    'hi': ['Hindi_hin', 'hin', 'Hindi', 'Hindi', 'Deva'],
    'id': ['Indonesian_ind', 'ind', 'Indonesian', 'Indonesian', 'Latn'],
    'ja': ['Japanese_jpn', 'jpn', 'Japanese', 'Japanese', 'Jpan'],
    'ko': ['Korean_kor', 'kor', 'Korean', 'Korean', 'Kore'],
    'zh': ['Mandarin_cmn', 'cmn', 'Mandarin', 'Mandarin Chinese', 'Hans'],
    'fa': ['Persian_pes', 'pes', 'Persian', 'Western Farsi', 'Arab'],
    'ru': ['Russian_rus', 'rus', 'Russian', 'Russian', 'Cyrl'],
    'es': ['Spanish_spa', 'spa', 'Spanish', 'Spanish', 'Latn'],
    'sw': ['Swahili_swh', 'swh', 'Swahili', 'Swahili', 'Latn'],
    'tl': ['Tagalog_tgl', 'tgl', 'Tagalog', 'Tagalog', 'Latn'],
    'th': ['Thai_tha', 'tha', 'Thai', 'Thai', 'Thai'],
    'tr': ['Turkish_tur', 'tur', 'Turkish', 'Turkish', 'Latn'],
    'vi': ['Vietnamese_vie', 'vie', 'Vietnamese', 'Vietnamese', 'Latn']
}


# Root path
def get_root(lang):
    return '../Corpus/' + lang_dic[lang][0] + '/non-fiction/written/'


# Request HTML page for the current language
def request(language):
    r = requests.get('http://opus.nlpl.eu/opusapi', params={'corpus': 'OpenSubtitles',
                                                            'source': language,
                                                            'target': 'any',
                                                            'preprocessing': 'raw'})
    html = r.json()
    return html


# Find link to the *.zip with OpenSubtitles, the newest version possible
def find_link(language, html):
    if len(html['corpora']) > 1:
        link = html['corpora'][-1]['url']
    else:
        link = html['corpora'][0]['url']

    if link is None:
        return 'No subtitles for the language ' + language
    else:
        return link


# Get request to obtain *.zip files
def get_file(url, fname):
    try:
        http = urllib3.PoolManager()
    except (Timeout, ssl.SSLError, ReadTimeoutError, ConnectionError):
        time.sleep(30)
        http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False, headers={'User-Agent': 'Mozilla/5.0'})
    cur_chunk = 16 * 1024
    with open(fname, 'wb') as fp:
        while True:
            chunk = r.read(cur_chunk)
            if not chunk:
                break
            fp.write(chunk)
    r.release_conn()


# Unzip file
def unzip_file(fname_zip, root):
    print(fname_zip)
    zip_ref = zipfile.ZipFile(fname_zip, 'r')
    zip_ref.extractall(root)
    zip_ref.close()
    os.remove(fname_zip)


# Search xmls
def search_xmls(lang, link):
    path = get_root(lang) + 'OpenSubtitles/raw/' + lang
    current_counter = 0
    total_tokens = 0
    skip_counter = 0

    for root, dirs, files in os.walk(path):
        for dirname in sorted(dirs, reverse=True):
            for files in os.walk(os.path.join(root, dirname)):
                if len(files[2]) > 0:
                    for f in files[2]:
                        if skip_counter % 2 == 0:
                            if total_tokens <= 5000000:
                                if get_text(os.path.join(files[0], f), lang) is not False:
                                    text, year, tokens = get_text(os.path.join(files[0], f), lang)

                                    total_tokens, current_counter, fname = sample(link, text, year, tokens, lang,
                                                                                  current_counter, total_tokens)

                                    if fname != '':
                                        skip_flag = check_duplicates(lang, fname)

                                        if skip_flag:
                                            text = codecs.open(fname, 'r', 'utf-8').read()
                                            os.remove(fname)
                                            print('Removed ' + fname)
                                            total_tokens -= count_tokens(text, lang)

                                        # rename all the files afterwards
                                        print('Total tokens: ', total_tokens)
                                        os.remove(os.path.join(files[0], f))

                                    else:
                                        print('Skipped file because there is more than 50 000 tokens')

                        skip_counter += 1

    return total_tokens, current_counter


# Remove initials xmls
def remove_xmls(lang):
    path = get_root(lang) + 'OpenSubtitles'
    shutil.rmtree(path)
    os.remove(get_root(lang) + 'INFO')
    os.remove(get_root(lang) + 'LICENSE')
    os.remove(get_root(lang) + 'README')


# Retrieve text
def get_text(fname, lang):
    f = codecs.open(fname, 'r', 'utf-8')
    print(fname)
    xml = f.read().encode('utf-8')
    parser = etree.XMLParser(encoding='utf-8')
    try:
        tree = etree.XML(xml, parser)
    except etree.XMLSyntaxError:
        return False
    text = ''
    year = 'NA'
    search_time = re.compile('/>([.\\s\\S]+?)<', re.UNICODE)
    for el in tree:
        if el.tag == 's':
            line = etree.tostring(el, encoding='unicode')

            time_str = re.search(search_time, line)
            if time_str is not None:
                time_str_result = time_str.group(1).strip()
                if time_str_result != '&amp;nbsp;':
                    text += time_str_result
                    text += '\n'

        if el.tag == 'meta':
            for child in el:
                if child.tag == 'source':
                    for c in child:
                        if c.tag == 'year':
                            year = c.text
                            print('Year: ', year)

    tokens = count_tokens(text, lang)

    return text, year, tokens


# Compare texts
def compare_texts(current_text, text):
    lines1 = current_text.split('\n')
    lines2 = text.split('\n')

    if min(len(lines1), len(lines2)) < 50:
        min_length = min(len(lines1), len(lines2))
    else:
        min_length = 50

    same_lines = []

    k = 0
    while k < min_length:
        if lines1[k] == lines2[k] and not lines1[k].startswith('#') and lines1[k] != '\n' and lines1[k] != '':
            same_lines.append(lines1[k])

        k += 1

    return len(same_lines)


def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


# Check for duplicates
def check_duplicates(lang, fname):
    skip_flag = False

    folder = get_root(lang)

    if len(os.listdir(folder)) > 1:
        for filename in os.listdir(folder):
            path_filename = os.path.join(folder, filename)
            if fname != path_filename and path_filename.endswith('txt'):

                text = u''
                f = codecs.open(path_filename, 'r', 'utf-8')
                for line in f:
                    text += line

                current_text = u''
                f = codecs.open(fname, 'r', 'utf-8')
                for line in f:
                    current_text += line

                number_same_lines = compare_texts(current_text, text)

                if number_same_lines > 20:
                    print('Current: ', fname)
                    print('Filename: ', path_filename)
                    print('Number of the same lines: ', number_same_lines)
                    skip_flag = True
                    return skip_flag

    return skip_flag


# Generate file name
def generate_fname(lang, current_counter):
    path = get_root(lang)
    max_counter = 0
    search_fcounter = re.compile(lang_dic[lang][1] + '_nfi_' + '([0-9]+)(\\.txt)?')
    for root, dirs, files in os.walk(path):
        for fname in files:
            fcounter = re.search(search_fcounter, fname)
            if fcounter is not None:
                if int(fcounter.group(1)) > max_counter:
                    current_counter = fcounter.group(1)
                    max_counter = int(current_counter)
            else:
                current_counter = 0
    if max_counter > 0:
        current_counter = max_counter
    fname = lang_dic[lang][1] + '_nfi_' + str(int(current_counter) + 1) + '.txt'
    print(get_root(lang) + fname)
    return (get_root(lang) + fname), current_counter


# Tokenization
def count_tokens(text, lang):
    if lang in ['en', 'fi', 'fr', 'de', 'el', 'he', 'hi', 'id', 'ja', 'ko', 'zh', 'fa', 'ru', 'es', 'tr']:
        tokens = tokenize(text, lang)
    elif lang == 'th':
        tokens = thai_tokenize(text)
    else:
        tokens = nltk_tokenize(text)

    tokens = [word.lower() for word in tokens
              if not (word in punctuation and not word.isdigit() and not word.isspace())]

    print('Number of tokens: ', len(tokens))

    return len(tokens)


def define_line_start(arr_text, tokens, lang, token_start):
    max_range = tokens - 50001
    random_range = []
    for i in range(len(arr_text) - 1):
        print(arr_text[i])
        if token_start <= max_range:
            if arr_text[i][-1] == '?':
                line_start = i
                token_start += count_tokens(arr_text[i], lang)
                random_range.append(line_start)
            token_start += count_tokens(arr_text[i], lang)
    line_start = random.choice(random_range)
    return line_start


# Random starting point
def starting_point(arr_text, tokens, lang):
    token_start = 0
    if tokens < 100001:
        line_start = define_line_start(arr_text, tokens, lang, token_start)
        return line_start
    else:
        return 0


# Sample
def sample(link, text, year, tokens, lang, current_counter, total_tokens):
    fname, current_counter = generate_fname(lang, current_counter)
    if int(tokens) <= 50000:
        f1 = codecs.open(fname, 'w', 'utf-8')
        meta = '''# language_name_wals:	''' + lang_dic[lang][2] + '''
# language_name_glotto:	''' + lang_dic[lang][3] + '''
# ISO_639-3:	''' + lang_dic[lang][1] + '''
# year_composed:	NA
# year_published:	''' + year + '''
# mode:	written
# genre_(broad):	non-fiction
# genre_(narrow):	prepared_speeches
# writing_system:	''' + lang_dic[lang][4] + '''
# special_characters:	NA
# short_description:	OpenSubtitles2018
# source:	''' + link + '''
# copyright_short:	http://www.opensubtitles.org/
# copyright_long:	http://www.opensubtitles.org/ P. Lison and J. Tiedemann, 2016, OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016)
# sample_type:	whole
# comments:	NA

'''
        meta = re.sub('\t{2,}', '\t', meta)
        f1.write(meta)

        text = re.sub('\t+', ' ', text)
        f1.write(text[:-1])
        total_tokens += int(tokens)
        return total_tokens, current_counter, fname


def main():
    # Go through the languages in the dictionary
    for lang in lang_dic:
        print(lang_dic[lang][2])

        # Request HTML
        html = request(lang)

        # Find link for the archive file
        link = find_link(lang, html)
        print(link)

        # Define a name for the zip file
        fname_zip = get_root(lang) + 'subs.zip'
        print(fname_zip)

        # Download a zip file
        get_file(link, fname_zip)
        print('Zip file downloaded')

        # Unzip file
        unzip_file(fname_zip, get_root(lang))

        total_tokens, current_counter = search_xmls(lang, link)
        remove_xmls(lang)

        report.write(lang_dic[lang][0] + ';' + str(total_tokens) + ';' + str(current_counter) + '\n')


if __name__ == "__main__":
    main()
