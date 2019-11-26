import json
import re
import sys
from exceptions import ValueError
from urllib import parse

import requests
from lxml import html

import ProcessProductData
from amznscraper.constants import (BASE_URL, DEFAULT_REGION, QUERY_BUILD_DICT,
                                   REGION_CODES, SEARCH_URL, SHORT_URL,
                                   URL_ADDONS)
from workflow import ICON_WEB, Workflow

query = sys.argv[1]


def build_url(url=None, query='', page_num=1, region=DEFAULT_REGION):
    if url is None:
        # build from query, page_num and region
        base = build_base_url(region)
        url = SEARCH_URL % (base, query, page_num)

    if url.startswith('/'):
        url = build_base_url(region) + url

    parsed_obj = parse.urlparse(url)
    query_dict = parse.parse_qs(parsed_obj.query)

    # update the query dict
    query_dict.update(QUERY_BUILD_DICT)

    parsed_obj = parsed_obj._replace(
        query=parse.urlencode(query_dict, doseq=True))
    return parsed_obj.geturl()


def build_base_url(region=DEFAULT_REGION):
    find_region = region.upper()
    if find_region not in REGION_CODES.keys():
        raise ValueError('%s is not a know Amazon region' % (repr(region)))

    return BASE_URL + REGION_CODES[find_region]


def generateAmazonShortURL(url):
    if not url:
        sys.exit('need url')
    regDp = re.compile(r'^.*(dp|gp)\/([A-Za-z0-9]+)')
    match = regDp.search(url)
    if not match:
        sys.exit('must be amazon url')

    return {
        "url": url,
        "shorturl": SHORT_URL + match.group(1) + '/' + match.group(2),
        "product_index": match.group(2)
    }


def sanitizeText(string, array):
    return re.sub(r"{}".format('|'.join(array)), r'', string).strip()


def getDoc(url):
    page = requests.get(url, URL_ADDONS)
    if page.status_code != 200:
        raise ValueError('captha')
    return html.fromstring(page.content)


def getProductData(query):
    amznurl = generateAmazonShortURL(query)
    doc = getDoc(amznurl['shorturl'])
    return ProcessProductData(doc, amznurl['shorturl'],
                              amznurl['product_index']).generateData()


def main(wf):
    data = getProductData(query)
    wf.add_item(title='copy all to clipboard',
                subtitle='all the args to clipboard',
                arg=json.dumps(data),
                valid=True,
                icon=ICON_WEB)
    wf.add_item(title='Name',
                subtitle=data['name'],
                copytext=data['name'],
                icon=ICON_WEB)
    wf.add_item(title='Author',
                subtitle=data['author'],
                copytext=data['author'],
                icon=ICON_WEB)
    wf.add_item(title='Url',
                subtitle=data['url'],
                copytext=data['url'],
                icon=ICON_WEB)
    wf.add_item(title='Image',
                subtitle=data['image'],
                copytext=data['image'],
                icon=ICON_WEB)
    wf.add_item(title='Published',
                subtitle=data['published'],
                copytext=data['published'],
                icon=ICON_WEB)
    wf.add_item(title='Product Index',
                subtitle=data['product_index'],
                copytext=data['product_index'],
                icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
