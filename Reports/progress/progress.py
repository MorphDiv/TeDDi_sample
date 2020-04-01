"""
Loops through the corpus files and reports the number of texts, genres covered,
unique characters and number of tokens per language.

This program returns zero values for languages that are not covered yet (unlike line_counts.py)

Structure of the output:
iso,language,number_texts,number_genres,number_characters,number_tokens

How to run:
python progress.py -s (counts tokens in a simple way,
i.e. separates by white spaces (no matter what language is processed)

python progress.py -a (counts tokens in an advanced way;
treats Burmese, Chinese, Japanese, Korean, Thai differently)

Running time (corpus state on 30.03.20):
python progress.py -s (7-9 min)
python progress.py -a (4.5 hrs)
"""

# import unicodedata
# from string import punctuation

import codecs
import csv
import os
import re
import sys


# Using this list in order to track languages with zero counts
all_langs = ['Abkhaz_abk', 'Acoma_kjq', 'Alamblak_amp', 'Amele_aey', 'Apurina_apu',
             'Arabic_Egyptian_arz', 'Arapesh_Mountain_ape', 'Asmat_tml', 'Bagirmi_bmi',
             'Barasano_bsn', 'Basque_eus', 'Berber_MiddleAtlas_tzm', 'Burmese_mya',
             'Burushaski_bsk', 'CanelaKraho_ram', 'Chamorro_cha', 'Chukchi_ckt',
             'Cree_Plains_crk', 'Daga_dgz', 'Dani_LoweGrandValley_dni', 'English_eng',
             'Fijian_fij', 'Finnish_fin', 'French_fra', 'Georgian_kat', 'German_deu',
             'Gooniyandi_gni', 'Grebo_gry', 'Greek_Modern_ell', 'Greenlandic_West_kal',
             'Guarani_gug', 'Hausa_hau', 'Hebrew_Modern_heb', 'Hindi_hin', 'Hixkaryana_hix',
             'HmongNjua_hnj', 'Imonda_imn', 'Indonesian_ind', 'Jakaltek_jac', 'Japanese_jpn',
             'Kannada_kan', 'Karok_kyh', 'Kayardild_gyd', 'Kewa_kew', 'Khalkha_khk',
             'Khoekhoe_naq', 'Kiowa_kio', 'Koasati_cku', 'Korean_kor',
             'KoyraboroSenni_ses', 'Krongo_kgo', 'Kutenai_kut', 'Lakota_lkt', 'Lango_laj',
             'Lavukaleve_lvk', 'Lezgian_lez', 'Luvale_lue', 'Makah_myh', 'Malagasy_plt',
             'Mandarin_cmn', 'Mangarrayi_mpc', 'Mapudungun_arn', 'Maricopa_mrc',
             'Martuthunira_vma', 'Maung_mph', 'Maybrat_ayz', 'Meithei_mni', 'Mixtec_Chalcatongo_mig',
             'Ngiyambaa_wyb', 'Oneida_one', 'Oromo_Harar_hae', 'Otomi_Mezquital_ote', 'Paiwan_pwn',
             'Persian_pes', 'Piraha_myp', 'Quechua_Imbabura_qvi', 'Rama_rma',
             'Rapanui_rap', 'Russian_rus', 'Sango_sag', 'Sanuma_xsu', 'Slave_scs',
             'Spanish_spa', 'Supyire_spp', 'Swahili_swh', 'Tagalog_tgl', 'Thai_tha', 'Tiwi_tiw',
             'TukangBesi_bhq', 'Turkish_tur', 'Vietnamese_vie', 'Warao_wba', 'Wari_pav', 'Wichi_mzh',
             'Wichita_wic', 'Yagua_yad', 'Yaqui_yaq', 'Yoruba_yor', 'Zoque_Copainala_zoc', 'Zulu_zul']

root_path = '../../Corpus'
genres = ['fiction', 'non-fiction', 'conversation', 'professional', 'technical', 'grammar']

genres_abbr = {
    'fiction': 'fic',
    'non-fiction': 'nfi',
    'conversation': 'con',
    'professional': 'pro',
    'technical': 'tec',
    'grammar': 'gre'
}

result = {}


def generate_result_dict():
    for lang in all_langs:
        result[lang] = [0, 0, 0, 0]


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def get_body_text(f):
    text = ''
    for line in f:
        if '<translation>' not in line \
                and '<segmentation>' not in line \
                and '<glossing>' not in line \
                and '<comment>' not in line \
                and not line.startswith('#') \
                and line != '\n':

            if line.startswith('<line') or \
                    line.startswith('<title') or \
                    line.startswith('<verse') or \
                    line.startswith('<paragraph'):
                find_line = re.search('^<(line|title|verse|paragraph).*?\\s+(.*)$', line)
                if find_line:
                    text += find_line.group(2)
            else:
                text += line

    return text


def count_files(subdir, lang_root):
    try:
        joined_subdir = os.path.join(lang_root, subdir)
        amount_files = len([name for name in os.listdir(joined_subdir)
                            if os.path.isfile(os.path.join(joined_subdir, name))])
    except FileNotFoundError:
        amount_files = 0
    return amount_files


def count_characters(subdir, lang_root):
    joined_subdir = os.path.join(lang_root, subdir)
    characters = set()
    for root, dirs, files in os.walk(joined_subdir):
        for file in files:
            f = codecs.open(os.path.join(joined_subdir, file), 'r', 'utf-8')
            text = get_body_text(f)
            characters.update(set(text))

    return len(characters)


# Separate by white spaces (no matter what language is processed)
def count_tokens_simple(subdir, lang_root):
    joined_subdir = os.path.join(lang_root, subdir)
    tokens = []
    for root, dirs, files in os.walk(joined_subdir):
        for file in files:
            f = codecs.open(os.path.join(joined_subdir, file), 'r', 'utf-8')
            text = get_body_text(f)
            # Split by white spaces and \n
            tokens += text.split()

    return len(tokens)


# Treat languages differently by using language specific libraries
def count_tokens_advanced(subdir, lang_root):
    langs = {
        'eng': 'en',
        'fin': 'fi',
        'fra': 'fr',
        'deu': 'de',
        'ell': 'el',
        'hin': 'hi',
        'ind': 'id',
        'jpn': 'ja',
        'kor': 'ko',
        'cmn': 'zh',
        'pes': 'fa',
        'rus': 'ru',
        'spa': 'es',
        'tur': 'tr'
    }
    lang = lang_root[-3:]
    joined_subdir = os.path.join(lang_root, subdir)
    tokens = []
    for root, dirs, files in os.walk(joined_subdir):
        for file in files:
            f = codecs.open(os.path.join(joined_subdir, file), 'r', 'utf-8')
            text = get_body_text(f)

            if lang in langs:
                tokens += tokenize(text, langs[lang])
            elif lang == 'tha':
                tokens += thai_tokenize(text)
            elif lang == 'mya':
                word_segmenter = WordSegment()

                text_arr = text.split('\n')
                for line in text_arr:
                    segments = word_segmenter.normalize_break(line, 'unicode',
                                                              word_segmenter.SegmentationMethod.sub_word_possibility)
                    for segment in segments:
                        for word in segment:
                            if '\n' not in word:
                                tokens.append(word)

            else:
                # NLTK tokenize works slow, maybe there are other better ways of tokenization
                tokens += nltk_tokenize(text)

            # The loop slows down the program (additional removal of punctuation, digits)
            # for token in tokens:
            #     print(token)
            #     if len(token) == 1 and unicodedata.category(token[0])[0] not in 'LN':
            #         tokens.remove(token)
            #     if len(token) > 1 and unicodedata.category(token[0])[0] not in 'LN'
            #     and unicodedata.category(token[1])[0] not in 'LN':
            #         tokens.remove(token)
            # tokens = [word.lower() for word in tokens if not word.isdigit()
            #           and not word.isspace() and word not in punctuation]

    return len(tokens)


def main(tokenization_mode, report_writer):
    generate_result_dict()
    i = 1
    for root, dirs, files in walklevel(root_path, level=0):
        for cur_dir in dirs:
            language = cur_dir
            print('\n' + str(i) + ' / 100...')
            print(language, 'in process...')

            number_genres = 0
            number_texts = 0
            number_characters = 0
            number_tokens = 0

            lang_root = os.path.join(root_path, language)

            for cur_root, cur_dirs, cur_files in os.walk(lang_root):
                for subdir in cur_dirs:
                    for genre in genres:
                        if subdir == genre:
                            number_genres += 1
                            if subdir == 'non-fiction' or subdir == 'grammar':
                                for text_type in ['written', 'spoken']:
                                    number_texts += count_files(subdir + '/' + text_type, lang_root)
                                    number_characters += count_characters(subdir + '/' + text_type, lang_root)

                                    if tokenization_mode == '-s':
                                        number_tokens += count_tokens_simple(subdir + '/' + text_type, lang_root)
                                    elif tokenization_mode == '-a':
                                        number_tokens += count_tokens_advanced(subdir + '/' + text_type, lang_root)
                            else:
                                number_texts += count_files(subdir, lang_root)
                                number_characters += count_characters(subdir, lang_root)
                                number_tokens += count_tokens_simple(subdir, lang_root)
                                if tokenization_mode == '-s':
                                    number_tokens += count_tokens_simple(subdir, lang_root)
                                elif tokenization_mode == '-a':
                                    number_tokens += count_tokens_advanced(subdir, lang_root)

            print(language, number_texts, number_genres, number_characters, number_tokens)

            result[language] = [number_texts, number_genres, number_characters, number_tokens]

            i += 1

        for lang in all_langs:
            for k, v in result.items():
                if k == lang:
                    report_writer.writerow((k, v[0], v[1], v[2], v[3]))


if __name__ == '__main__':
    mode = sys.argv[1]
    report_name = ''

    if mode == '-s':
        report_name = 'progress_simple.csv'

    elif mode == '-a':
        from nltk.tokenize import word_tokenize as nltk_tokenize
        from pythainlp import word_tokenize as thai_tokenize
        from wordfreq import tokenize
        from word_breaker.word_segment_v5 import WordSegment
        report_name = 'progress_advanced.csv'

    if report_name != '':
        with open(report_name, 'w') as report:
            writer = csv.writer(report, lineterminator='\n')
            writer.writerow(('language', 'number_texts', 'number_genres', 'number_characters', 'number_tokens'))
            main(mode, writer)
            print('\nDONE')
    else:
        print('Please enter either -s or -a as an argument')

