from scrapy.selector import Selector
from scraper.items import ApkItem

# Parse the information for an individual APK from the Google Play store
def parse_google(response):
    sel = Selector(response)
    item = ApkItem()

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