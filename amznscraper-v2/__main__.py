import json
import sys
from exceptions import ValueError

import requests
from lxml import html

import ProcessProductData
from amznscraper import generateAmazonShortURL
from amznscraper.constants import (BASE_URL, DEFAULT_REGION, QUERY_BUILD_DICT,
                                   REGION_CODES, SEARCH_URL, SHORT_URL,
                                   URL_ADDONS)
from workflow import ICON_WEB, Workflow

query = sys.argv[1]


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
