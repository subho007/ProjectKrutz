import requests
from scrapy import log
from scrapy.selector import Selector
from scraper.items import ApkItem
from key import api_key

# Parse the information for an individual APK from the Google Play store
def parse_app(response):
    sel = Selector(response)
    item = ApkItem()

    # Special logic for GooglePlaySpider
    if response.meta['come_from'] == 'googleplay':
        price = sel.xpath('//meta[@itemprop="price"]/@content').extract()[0]

        # We are only downloading free apps
        if price != '0':
            log.msg('Not a free app, skipping item: %s' % response.url, level=log.INFO)
            return

        package_name = response.url[response.url.find('id=') + 3:]

        data = {
            'packagename': package_name,
            'fetch': 'false',
            'api_key': api_key
        }

        post_data = requests.post('http://api.evozi.com/apk-downloader/download', data=data).json()

        # If a download URL is not sent back, we know that an error occurred
        if 'url' not in post_data:
            log.msg('< %s >' % response.url, level=log.ERROR)
            return

        item['url'] = response.url
        item['file_urls'] = [post_data['url']]

    # Logic for all other Spider objects
    else:
        item['url'] = response.meta['url']
        item['file_urls'] = response.meta['file_urls']

    info_container = sel.xpath('//div[@class="info-container"]')
    item['name'] = info_container.xpath('//div[@class="document-title"]/div/text()').extract()[0]
    item['developer'] = info_container.xpath('//div[@itemprop="author"]/a/span[@itemprop="name"]/text()').extract()[0]
    item['genre'] = info_container.xpath('//span[@itemprop="genre"]/text()').extract()[0]

    score_container = sel.xpath('//div[@class="score-container"]')
    item['score'] = score_container.xpath('//div[@class="score"]/text()').extract()[0]

    additional_information = sel.xpath('//div[@class="details-section metadata"]')
    item['date_published'] = additional_information.xpath('//div[@itemprop="datePublished"]/text()').extract()[0]
    item['file_size'] = additional_information.xpath('//div[@itemprop="fileSize"]/text()').extract()[0].strip()
    item['num_downloads'] = additional_information.xpath('//div[@itemprop="numDownloads"]/text()').extract()[0].strip()
    item['software_version'] = additional_information.xpath('//div[@itemprop="softwareVersion"]/text()').extract()[0].strip()
    item['operating_systems'] = additional_information.xpath('//div[@itemprop="operatingSystems"]/text()').extract()[0].strip()

    yield item