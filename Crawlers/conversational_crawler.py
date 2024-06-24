!pip install pythainlp
!pip install wordfreq
!pip install mecab
!apt-get install mecab mecab-ipadic-utf8 libmecab-dev swig
!pip install mecab-python3
!pip install mecab-ko
!pip install ipadic
!pip install git+https://github.com/TalkBank/TBDBpy.git

import nltk
nltk.download('punkt')

import codecs
import random
import shutil
import ssl
import time
import zipfile
from string import punctuation
from io import StringIO

import os
import re
import requests
import urllib3
from lxml import etree
import nltk
from nltk.tokenize import word_tokenize as nltk_tokenize
from pythainlp import word_tokenize as thai_tokenize
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
from wordfreq import tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

import MeCab
import mecab_ko_dic

import tbdb

lang_dic = {
    'ko': ['Korean_kor', 'kor', 'Korean', 'Korean', 'Kore'],
    'ja': ['Japanese_jpn', 'jpn', 'Japanese', 'Japanese', 'Jpan'],
    'zh': ['Mandarin_cmn', 'cmn', 'Mandarin', 'Mandarin Chinese', 'Hans'],
    'de': ['German_deu', 'deu', 'German', 'German', 'Latn'],
    'el': ['Greek_Modern_ell', 'ell', 'Greek (Modern)', 'Modern Greek', 'Grek'],
    'en': ['English_eng', 'eng', 'English', 'English', 'Latn'],
    'es': ['Spanish_spa', 'spa', 'Spanish', 'Spanish', 'Latn'],
    'eu': ['Basque_eus', 'eus', 'Basque', 'Basque', 'Latn'],
    'fa': ['Persian_pes', 'pes', 'Persian', 'Western Farsi', 'Arab'],
    'fi': ['Finnish_fin', 'fin', 'Finnish', 'Finnish', 'Latn'],
    'fr': ['French_fra', 'fra', 'French', 'French', 'Latn'],
    'gn': ['Guarani_gug', 'gug', 'Guaraní', 'Paraguayan Guaraní', 'Latn'],
    'ha': ['Hausa_hau', 'hau', 'Hausa', 'Hausa', 'Latn'],
    'he': ['Hebrew_Modern_heb', 'heb', 'Hebrew (Modern)', 'Modern Hebrew', 'Hebr'],
    'hi': ['Hindi_hin', 'hin', 'Hindi', 'Hindi', 'Deva'],

    'id': ['Indonesian_ind', 'ind', 'Indonesian', 'Indonesian', 'Latn'],
    'ka': ['Georgian_kat', 'kat', 'Georgian', 'Georgian', 'Geor'],
    'kl': ['Greenlandic_West_kal', 'kal', 'Greenlandic (West)', 'Kalaallisut', 'Latn'],
    'kn': ['Kannada_kan', 'kan', 'Kannada', 'Kannada', 'Knda'],
    'my': ['Burmese_mya', 'mya', 'Burmese', 'Burmese', 'Mymr'],
    'ru': ['Russian_rus', 'rus', 'Russian', 'Russian', 'Cyrl'],
    'sw': ['Swahili_swh', 'swh', 'Swahili', 'Swahili', 'Latn'],
    'th': ['Thai_tha', 'tha', 'Thai', 'Thai', 'Thai'],
    'tl': ['Tagalog_tgl', 'tgl', 'Tagalog', 'Tagalog', 'Latn'],
    'tr': ['Turkish_tur', 'tur', 'Turkish', 'Turkish', 'Latn'],
    'vi': ['Vietnamese_vie', 'vie', 'Vietnamese', 'Vietnamese', 'Latn'],
    'yo': ['Yoruba_yor', 'yor', 'Yoruba', 'Yoruba', 'Latn'],
    'zu': ['Zulu_zul', 'zul', 'Zulu', 'Zulu', 'Latn'],
    'mg': ['Malagasy_plt', 'plt', 'Malagasy', 'Plateau Malagasy', 'Latn'],
    'om': ['Oromo_Harar_hae', 'hae', 'Oromo (Harar)', 'Eastern Oromo', 'Latn'],
}

report = codecs.open('../report_conversation.csv', 'a', 'utf-8')
report.write('folder_name;tokens;txt_files\n')

resource = ''
copyright_short = ''
copyright_long = ''
duplicate_text_set = set()

total_tokens = 0
first_counter = 0
current_counter = 0



# get content from link
def get_content(link):
  response = requests.get(link)
  content = response.text
  # print(content)
  return content

# removes lines that start with @ or %
def remove_metadata_and_comments(text):
  lines = text.split('\n')
  filtered_lines = filter(lambda line: line.startswith('*'), lines)
  result = '\n'.join(filtered_lines)
  return result


# get date when resouce was created
def parse_date(content):
  pattern = r"@Date:\s+\d{1,2}-\w{3}-(\d{4})"
  match = re.search(pattern, content)
  if match:
      year = match.group(1)
  else:
      year = 'NA'
  return year


# read text line by line and remove everything before first : (speaker name)
def remove_speakers_names(text):
  lines = text.split('\n')
  result = []

  for line in lines:
      result.append(line.split(':', 1)[-1].strip())

  result_text = '\n'.join(result)
  return result_text


# filtering (.), [.*]
def filter_text(text):
  text = text.replace("(.)", "")
  text = re.sub(r'\[.*?\]', '', text)
  stripped_lines = [line.strip() for line in text.split('\n')]
  text = '\n'.join(stripped_lines)

  return text

def extract50K(text, lang):
    tokens_extracted = 0
    text = StringIO(text)
    text50K = ''
    remaining_text = ''
    while(True):
        nl = text.readline()
        if nl != '':
            tokens_extracted += count_tokens(nl, lang)[0]
            if(tokens_extracted < 50000):
                text50K += nl
            else:
                remaining_text += nl
        else:
            break;
    return text50K, remaining_text


def define_line_start(arr_text):
    random_range = [0]
    for i in range(int(len(arr_text)/2)):
        if arr_text[i][-1] in ['?','.']:
            char_start = i
            random_range.append(char_start)
    char_start = random.choice(random_range)
    return char_start

# Random starting point
def starting_point(arr_text, tokens, lang):
    if tokens > 100001:
        line_start = define_line_start(arr_text)
        return line_start
    else:
        return 0

def write_50k_to_file(fname,lang_dic,lang,year,resource,link,text,isWhole):
    f1 = codecs.open(fname, 'w', 'utf-8')
    meta = '''# language_name_wals:	''' + lang_dic[lang][2] + '''
# language_name_glotto:	''' + lang_dic[lang][3] + '''
# iso639_3:	''' + lang_dic[lang][1] + '''
# year_composed:	NA
# year_published:	''' + year + '''
# mode:	written
# genre_broad:	conversation
# genre_narrow:	NA
# writing_system:	''' + lang_dic[lang][4] + '''
# special_characters:	NA
# short_description:	''' + resource + '''
# source:	''' + link + '''
# copyright_short:	''' + copyright_short + '''
# copyright_long:	''' + copyright_long + '''
# sample_type:	''' + isWhole + '''
# comments:	NA
'''
    meta = re.sub('\t{2,}', '\t', meta)
    meta = re.sub(' {2,}', ' ', meta)
    f1.write(meta)

    text = re.sub('\t+', ' ', text)
    text = re.sub(' {2,}', ' ', text)

    f1.write(text[:-1])
    f1.close()

# Root path
def get_root(lang):
    pathToZip = os.path.join('..','Corpus',lang_dic[lang][0], 'conversation' )

    if not os.path.exists(pathToZip):
        os.makedirs(pathToZip)
    return pathToZip

# Generate file name
def generate_fname(lang, current_counter):
    path = get_root(lang)
    max_counter = 0
    search_fcounter = re.compile(lang_dic[lang][1] + '_con_' + '([0-9]+)(\\.txt)?')
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
    fname = lang_dic[lang][1] + '_con_' + str(int(current_counter) + 1) + '.txt'
    return os.path.join(get_root(lang) ,fname), current_counter

# Sample
def sample(link, text, year, tokens, lang, current_counter, total_tokens,tokens_arr):
    fname = ''
    if int(tokens) <= 50000 and int(tokens) > 0:
        fname, current_counter = generate_fname(lang, current_counter)
        write_50k_to_file(fname,lang_dic,lang,year,resource,link,text,'whole')
        total_tokens += int(tokens)

    if(tokens>50000):  
        whole_file_covered = 0
        while not whole_file_covered:
            starting_place = starting_point(text, tokens, lang)
            if (starting_place!=0):
                starting_place+=1
                
            left, right = text[:starting_place], text[starting_place:]
            text_with_only_50k, remaining_text = extract50K(right, lang)
            remaining_text = left + remaining_text          

            fname, current_counter = generate_fname(lang, current_counter)
            write_50k_to_file(fname,lang_dic,lang,year,resource,link,text_with_only_50k,'part')
            tokens = count_tokens(text_with_only_50k, lang)[0]
            total_tokens += tokens
            text = remaining_text
            tokens_arr = count_tokens(text, lang)[1]
            token_cnt, t = count_tokens(text, lang)

            if(token_cnt < 100):
                whole_file_covered = 1
                   
    return total_tokens, current_counter, fname, tokens

# Tokenization
def count_tokens(text, lang):
    if(lang =='zh_CN'):
        lang = 'zh'
    if(lang == 'en_GB'):
        lang = 'en'
    if lang in ['en', 'fi', 'fr', 'de', 'el', 'he', 'hi', 'id', 'ja', 'ko', 'zh','fa', 'ru', 'es', 'tr']:
        tokens = tokenize(text, lang)
    elif lang == 'th':
        tokens = thai_tokenize(text)
    else:
        tokens = nltk_tokenize(text)

    tokens_tmp = [word.lower() for word in tokens
              if not (word in punctuation and not word.isdigit() and not word.isspace())]

    return len(tokens_tmp),tokens

# Retrieve text from document and filter it
def get_text(lang, checkForDuplicates, content):
    if(not content):
      return False

    text_for_checking_duplicates = ''
    num_line = 0

    year = parse_date(content)
    content = remove_metadata_and_comments(content)
    content = remove_speakers_names(content)
    text = filter_text(content)

    text_for_checking_duplicates = tuple(text.splitlines()[:20])

    tokens, tokens_arr = count_tokens(text, lang)

    if(checkForDuplicates):
        if(text_for_checking_duplicates in duplicate_text_set):
            return False
        else:
            duplicate_text_set.add(text_for_checking_duplicates)
        
    return text, year, tokens, tokens_arr

def total_tokens_not_reached(total_tokens):
    if ((total_tokens > 5000000)):
        return False
    else:
        return True

def search_xmls(lang, total_tokens,current_counter, linkToFiles):
    tokens_per_resource_per_language = 0
    for row in linkToFiles['data']:
        path = row[linkToFiles['colHeadings'].index('path')]

        link = createUrl(path)
        text = get_content(link)

        if total_tokens_not_reached(total_tokens):
            if get_text(lang, True, text) is not False:
                text, year, tokens, tokens_arr = get_text(lang, False, text)

                total_tokens, current_counter, fname, current_tokens = sample(link, text, year, tokens, lang,
                                                              current_counter, total_tokens, tokens_arr)
                tokens_per_resource_per_language += current_tokens
                print("Saved file", fname)

            else:
                print('Skipped file due to parsing error or duplicate file')
        else:
            return total_tokens, current_counter

    return total_tokens, current_counter


# url to one text file
def createUrl(path):
  new_path = 'https://childes.talkbank.org/data-orig/' + path.split('/', 1)[1] + '.cha'
  print(new_path)
  return new_path

def skip_resource_language(resource, language):
    return False


def main():
    print("STARTING....")
    total_tokens_for_all_languages = 0
    
    for lang in lang_dic:
        current_counter = 0
        #total_tokens for single language for all resources
        total_tokens = 0
        for curr_resource in ['CHILDES']:
            if(skip_resource_language(curr_resource,lang)):
                continue
            global resource
            resource = curr_resource
            global copyright_short
            copyright_short = 'https://sla.talkbank.org/TBB/childes'
            global copyright_long
            copyright_long = 'MacWhinney, B. (2000). The CHILDES Project: Tools for analyzing talk. Third Edition. Mahwah, NJ: Lawrence Erlbaum Associates.'

            global duplicate_text_set
            duplicate_text_set = set()
    
            print("Language: ",lang_dic[lang][2])
            #get all files for language
            resources = tbdb.getTranscripts( {"corpusName": "childes", "lang": [lang_dic[lang][1]]} )
            #remove files that contain more than one language
            new_data = [row for row in resources['data'] if ',' not in row[2]]
            resources['data'] = new_data

            total_tokens, current_counter = search_xmls(lang, total_tokens,current_counter, resources)
            
        total_tokens_for_all_languages += total_tokens
        report.write(lang_dic[lang][0] + ';' + str(total_tokens) + ';' + str(current_counter+1) + '\n')
    # print("Total tokens collected for all languages: ", total_tokens_for_all_languages)
    report.close()
    print("END...")


if __name__ == "__main__":
    main()