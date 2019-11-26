#Defaults
REGION_CODES = {
    'AU': '.com.au',
    'BR': '.com.br',
    'CA': '.ca',
    'CN': '.cn',
    'DE': '.de',
    'ES': '.es',
    'FR': '.fr',
    'IN': '.in',
    'IT': '.it',
    'JP': '.co.jp',
    'MX': '.com.mx',
    'NL': '.nl',
    'SG': '.com.sg',
    'UK': '.co.uk',
    'US': '.com'
}
DEFAULT_REGION = "US"
BASE_URL = 'https://www.amazon'
SHORT_URL = 'https://www.amzn.com'
URL_HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 \
        Safari/537.36'
}

GAT_ID = 't' + 'ag'
QUERY_BUILD_DICT = {GAT_ID: 'alhs-20'}
SEARCH_URL = '%s/s/ref=nb_sb_noss?sf=qz&keywords=%s&ie=UTF8&unfiltered=1&page=%s'
