import os
import codecs
import timeit

from report_tokenized import count_files, walklevel

root_path = '/home/olga/Documents/Repositories/100LC/Corpus'
genres = ['fiction', 'non-fiction', 'conversation', 'professional', 'technical', 'grammar_examples']

genres_abbr = {
    'fiction': 'fic',
    'non-fiction': 'nfi',
    'conversation': 'con',
    'professional': 'pro',
    'technical': 'tec',
    'grammar_examples': 'gre'
}

report = codecs.open('report_lines.csv', 'w', 'utf-8')
report.write('language,fic_lines,nfi_lines,con_lines,pro_lines,tec_lines,gre_lines,'
             'fic_files,nfi_files,con_files,pro_files,tec_files,gre_files,'
             'total_lines,total_files\n')

result = {}


def count_lines(subdir, lang_root):
    joined_subdir = os.path.join(lang_root, subdir)
    lines = 0

    for root, dirs, files in os.walk(joined_subdir):
        for file in files:
            f = codecs.open(os.path.join(joined_subdir, file), 'r', 'utf-8')
            for line in f:
                # Exclude meta and lines that we don't want to count
                if '<translation>' not in line \
                        and '<segmentation>' not in line \
                        and '<glossing>' not in line \
                        and '<comment>' not in line \
                        and not line.startswith('#') \
                        and line != '\n':

                    # Structured files
                    if '<line' in line:
                        lines += 1

                    # Unstructured files
                    elif not line.startswith('<'):
                        lines += 1

    return lines


def main():
    start = timeit.timeit()
    for root, dirs, files in walklevel(root_path, level=0):
        for cur_dir in dirs:

            total_files = 0
            total_lines = 0

            language = cur_dir

            print(language)
            lang_root = os.path.join(root_path, language)

            # genre : num_files, num_lines
            lang_stat = {
                'fic': [0, 0],
                'nfi': [0, 0],
                'con': [0, 0],
                'pro': [0, 0],
                'tec': [0, 0],
                'gre': [0, 0]
            }

            for cur_root, cur_dirs, cur_files in os.walk(lang_root):
                for subdir in cur_dirs:
                    for genre in genres:
                        if subdir == genre:
                            if subdir == 'non-fiction' or subdir == 'grammar_examples':
                                amount_files_w = count_files(subdir + '/written', lang_root)
                                amount_lines_w = count_lines(subdir + '/written', lang_root)
                                amount_files_s = count_files(subdir + '/spoken', lang_root)
                                amount_lines_s = count_lines(subdir + '/spoken', lang_root)

                                lang_stat[genres_abbr[genre]] = [amount_files_w + amount_files_s,
                                                                 amount_lines_w + amount_lines_s]

                                total_files += amount_files_w + amount_files_s
                                total_lines += amount_lines_w + amount_lines_s

                            else:
                                amount_files = count_files(subdir, lang_root)
                                amount_lines = count_lines(subdir, lang_root)
                                lang_stat[genres_abbr[genre]] = [amount_files, amount_lines]

                                total_files += amount_files
                                total_lines += amount_lines

            result[language] = ',' + \
                                str(lang_stat['fic'][1]) + ',' + \
                                str(lang_stat['nfi'][1]) + ',' + \
                                str(lang_stat['con'][1]) + ',' + \
                                str(lang_stat['pro'][1]) + ',' + \
                                str(lang_stat['tec'][1]) + ',' + \
                                str(lang_stat['gre'][1]) + ',' + \
                                str(lang_stat['fic'][0]) + ',' + \
                                str(lang_stat['nfi'][0]) + ',' + \
                                str(lang_stat['con'][0]) + ',' + \
                                str(lang_stat['pro'][0]) + ',' + \
                                str(lang_stat['tec'][0]) + ',' + \
                                str(lang_stat['gre'][0]) + ',' + \
                                str(total_lines) + ',' + \
                                str(total_files) + '\n'

    for k, v in sorted(result.items()):
        report.write(k + v)

    end = timeit.timeit()
    print('TIME:', end - start)


if __name__ == '__main__':
    main()
