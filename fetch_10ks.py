import sys
from multiprocessing.pool import Pool

import requests

from requests.adapters import HTTPAdapter
from tqdm import tqdm

from sec_helpers import _fetch_helper
import multiprocessing


def download_10ks(cik_list_path, output_path):
    adapter = HTTPAdapter(max_retries=10)
    s = requests.Session()
    s.mount('https://www.sec.gov/', adapter)
    with open(cik_list_path, 'r') as cik_file:
        ciks = cik_file.read().split('\n')[:20]
    keys = sorted([(s, i, output_path) for i in ciks])
    print(keys)
    pool = Pool(processes=min(8, multiprocessing.cpu_count() - 1))
    print(list(tqdm(pool.imap_unordered(_fetch_helper, keys), total=len(keys))))
    pool.close()


if __name__ == '__main__':
    OUTPUT_FOLDER_10K = sys.argv[1] if len(sys.argv) > 1 else '10K_files'
    # check_output(f'mkdir -p {OUTPUT_FOLDER_10K}')
    CIK_FILE_PATH = sys.argv[2] if len(sys.argv) > 2 else 'cik_list.txt'

    download_10ks(CIK_FILE_PATH, OUTPUT_FOLDER_10K)
