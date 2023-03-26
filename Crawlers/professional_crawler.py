!pip install pythainlp
!pip install wordfreq
!pip install mecab
!apt-get install mecab mecab-ipadic-utf8 libmecab-dev swig
!pip install mecab-python3
!pip install mecab-ko
!pip install ipadic
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

report = codecs.open('../report_professional.csv', 'a', 'utf-8')
report.write('folder_name;tokens;txt_files\n')

resource = ''
copyright_short = ''
copyright_long = ''
duplicate_text_set = set()

total_tokens = 0
first_counter = 0
current_counter = 0

 
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

def total_tokens_not_reached(total_tokens, resource, language,tokens_per_resource_per_language):
    if ((total_tokens > 5000000) or (language in ['en', 'fr','de','sp'] and resource in ['MultiUN', 'Europarl'] and tokens_per_resource_per_language>2500000)):
        return False
    else:
        return True

def removeWordsBeforeAfterNewLine(text, before):
    try:
        splitted = text.split('.', 1)[before]
    except:
        try:
            splitted = text.split('\n', 1)[before]
        except:
            splitted = text
    return splitted 

# Search xmls, represents one unzipped folder
def search_xmls(lang, link,total_tokens,current_counter,curr_resource):
    path = os.path.join(get_root(lang), resource, 'raw',lang)
    tokens_per_resource_per_language = 0

    
    for root, dirs, files in os.walk(path):
        for file in sorted(files):
            if total_tokens_not_reached(total_tokens, curr_resource, lang, tokens_per_resource_per_language):
                if get_text(os.path.join(root, file), lang, True) is not False:
                    text, year, tokens, tokens_arr = get_text(os.path.join(root, file), lang, False)

                    total_tokens, current_counter, fname, current_tokens = sample(link, text, year, tokens, lang,
                                                                  current_counter, total_tokens, tokens_arr)
                    tokens_per_resource_per_language += current_tokens
                    print("Saved file", fname)

                    if fname != '':
                        os.remove(os.path.join(root, file))

                    else:
                        print('Skipped file')
                else:
                    print('Skipped file due to parsing error or duplicate file')
            else:
                return total_tokens, current_counter

    return total_tokens, current_counter

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

# Generate file name
def generate_fname(lang, current_counter):
    path = get_root(lang)
    max_counter = 0
    search_fcounter = re.compile(lang_dic[lang][1] + '_pro_' + '([0-9]+)(\\.txt)?')
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
    fname = lang_dic[lang][1] + '_pro_' + str(int(current_counter) + 1) + '.txt'
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

def write_50k_to_file(fname,lang_dic,lang,year,resource,link,text,isWhole):
    f1 = codecs.open(fname, 'w', 'utf-8')
    meta = '''# language_name_wals:	''' + lang_dic[lang][2] + '''
# language_name_glotto:	''' + lang_dic[lang][3] + '''
# iso639_3:	''' + lang_dic[lang][1] + '''
# year_composed:	NA
# year_published:	''' + year + '''
# mode:	written
# genre_broad:	professional
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
    
# Retrieve text from xml document
def get_text(fname, lang, checkForDuplicates):
    text_for_checking_duplicates = ''
    num_line = 0
    f = codecs.open(fname, 'r', 'utf-8')
    try:
        xml = f.read().encode('utf-8')
    except UnicodeDecodeError:
        f.close()
        return False
    except:
        return False
    parser = etree.XMLParser(encoding='utf-8')
    try:
        tree = etree.XML(xml, parser)
    except etree.XMLSyntaxError:
        f.close()
        return False
    text = ''
    year = 'NA'

    for el in tree.iter("*"):
        if el.tag == 's':
            try:
                line = el.text.strip()
            except AttributeError:
                line = ''
            line = line.replace('\\t', '\t')
            text += line + '\n'
            num_line += 1
            if(num_line<20):
                text_for_checking_duplicates += line + '\n'

        if el.tag == 'pubDate':
            try:
                year = el.text[:4]
            except TypeError:
                year = 'NA'
    f.close()
    tokens, tokens_arr = count_tokens(text, lang)
    if(checkForDuplicates):
        if(text_for_checking_duplicates in duplicate_text_set):
            return False
        else:
            duplicate_text_set.add(text_for_checking_duplicates)
        
    return text, year, tokens, tokens_arr

# Remove unnecessary xmls
def remove_xmls(lang):
    rootFolder = get_root(lang)
    path = os.path.join(rootFolder, resource)
    shutil.rmtree(path)
    os.remove(os.path.join(rootFolder,'INFO'))
    os.remove(os.path.join(rootFolder , 'LICENSE'))
    os.remove(os.path.join(rootFolder , 'README'))
    print("Unnecessary files removed")
    
# Unzip files
def unzip_file(fname_zip, root):
    zip_ref = zipfile.ZipFile(fname_zip, 'r')
    zip_ref.extractall(root)
    zip_ref.close()
    os.remove(fname_zip)
    
# Get request to obtain *.zip file
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

# Root path
def get_root(lang):
    pathToZip = os.path.join('..','Corpus',lang_dic[lang][0], 'professional' )

    if not os.path.exists(pathToZip):
        os.makedirs(pathToZip)
    return pathToZip

# Request HTML page for the current language 
def request(language):
    r = requests.get('http://opus.nlpl.eu/opusapi', params={'corpus': resource,
                                                            'source': language,
                                                            'preprocessing': 'raw'})
    html = r.json()
    return html

# Find link to the *.zip
def find_link(language, html):
    print("RESOURCE", resource)
    target = [obj for obj in html['corpora'] if(obj['corpus'] == resource and obj['source'] == language 
                                                and obj['target'] == "" and obj['latest'] == "True")]
    if(not target):
        target = [obj for obj in html['corpora'] if(obj['corpus'] == resource and obj['source'] == language 
                                                and obj['target'] == "")]
    try:
        link = target[0]['url']
        return link
    except:
        return None

def skip_resource_language(resource, language):
    return False

def main():
    print("STARTING....")
    total_tokens_for_all_languages = 0
    
    for lang in lang_dic:
        current_counter = 0
        #total_tokens for single language for all resources
        total_tokens = 0
        for curr_resource in ['EUconst', 'MultiUN', 'Europarl']:
            if(skip_resource_language(curr_resource,lang)):
                continue
            global resource
            resource = curr_resource
            global copyright_short
            copyright_short = 'http://opus.nlpl.eu/' + resource + '.php'
            global copyright_long
            copyright_long = 'http://opus.nlpl.eu/' + resource + '.php J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)'

            global duplicate_text_set
            duplicate_text_set = set()

    
            print("Language: ",lang_dic[lang][2])

            # Request HTML
            html = request(lang)

            # Find link for the archive file
            link = find_link(lang, html)
            if(link is None):
                print('No corpus for the language ' + lang)
                continue
            print("Link to zip file: ", link)

            # Define a name for the zip file
            fname_zip = get_root(lang) + lang + '.zip'
            print("Zip file filename: ",fname_zip)

            # Download a zip file
            get_file(link, fname_zip)
            print("Zip file downloaded")

            # Unzip file
            unzip_file(fname_zip, get_root(lang))
            print("Zip file unzipped")

            total_tokens, current_counter = search_xmls(lang, link,total_tokens, current_counter,curr_resource)

            remove_xmls(lang)
            
        total_tokens_for_all_languages += total_tokens
        report.write(lang_dic[lang][0] + ';' + str(total_tokens) + ';' + str(current_counter+1) + '\n')
    # print("Total tokens collected for all languages: ", total_tokens_for_all_languages)
    report.close()
    print("END...")


if __name__ == "__main__":
    main()