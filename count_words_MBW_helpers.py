from local_paths import *
import re
import numpy as np


def clean_text(doc):
    '''
    cleans a file object
    @param doc: a file object
    @return: cleaned text
    '''

    # remove script and style tags
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", doc)

    # remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)

    # next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

    # delete spaces and make text lower
    cleaned = cleaned.strip().lower()
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"\n|\t", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)


    # find document type
    try:
        doc_type = re.search(pattern=r"conformed submission type:\s?((\b\d+-k\/?405\b)|(\b\d+-k/a\b)|(\b\d+-k\b)|(\b\d+-k[^\s]+\b))",
                             string=cleaned)
    except:
        doc_type = re.search(pattern=r"form\s?((\b\d+-k/?405\b)|(\b\d+-k/a\b)|(\b\d+-k\b)|(\d+-k[^\s]+\b))",
                             string=cleaned)

    if doc_type == None:
        doc_type = np.nan
    else:
        doc_type = doc_type.groups()[0]




    # delete numbers and special characters
    cleaned = re.sub(r"\d+", " ", cleaned)
    cleaned = re.sub(
        """x]|\]|\!|\"|\#|\$|\%|\&|\(|\)|\*|\+|\,|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\-|\`|\{|\||\}|\~""", " ",
        cleaned)

    cleaned = ''.join([i if ord(i) < 128 else '' for i in cleaned])
    cleaned = ' '.join([word for word in cleaned.split(" ") if len(word) > 1])
    tot_words = len(cleaned.split(' '))


    return cleaned, doc_type, tot_words





def count_special_wrds(doc):
    '''
    computes numbers of occurencies for each special word
    @param doc: a file object
    @return: doc_type, total words and individual counts
    '''
    text, doc_type, tot_words = clean_text(doc)
    variable_cost_ct = len(re.findall(r"\bvariable\b \bcosts?\b", text))
    variable_exp_ct = len(re.findall(r"\bvariable\b \bexpenses?\b", text))
    fixed_exp_ct = len(re.findall(r"\bfixed\b \bexpenses?\b", text))
    fixed_cost_ct = len(re.findall(r"\bfixed\b \bcosts?\b", text))
    large_fixed_ct = len(re.findall(r"\blarge\b \bfixed\b", text))
    sign_fixed_ct = len(re.findall(r"\bsignificant\b \bfixed\b", text))
    rel_fixed_ct = len(re.findall(r"\brelatively\b \bfixed\b", text))
    mostly_fixed_ct = len(re.findall(r"\bmostly\b \bfixed\b", text))
    just_in_time_ct = len(re.findall(r"\bjust\b \bin\b \btime\b", text))
    lean_ct = len(re.findall(r"\blean\b", text))
    tot_quality_mng_ct = len(re.findall(r"\btotal\b \bquality\b \bmanagement\b", text))
    six_sigm_ct = len(re.findall(r"\bsix\b \bsigma\b", text))
    scale_econ_ct = len(re.findall(r"\bscale\b \beconomies\b", text))
    scope_econ_ct = len(re.findall(r"\bscope\b \beconomies\b", text))
    econ_of_scale_ct = len(re.findall(r"\beconomies\b \bof\b \bscale\b", text))
    econ_of_scope_ct = len(re.findall(r"\beconomies\b \bof\b \bscope\b", text))
    unv_ct = len(re.findall(r"\buniversity\b \bof\b", text))
    outsource_ct = len(re.findall(r"\boutsource\b|\boutsourcing\b|\boutsourced\b", text))

    return doc_type, tot_words, variable_cost_ct, variable_exp_ct, fixed_exp_ct, fixed_cost_ct, large_fixed_ct, sign_fixed_ct, sign_fixed_ct, rel_fixed_ct, mostly_fixed_ct, just_in_time_ct, lean_ct, tot_quality_mng_ct, six_sigm_ct, scale_econ_ct, scope_econ_ct, econ_of_scale_ct, econ_of_scope_ct, unv_ct, outsource_ct



#
# def count_founded_in(doc):
#     '''
#     computes numbers of occurencies the words 'funded in' is present in the document
#     @param doc:
#     @return:
#     '''
#     text, doc_type, tot_words = clean_text(doc)
#     founded_year = len(re.findall(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,5}founded in(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,5}", text))
#     return doc_type, tot_words, founded_year



def process_file(fn):
    try:
        with open(fn, 'r') as f:
            out = count_special_wrds(f.read())
        return fn.replace('{}/10K_files/'.format(hard_disk), '').replace('.txt', ''), out
    except Exception as e:
        print(e)
        print("error with last file", fn)
    pass




with open('/Volumes/Samsung_T5/10K_files/19520_1995-03-24_1994-11-30_0000912057-95-001705.txt', 'r') as f:
    read_data = f.read()
    cleaned, doc_type, tot_words = clean_text(read_data)



# def process_file_2(fn):
#     try:
#         with open(fn, 'r') as f:
#             out = count_founded_in(f.read())
#         return fn.replace('{}/10K_files/'.format(hard_disk), '').replace('.txt', ''), out
#     except:
#         print("error with last file", fn)
#     pass



#
# with open("/Users/najmabader/Desktop/0000950134-03-015704.txt") as file: # Use file to refer to the file object
#     doc = file.read()
#     doc_type, tot_words, variable_cost_ct, variable_exp_ct, fixed_exp_ct, fixed_cost_ct, large_fixed_ct, sign_fixed_ct, sign_fixed_ct, rel_fixed_ct, mostly_fixed_ct, just_in_time_ct, lean_ct, tot_quality_mng_ct, six_sigm_ct, scale_econ_ct, scope_econ_ct, econ_of_scale_ct, econ_of_scope_ct, unv_ct, outsource_ct = count_special_wrds(doc)
#
#
# print(doc_type, tot_words, variable_cost_ct, variable_exp_ct, fixed_exp_ct, fixed_cost_ct, large_fixed_ct, sign_fixed_ct, sign_fixed_ct, rel_fixed_ct, mostly_fixed_ct, just_in_time_ct, lean_ct, tot_quality_mng_ct, six_sigm_ct, scale_econ_ct, scope_econ_ct, econ_of_scale_ct, econ_of_scope_ct, unv_ct, outsource_ct
# )