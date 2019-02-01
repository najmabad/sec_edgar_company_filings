import re
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
    cleaned = re.sub(r"\s+", ' ', cleaned)
    cleaned = ''.join([i if ord(i) < 128 else '' for i in cleaned])
    cleaned = ' '.join([word for word in cleaned.split(" ") if len(word) > 1 and word not in stopwords])
    return cleaned


def find_special_words(doc, rules):
    """
    computes numbers of occurrences for each special word
    :param rules:
    :param doc: text on which the regex expression is applied
    :return: total words, individual counts for each word
    """
    counts = {}
    for rule_name, rule in rules:
        counts[rule_name] = re.findall(rule, doc)

    return counts


def process_file(args):
    file_path, rules = args
    with open(file_path, 'r') as f:
        raw_text = f.read()
        text = raw_text#clean_text(raw_text)
        # counts = {k: len(v) for k, v in find_special_words(text, rules).items()}
        doc_type = _find_doc_type(raw_text.lower())

    return file_path.replace('.txt', '').split('/')[-1], find_special_words(text, rules), doc_type
