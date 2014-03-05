from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scraper.items import ApkDownloadItem
from scrapy.http import Request
from play import parse_google
from time import sleep

class AndroidPotSpider(CrawlSpider):
    name = "androidpot"
    start_urls = ["http://www.androidpot.net"]

    # Parses the AndroidPot home page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//h2/a/@href').extract()

        for url in apk_page_urls:
            yield Request(url, callback=self.parse_page)

        next_page = sel.xpath('//a[@class="blog-pager-older-link"]/@href').extract()
        
        yield Request(next_page[0])

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//a[".apk" = substring(@href, string-length(@href) - 3)]/@href').extract()
        google_play_url = sel.xpath('//a[contains(@href, "play.google.com/store/apps")]/@href').extract()
        
        if download_url and google_play_url:
            yield Request(download_url[0], meta={'url': response.url}, callback=self.parse_file)
            yield Request(google_play_url[0], meta={'url': response.url}, callback=parse_google)

    # Download the APK file
    def parse_file(self, response):
        item = ApkDownloadItem()
        item['file_urls'] = [response.url]
        item['come_from'] = response.meta['url']
        
        yield item