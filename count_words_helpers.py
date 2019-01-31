import re
import sys

from scripts.input.rules import RULES
from scripts.input.stopwords import stopwords


def _find_doc_type(doc):
    doc_type = re.search(
        pattern=r"((form)|(type)):\s(\d{1,2}-k.*)\n",
        string=doc)

    if doc_type:
        return doc_type.groups()[-1]

    else:
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
        r"&nbsp;|\n|\t|\d+|x]|!|\"|#|\$|%|&|\(|\)|\*|\+|,|\.|/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|-|`|{|\||\}|~",
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
