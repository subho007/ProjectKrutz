from scrapy.selector import Selector
from apkSpider.items import ApkItem

# Parse the information for an individual APK from the Google Play store
def parse_google(response):
    sel = Selector(response)
    item = ApkItem()

    item['download_url'] = response.meta['download_url']

    info_container = sel.xpath('//div[@class="info-container"]')
    item['name'] = info_container.xpath('//div[@class="document-title"]/div/text()').extract()
    item['developer'] = info_container.xpath('//div[@itemprop="author"]/a/span[@itemprop="name"]/text()').extract()
    item['genre'] = info_container.xpath('//span[@itemprop="genre"]/text()').extract()

    score_container = sel.xpath('//div[@class="score-container"]')
    item['score'] = score_container.xpath('//div[@class="score"]/text()').extract()

    additional_information = sel.xpath('//div[@class="details-section metadata"]')
    item['date_published'] = additional_information.xpath('//div[@itemprop="datePublished"]/text()').extract()
    item['file_size'] = additional_information.xpath('//div[@itemprop="fileSize"]/text()').extract()
    item['num_downloads'] = additional_information.xpath('//div[@itemprop="numDownloads"]/text()').extract()
    item['software_version'] = additional_information.xpath('//div[@itemprop="softwareVersion"]/text()').extract()
    item['operating_systems'] = additional_information.xpath('//div[@itemprop="operatingSystems"]/text()').extract()

    # TODO: Store the information in SQL table
    yield item