import sys
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import glob
from tqdm import tqdm

from count_words_helpers import RULES, process_file


def main():
    print(cpu_count() - 1)
    pool = Pool(processes=cpu_count() - 1)

    files = glob.glob('{}/*.txt'.format(INPUT_FOLDER_10K)

    headers = ["cik", "filing_date", "period_of_report", "id", "doc_type"]
    headers.extend([rule[0] for rule in RULES])

    csv_lines = [",".join(headers)]
    for file_name, counts, doc_type in tqdm(pool.imap_unordered(process_file, files), total=len(files)):
        csv_lines.append(
            f"{file_name.replace('_', ',')},{doc_type},{','.join([str(counts[rule[0]]) for rule in RULES])}"
        )

    with open('{}/words_count.csv'.format(INPUT_FOLDER_10K), 'w') as f:
        f.write("\n".join(csv_lines))


if __name__ == '__main__':
    INPUT_FOLDER_10K = sys.argv[1] if len(sys.argv) > 1 else '10K_files'
    main()
