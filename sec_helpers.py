import time

from bs4 import BeautifulSoup


def request_page(s, url):
    r = s.get(url)
    backoff = 1
    while r.status_code == 429:
        time.sleep(backoff ** 2)
        backoff += 1
        r = s.get(url)
    return r


def get_search_results(s, cik):
    """
    scrapes the EDGAR Search Results for a given company (i.e. looking for a given CIK) filtering
    for 'Filing Type' = '10-K'
    :param s: instance of request.session
    :param cik: Central Index Key, i.e company identifier
    :return: a list of links to the 10-K, 10-K/A, 10-K405 pages of the company. Note that all
    documents starting with 10-K will be downloaded.
    """

    r = request_page(s,
                     'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&type=10-k&count=100'.format(
                         cik))

    soup = BeautifulSoup(r.text, 'html.parser')

    links = []

    for row in soup.select('div#seriesDiv table.tableFile2 tr')[1:]:  # exclude the first row that contains headers
        tds = row.select('td')

        document_link = tds[1].select('a')[0].attrs['href']

        if document_link.startswith('/'):
            document_link = 'https://www.sec.gov{}'.format(document_link)
        links.append(document_link)

    return links


def get_10k(s, cik, output_folder):
    """
    Downloads the 10k files for a given `cik` to the `output_folder`
    :param s: instance of request.session
    :param cik: Central Index Key, i.e the company identifier
    :param output_folder:
    :return: list of links for all complete submission text file of a given company
    """
    links_by_year = get_search_results(s, cik)

    for link in links_by_year:

        # retrieve the content of the webpage containing the complete submission file
        r = request_page(s, link)
        soup = BeautifulSoup(r.text, 'html.parser')

        # find `filing date` and `period of report`
        filing_date = None
        period_of_report = None

        for el in soup.select('div.formGrouping'):
            if el.text.lower().strip().startswith('filing date'):
                filing_date = el.select('div.info')[0].text

            if el.text.lower().strip().startswith('period of report'):
                period_of_report = el.select('div.info')[0].text

        doc_id = None
        doc = None

        # find document link
        table_rows = soup.find('table').select('tr')[1:]  # skip the first row that contains the header
        for row in table_rows:
            tds = row.select('td')
            if tds[1].text.lower().strip() == 'complete submission text file':
                document_element = tds[2].select('a')[0]
                document_link = document_element.attrs['href']
                doc_id = document_link.split('/')[-1].replace('.txt', '')  # save document id

                if document_link.startswith('/'):
                    document_link = 'https://www.sec.gov{}'.format(document_link)

                    if document_link.lower().endswith('htm') or document_link.lower().endswith('html'):
                        doc = BeautifulSoup(request_page(s, document_link).text, 'html.parser').getText(separator=' ')

                    else:
                        doc = request_page(s, document_link).text

        if not doc_id or not doc:
            print(f'Could not find doc_id for complete sumbission text file of CIK: {cik} ({link}) - SKIPPING')
            continue

        f_path = '{folder}/{cik}_{fd}_{pr}_{doc_id}.txt'.format(folder=output_folder, cik=cik,
                                                                fd=filing_date,
                                                                pr=period_of_report, doc_id=doc_id)

        with open(f_path, 'w') as f:
            f.write(doc)


def _fetch_helper(args):
    s, cik, output_path = args
    return cik, get_10k(s, cik, output_path)
