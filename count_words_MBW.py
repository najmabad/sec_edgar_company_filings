from count_words_MBW_helpers import *

from multiprocessing.pool import ThreadPool, Pool
import glob
from tqdm import tqdm

pool = Pool(processes=11)

results = {}
files = glob.glob('{}/10K_files/*.txt'.format(hard_disk))


files_test = ['/Volumes/Samsung_T5/10K_files/19520_1995-03-24_1994-11-30_0000912057-95-001705.txt']

# files = files[:500]

for key, output in tqdm(pool.imap_unordered(process_file, files), total=len(files)):
    results[key] = output

with open('{}/wrds_count.csv'.format(hard_disk), 'w') as f:
    out = "cik,filing_date,period_of_report,id,doc_type,total_words,variable_cost_ct,variable_exp_ct,fixed_exp_ct,fixed_cost_ct,large_fixed_ct,sign_fixed_ct,sign_fixed_ct,rel_fixed_ct,mostly_fixed_ct,just_in_time_ct,lean_ct,tot_quality_mng_ct,six_sigm_ct,scale_econ_ct,scope_econ_ct,econ_of_scale_ct,econ_of_scope_ct,unv_ct,outsource_ct"

    for k, v in results.items():
        out += "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},".format(k.replace('_', ','), v[0],
                                                                                             v[1], v[2], v[3], v[4],
                                                                                             v[5], v[6], v[7], v[8],
                                                                                             v[9], v[10], v[11], v[12],
                                                                                             v[13], v[14], v[15], v[16],
                                                                                             v[17], v[18], v[19],
                                                                                             v[20], )
    f.write(out)


print('done')





# second analysis

# for key, output in tqdm(pool.imap_unordered(process_file_2, files), total=len(files)):
#     results[key] = output
#
# with open('{}/wrds_ct.csv'.format(path_output), 'w') as f:
#     out = "cik, filing_date, period_of_report, id, doc_type, total_words, founded_year "
#
#     for k, v in results.items():
#         out += "\n{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},".format(k.replace('_', ','), v[0],
#                                                                                              v[1], v[2], v[3], v[4],
#                                                                                              v[5], v[6], v[7], v[8],
#                                                                                              v[9], v[10], v[11], v[12],
#                                                                                              v[13], v[14], v[15], v[16],
#                                                                                              v[17], v[18], v[19],
#                                                                                              v[20], )
#     f.write(out)
#
# print('done')
