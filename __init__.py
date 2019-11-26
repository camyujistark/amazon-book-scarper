import re
import sys

from constants import SHORT_URL


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
