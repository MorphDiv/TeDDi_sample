# -*- coding: utf-8 -*-

# Chinese
# English
# Finnish
# French
# German
# Greek
# Spanish
# Tagalog
# Farsi
# Hebrew
# Japanese
# Korean
# Russian

import codecs
import random
import warnings
from string import punctuation

import os
import re
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize as nltk_tokenize
from pythainlp import word_tokenize as thai_tokenize
from wordfreq import tokenize

warnings.filterwarnings("ignore")

report = codecs.open('report_gutenberg.csv', 'w', 'utf-8')
report.write('folder_name;tokens;txt_files\n')

link = re.compile('<li class="pgdbetext"><a href="(/ebooks.*?)">')
p_tag = re.compile(u'<p.*?>(.*?)</p>', re.DOTALL)

# Last element: languages in Gutenberg
lang_dic = {
     'en': ['English_eng', 'eng', 'English', 'English', 'Latn', 'English'],
     'fi': ['Finnish_fin', 'fin', 'Finnish', 'Finnish', 'Latn', 'Finnish'],
     'fr': ['French_fra', 'fra', 'French', 'French', 'Latn', 'French'],
     'de': ['German_deu', 'deu', 'German', 'German', 'Latn', 'German'],
     'el': ['Greek_Modern_ell', 'ell', 'Greek (Modern)', 'Modern Greek', 'Grek', 'Greek'],
     'he': ['Hebrew_Modern_heb', 'heb', 'Hebrew (Modern)', 'Modern Hebrew', 'Hebr', 'Hebrew'],
     'ja': ['Japanese_jpn', 'jpn', 'Japanese', 'Japanese', 'Jpan', 'Japanese'],
     'zh': ['Mandarin_cmn', 'cmn', 'Mandarin', 'Mandarin Chinese', 'Hans', 'Chinese'],
     'fa': ['Persian_pes', 'pes', 'Persian', 'Western Farsi', 'Arab', 'Farsi'],
     'ru': ['Russian_rus', 'rus', 'Russian', 'Russian', 'Cyrl', 'Russian'],
     'es': ['Spanish_spa', 'spa', 'Spanish', 'Spanish', 'Latn', 'Spanish'],
     'tl': ['Tagalog_tgl', 'tgl', 'Tagalog', 'Tagalog', 'Latn', 'Tagalog'],
}


# Root path
def get_root(lang):
    return '../Corpus/' + lang_dic[lang][0] + '/fiction/'


# Generate file name
def generate_fname(lang, current_counter):
    path = get_root(lang)
    max_counter = 0
    search_fcounter = re.compile(lang_dic[lang][1] + '_fic_' + '([0-9]+)(\\.txt)?')
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
    fname = lang_dic[lang][1] + '_fic_' + str(int(current_counter) + 1) + '.txt'
    print(get_root(lang) + fname)
    return (get_root(lang) + fname), current_counter


# Converts HTML entities to unicode. For example '&amp;' becomes '&'.
def html_entities_transform(text):
    soup = BeautifulSoup(text)
    text = soup.get_text()
    return str(text)


# Request HTML page for the current language
def request_lang(language):
    r = requests.get('http://www.gutenberg.org/browse/languages/' + language)
    html = r.text
    return html


# Request HTML page for the current author
def request_author(author):
    r = requests.get('http://www.gutenberg.org/browse/authors/' + author)
    html = r.text
    return html


# Find link to the *.zip with OpenSubtitles, the newest version possible
def find_links(html):
    all_links = re.findall(link, html)
    print('NUM LINKS: ', len(all_links))
    return all_links


# Get html with a book
def get_book(cur_link):
    r = requests.get('http://www.gutenberg.org' + cur_link + '.html.noimages')
    r.encoding = r.apparent_encoding
    html_book = r.text

    if 'Page Not Found' in html_book:
        cur_link = cur_link.replace('ebooks', 'files')
        find_number = re.search('[0-9]+', cur_link)
        if find_number:
            number = find_number.group(0)

            print('\nhttp://www.gutenberg.org' + cur_link + '/' + number + '-h/' + number + '-h.htm')

            r = requests.get('http://www.gutenberg.org' + cur_link + '/' + number + '-h/' + number + '-h.htm')
            r.encoding = r.apparent_encoding
            html_book = r.text

            return html_book, 'http://www.gutenberg.org' + cur_link + '/' + number + '-h/' + number + '-h.htm'

    print('\nhttp://www.gutenberg.org' + cur_link + '.html.noimages')

    return html_book, 'http://www.gutenberg.org' + cur_link + '.html.noimages'


# Find p tags
def find_p(html_book):
    text = ''
    all_p = re.findall(p_tag, html_book)
    start_i = 0
    end_i = len(all_p)
    for i in range(len(all_p)):
        if 'Produced by' in all_p[i]:
            start_i = i
            break

    if start_i == 0:
        for i in range(len(all_p)):
            if 'START OF THIS PROJECT GUTENBERG' in all_p[i]:
                start_i = i
                break

    for i in range(len(all_p)):
        if 'End of the Project Gutenberg' in all_p[i]:
            end_i = i
            break
        elif 'End of Project Gutenberg' in all_p[i]:
            end_i = i
            break

    for i in range(len(all_p)):
        if start_i < i < end_i:
            text += all_p[i] + '\n'

    all_p = all_p[start_i+1:end_i]

    text = text.replace('<br/>', '')

    return text, all_p


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

    return len(tokens)


# Make meta info
def make_meta(lang, html_book, sample_type, source):
    year = 'NA'
    find_year = re.search('<(.*?)name="DCTERMS.created"(.*?)>', html_book)
    if find_year:
        find_four_num = re.search('[0-9]{4}', find_year.group(0))
        if find_four_num:
            year = find_four_num.group(0)

    author = ''
    find_author = re.search('<(.*?)name="DCTERMS.creator"(.*?)>', html_book)
    if find_author:
        find_content = re.search('content\\s*=\\s*"(.*?)"', find_author.group(0))
        if find_content:
            author = find_content.group(1)

    title = ''
    find_title = re.search('<(.*?)name="DCTERMS.title"(.*?)>', html_book)
    if find_title:
        find_content = re.search('content\\s*=\\s*"(.*?)"', find_title.group(0))
        if find_content:
            title = find_content.group(1)

    find_description = re.search('<(.*?)DCTERMS.subject(.*?)>', html_book)
    short_description = 'NA'

    if find_description:
        if 'content' in find_description.group(1):
            content = re.search('content\\s*=\\s*"(.*?)"', find_description.group(1))
            if content:
                if author != '' and title != '':
                    short_description = author + ', ' + title + ', ' + content.group(1)
                else:
                    short_description = content.group(1)

        elif 'content' in find_description.group(2):
            content = re.search('content\\s*=\\s*"(.*?)"', find_description.group(2))
            if content:
                if author != '' and title != '':
                    short_description = author + ', ' + title + ', ' + content.group(1)
                else:
                    short_description = content.group(1)

    else:
        if author != '' and title != '':
            short_description = author + ', ' + title

        else:
            short_description = 'Gutenberg Project, ' + lang_dic[lang][3]

    # Try to find info in the tag pre
    if year == 'NA' or short_description == 'Gutenberg Project, ' + lang_dic[lang][3]:
        find_pre = re.search('<pre(.*?)>(.*?)</pre>', html_book, re.DOTALL)
        if find_pre:

            short_description = ''
            find_author = re.search('[aA]uthor: (.+)\r\n', html_book)
            find_title = re.search('[tT]itle: (.+)\r\n', html_book)
            find_date = re.search('[rR]elease [dD]ate:(.*?)([0-9]{4})', html_book)

            if find_author:
                short_description += find_author.group(1)
            if find_title:
                short_description += ', ' + find_title.group(1)
            if find_date:
                year = find_date.group(2)

    short_description = html_entities_transform(short_description)

    # Exclude broken lines
    if '\n' in short_description:
        short_description = re.sub('\n', ', ', short_description)

    meta = '''# language_name_wals:	''' + lang_dic[lang][2] + '''
# language_name_glotto:	''' + lang_dic[lang][3] + '''
# ISO_639-3:	''' + lang_dic[lang][1] + '''
# year_composed:	NA
# year_published:	''' + year + '''
# mode:	written
# genre_(broad):	fiction
# genre_(narrow):	general_fiction
# writing_system:	''' + lang_dic[lang][4] + '''
# special_characters:	NA
# short_description:	''' + html_entities_transform(short_description) + '''
# source:	''' + source + '''
# copyright_short:	http://www.gutenberg.org
# copyright_long:	http://www.gutenberg.org
# sample_type:	''' + sample_type + '''
# comments:	NA

    '''
    meta = re.sub('\t{2,}', '\t', meta)
    return meta


# One sample of 50000 tokens
def one_sample(lines, lang):
    # Sample tokens
    sample_tokens = 0
    sample = ''

    starts = [-1]

    # Different conditions for different writing systems
    if lang in ['zh', 'ja', 'ko']:
        search_string = '^.{0,5}$'
    else:
        search_string = '^.{0,10}$'

    for i in range(len(lines)-1):
        # Random start -- visual division of the text
        # E.g. blank line, very short line (sample after that)
        find_start = re.search(search_string, lines[i])
        if find_start:
            try:
                if lines[i+1][0] not in '。！」？、，'\
                        and lines[i+1][0] not in punctuation:
                    starts.append(i)
            except:
                starts.append(i)

    # Choose random start from collected ids (and 0 line)
    random_start = random.choice(starts)
    print('RANDOM START (LINE): ', random_start+1)

    # Take out 50000 tokens starting from the random start
    line_counter = 0
    for line in lines[random_start + 1:]:
        line_tokens = count_tokens(line, lang)
        if sample_tokens + line_tokens <= 50000:
            sample += line + '\n'
            sample_tokens += line_tokens
            line_counter += 1
        else:
            break

    print('REACHED END (LINE): ', random_start + 1 + line_counter)

    # Cut used lines
    lines = lines[:random_start + 1] + lines[random_start + 1 + line_counter:]

    # If sampled less than 50000 tokens, then start from the beginning
    # Constraint: do not sample from the beginning, if it will be just 1-2 sentences (20 tokens estimate)
    if sample_tokens < 50000 and not sample_tokens > 49980:
        print('SAMPLED SO FAR: ', sample_tokens)
        print('CONTINUE FROM THE BEGINNING')
        line_counter = 0
        for line in lines:
            line_tokens = count_tokens(line, lang)
            if sample_tokens + line_tokens <= 50000:
                sample += line + '\n'
                sample_tokens += line_tokens
                line_counter += 1
            else:
                break

        # Cut used lines again
        lines = lines[line_counter:]

    print('SAMPLED TOKENS: ', sample_tokens)

    return lines, sample, sample_tokens


def sampling(text, tokens, lang):

    current_tokens = 0

    samples = []

    lines = text.split('\n')

    if tokens > 50000:

        # No constraints on the number of samples per file (until possible to gather contiguous 50000 tokens)

        # Number of samples
        num_samples = int(tokens/50000)

        print('NUM SAMPLES: ', num_samples)

        for n in range(num_samples):
            print('SAMPLE #' + str(n+1))
            lines, current_sample, current_sample_tokens = one_sample(lines, lang)
            samples.append(current_sample)
            current_tokens += current_sample_tokens

    else:
        samples.append(text)
        current_tokens += tokens

    return samples, current_tokens


def main():
    # tgl 15, 17, 18, 25, 51 -- to check
    # added manually
    # links = ['/ebooks/14205',
    #          '/ebooks/18536',
    #          '/ebooks/16446',
    #          '/ebooks/18888',
    #          '/ebooks/18887']

    # fr 88, 94, 106 -- to check
    # links = ['/ebooks/24300',
    #          '/ebooks/29251',
    #          '/ebooks/22388']

    for lang in lang_dic:
        sources = []

        print('\nLANGUAGE: ', lang_dic[lang][2])

        total_tokens = 0
        txt_files = 0

        if lang == 'en':
            authors = 'abcdefghijklmnopqrstuvwxyz'
            for letter in authors:
                html = request_author(letter)
                en_link = re.compile('<li class="pgdbetext"><a href="(/ebooks.*?)">.*?English')
                found_links = re.findall(en_link, html)
                print('NUM LINKS: ', len(found_links))

        else:
            html = request_lang(lang)
            found_links = find_links(html)

        current_counter = 0

        for fl in found_links:

            if total_tokens < 5000000:

                html_book, source = get_book(fl)

                # Check language of the file (should be one)
                if 'Language: ' + lang_dic[lang][5] in html_book:

                    if source not in sources:
                        sources.append(source)

                        text, all_p = find_p(html_book)
                        text = html_entities_transform(text)

                        if text != '':

                            tokens = count_tokens(text, lang)
                            print('TOKENS: ', tokens)

                            samples, current_tokens = sampling(text, tokens, lang)

                            total_tokens += current_tokens

                            if tokens > 50000:
                                sample_type = 'part'
                            else:
                                sample_type = 'whole'

                            meta = make_meta(lang, html_book, sample_type, source)

                            for sample in samples:
                                fname, current_counter = generate_fname(lang, current_counter)
                                f = codecs.open(fname, 'w', 'utf-8')
                                f.write(meta)

                                # Replace tabs
                                sample = re.sub('\t+', ' ', sample)

                                f.write(sample)

                                txt_files += 1

                            print('CURRENT TOTAL TOKENS: ', total_tokens)

            else:
                print('TOTAL TOKENS: ', total_tokens)
                report.write(lang_dic[lang][0] + ';' + str(total_tokens) + ';' + str(txt_files) + '\n')
                break

        if total_tokens < 5000000:
            print('TOTAL TOKENS: ', total_tokens)
            report.write(lang_dic[lang][0] + ';' + str(total_tokens) + ';' + str(txt_files) + '\n')


if __name__ == "__main__":
    main()
