"""
Loops through the corpus files and reports the number of texts, genres covered,
unique characters per language.

This program returns zero values for languages that are not covered yet (unlike line_counts.py)

Structure of the output:
language,number_texts,number_genres,number_characters
"""


import codecs
import csv
import os
import re


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


def main(report_writer):
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

                            else:
                                number_texts += count_files(subdir, lang_root)
                                number_characters += count_characters(subdir, lang_root)

            print(language, number_texts, number_genres, number_characters)

            result[language] = [number_texts, number_genres, number_characters]

            i += 1

        for lang in all_langs:
            for k, v in result.items():
                if k == lang:
                    report_writer.writerow((k, v[0], v[1], v[2]))


if __name__ == '__main__':
    report_name = 'progress.csv'

    with open(report_name, 'w', encoding='utf-8') as report:
            writer = csv.writer(report, lineterminator='\n')
            writer.writerow(('language', 'number_texts', 'number_genres', 'number_characters'))
            main(writer)
            print('\nDONE')