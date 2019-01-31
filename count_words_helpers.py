import re
import sys

from stopwords import stopwords

RULES = [
    ('total_words', re.compile(r"\b\w+\b")),
    ('variable_cost_ct', re.compile(r"\bvariable\b \bcosts?\b")),
    ('variable_exp_ct', re.compile(r"\bvariable\b \bexpenses?\b")),
    ('fixed_exp_ct', re.compile(r"\bfixed\b \bexpenses?\b")),
    ('fixed_cost_ct', re.compile(r"\bfixed\b \bcosts?\b")),
    ('large_fixed_ct', re.compile(r"\blarge\b \bfixed\b")),
    ('sign_fixed_ct', re.compile(r"\bsignificant\b \bfixed\b")),
    ('rel_fixed_ct', re.compile(r"\brelatively\b \bfixed\b")),
    ('mostly_fixed_ct', re.compile(r"\bmostly\b \bfixed\b")),
    ('just_in_time_ct', re.compile(r"\bjust\b \bin\b \btime\b")),
    ('lean_ct', re.compile(r"\blean\b")),
    ('tot_quality_mng_ct', re.compile(r"\btotal\b \bquality\b \bmanagement\b")),
    ('six_sigm_ct', re.compile(r"\bsix\b \bsigma\b")),
    ('scale_econ_ct', re.compile(r"\bscale\b \beconomies\b")),
    ('scope_econ_ct', re.compile(r"\bscope\b \beconomies\b")),
    ('econ_of_scale_ct', re.compile(r"\beconomies\b \bof\b \bscale\b")),
    ('econ_of_scope_ct', re.compile(r"\beconomies\b \bof\b \bscope\b")),
    ('unv_ct', re.compile(r"\buniversity\b \bof\b")),
    ('outsource_ct', re.compile(r"\boutsource\b|\boutsourcing\b|\boutsourced\b")),
]


def _find_doc_type(doc):
    doc_type = re.search(
        pattern=r"((form)|(type)):\s(\d{1,2}-k.*)\n",
        string=doc)

    if doc_type:
        return doc_type.groups()[-1]

    return "unknown"


def remove_html_tags(doc):
    """
    cleans a string
    @param doc: a string
    @return: cleaned text
    """

    # remove script and style tags
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", doc.strip().lower())

    # remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)

    # next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

    return cleaned


def clean_text(doc):
    cleaned = remove_html_tags(doc)
    cleaned = re.sub(
        r"&nbsp;|\n|\t|\d+|x]|\]|\!|\"|\#|\$|\%|\&|\(|\)|\*|\+|\,|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\-|\`|\{|\||\}|\~",
        " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = ''.join([i if ord(i) < 128 else '' for i in cleaned])
    cleaned = ' '.join([word for word in cleaned.split(" ") if len(word) > 1 and word not in stopwords])
    return cleaned


def count_special_words(doc):
    """
    computes numbers of occurencies for each special word
    :param doc: a file object
    :return: doc_type, total words and individual counts
    """
    counts = {}
    for rule_name, rule in RULES:
        counts[rule_name] = len(re.findall(rule, doc))

    return counts


#
# def count_founded_in(doc):
#     '''
#     computes numbers of occurencies the words 'funded in' is present in the document
#     @param doc:
#     @return:
#     '''
#     text, doc_type, tot_words = clean_text(doc)
#     founded_year', r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,5}founded in(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,5}", text))
#     return doc_type, tot_words, founded_year


def process_file(file_path):
    with open(file_path, 'r') as f:
        raw_text = f.read()
        text = clean_text(raw_text)
        counts = count_special_words(text)
        doc_type = _find_doc_type(raw_text.lower())

    return file_path.replace('.txt', '').split('/')[-1], counts, doc_type
