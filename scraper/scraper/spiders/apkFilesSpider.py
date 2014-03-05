from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scraper.items import ApkDownloadItem
from scrapy.http import Request
from play import parse_google

class ApkFilesSpider(CrawlSpider):
    name = "apkfiles"
    start_urls = ["http://www.apkfiles.com/cat/applications/"]

    # Parses the F-Droid "Browse" page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_category_urls = sel.xpath('//div[@class="category_list"]/div[@class="category"]/a/@href').extract()

        for url in apk_category_urls:
            yield Request('http://www.apkfiles.com' + url, callback=self.parse_category)

    def parse_category(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//div[@class="file_list_item"]/a/@href').extract()

        for url in apk_page_urls:
            yield Request('http://www.apkfiles.com' + url, callback=self.parse_page)

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//a[@class="yellow_button"]/@href').extract()
        
        if download_url:
            item = ApkDownloadItem()
            item['file_urls'] = ['http://www.apkfiles.com' + download_url[0]]
            item['come_from'] = response.url
            yield item