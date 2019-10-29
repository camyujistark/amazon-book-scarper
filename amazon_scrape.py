from lxml import html
import csv,os,json
import requests
import sys

from exceptions import ValueError
from time import sleep

if len(sys.argv) != 2:
    sys.stderr.write("usage: {} need second argument ".format(sys.argv[0]))
    exit(-1) # or deal with this case in another way
url = sys.argv[1]

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 \
            Safari/537.36'}
    page = requests.get(url, headers=headers)
    doc = html.fromstring(page.content)

    RAW_NAME = doc.xpath('//h1[@id="title"]//text()')
    RAW_AUTHOR = doc.xpath('//*[@id="bylineInfo"]/span/span[1]/a[1]//text()')
    RAW_IMAGE = doc.xpath('//img[@id="ebooksImgBlkFront"]/@src')

    NAME = ' '.join(''.join(RAW_NAME).split()) \
        if RAW_NAME else None
    AUTHOR = ' '.join(''.join(RAW_AUTHOR).split()).strip()\
        if RAW_AUTHOR else None
    IMAGE = ' > '.join([i.strip() for i in RAW_IMAGE])\
        if RAW_IMAGE else None

    if page.status_code != 200:
        raise ValueError('captha')
    data = {
            'name': NAME,
            'author': AUTHOR,
            'image': IMAGE,
            'url': url,
            }

    return data


def ReadAsin():
    print "Processing: "+ url
    print json.dumps(AmzonParser(url), sort_keys=True, indent=4)

if __name__ == "__main__":
    ReadAsin()
0

