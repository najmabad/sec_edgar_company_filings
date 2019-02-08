import sys
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import glob
from tqdm import tqdm

from count_words_helpers import process_file
from scripts.input.rules import rules


def main(rules):
    pool = Pool(processes=cpu_count() - 1)

    files = glob.glob('{}/*.txt'.format(INPUT_FOLDER_10K))

    headers = ["cik", "filing_date", "period_of_report", "id", "doc_type"]
    headers.extend([rule[0] for rule in rules])

    csv_lines = [",".join(headers)]
    for file_name, counts, doc_type in tqdm(pool.imap_unordered(process_file, [(file, rules) for file in files]), total=len(files)):
        csv_lines.append(
            f"{file_name.replace('_', ',')},{doc_type},{','.join([str(counts[rule[0]]) for rule in rules])}"
        )

    with open('{}/words_count.csv'.format(OUTPUT_FOLDER), 'w') as f:
        f.write("\n".join(csv_lines))


if __name__ == '__main__':
    INPUT_FOLDER_10K = sys.argv[1] if len(sys.argv) > 1 else '10K_files'
    OUTPUT_FOLDER = sys.argv[2] if len(sys.argv) > 2 else '10K_files'
    main(rules)
