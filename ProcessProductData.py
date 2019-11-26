import re


def sanitizeText(string, array):
    return re.sub(r"{}".format('|'.join(array)), r'', string).strip()


class ProcessProductData:
    def __init__(self, doc, url, product_index):
        self.doc = doc
        self.url = url
        self.product_index = product_index

    def getText(self, xpathArray):
        string = 'N/A'
        for xpath in xpathArray:
            result = self.doc.xpath(xpath)
            if not result:
                continue
            string = ' '.join(''.join(result).split()).strip()
            string = sanitizeText(
                string,
                [
                    # non ascii
                    '[^\x00-\x7f]',
                    'Publication Date:'
                ])
            break
        return string

    def getImage(self, xpathArray):
        string = 'N/A'
        for xpath in xpathArray:
            result = self.doc.xpath(xpath)
            if not result:
                continue
            string = ' > '.join([i.strip() for i in result])
            break
        return string

    def generateData(self):
        data = {}
        data['name'] = self.getText([
            '//*[@id="productTitle"]//text()',
            '//*[@id="ebooksProductTitle"]//text()', '//*[@id="title"]//text()'
        ])
        data['author'] = self.getText(
            ['//*[@id="bylineInfo"]/span/span[1]/a[1]//text()'])
        data['published'] = self.getText([
            '//*[@id="title"]/span[3]//text()',
            '//*[@id="productDetailsTable"]/tr/td/div/ul/li[5]//text()',
            '//*[@id="productDetailsTable"]/tr/td/div/ul/li[4]//text()',
            '//*[@id="productDetailsTable"]/tr/td/div/ul/li[3]//text()'
        ])
        data['image'] = self.getImage([
            '//img[@id="imgBlkFront"]/@src',
            '//img[@id="ebooksImgBlkFront"]/@src'
        ])
        data['url'] = self.url
        data['product_index'] = self.product_index

        # Final cleanup
        return dict(
            map(
                lambda k: (k, data[k].strip()
                           if isinstance(data[k], str) else data[k]), data))
