from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scraper.items import ApkDownloadItem
from scrapy.http import Request
from play import parse_google

class APKTOPSpider(CrawlSpider):
    name = "apktop"
    start_urls = ["http://www.papktop.com/category/android-apps"]

    # Parses the APKTOP "Android Apps" page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//div[@class="title"]/h2/a/@href').extract()

        for url in apk_page_urls:
            yield Request(url, callback=self.parse_page)

        next_page = sel.xpath('//a[@class="next"]/@href').extract()
        
        yield Request(next_page[0])

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//a[contains(@href, ".apk")]/@href').extract()
        app_id = response.url[response.url.find('id=') + 3:]
        google_play_url = sel.xpath('//a[contains(@href, "play.google.com/store/apps")]/@href').extract()        
        
        if download_url and google_play_url:
            item = ApkDownloadItem()
            item['file_urls'] = [download_url[0]]
            yield item

            yield Request(google_play_url[0], meta={'download_url': response.url}, callback=parse_google)