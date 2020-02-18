import json
import re
import sys
from exceptions import ValueError

import requests
from lxml import html

from constants import SHORT_URL, URL_HEADERS
from ProcessProductData import ProcessProductData
from workflow import ICON_WEB, Workflow

query = sys.argv[1]


def generateAmazonShortURL(string):
    TYPE = 'dp'
    if not string:
        sys.exit('need parameter')
    else:
        regDp = re.compile(r'^.*(dp|gp)\/([A-Za-z0-9]+)')
        match = regDp.search(string)
        TYPE = match.group(1)
        ID = match.group(2)
        if not match:
            sys.exit('must be amazon url')

    return {
        "query": string,
        "shorturl": SHORT_URL + '/' + TYPE + '/' + ID,
        "product_index": ID
    }


def getProductData(query):
    amznurl = generateAmazonShortURL(query)
    s = requests.Session()
    page = s.get(amznurl['shorturl'], headers=URL_HEADERS)
    doc = html.fromstring(page.content)
    # print(page.content)

    if page.status_code != 200:
        raise ValueError('captha')

    pd = ProcessProductData(doc, amznurl['shorturl'], amznurl['product_index'])
    return pd.generateData()


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
