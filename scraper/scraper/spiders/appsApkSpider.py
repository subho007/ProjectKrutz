from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scraper.items import ApkItem
from scrapy.http import Request

class AppsApkSpider(CrawlSpider):
    name = "appsapk"
    start_urls = ["http://www.appsapk.com/android/all-apps/"]
    
    # Parses the AppsApk "All Apps" page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//h2[@class="post-title"]/a/@href').extract()

        for url in apk_page_urls:
            yield Request(url, callback=self.parse_page)

        next_page = sel.xpath('//div[@class="pagenav clearfix"]/span[@class="number current"]/following::a[1]/@href').extract()
        
        yield Request(next_page[0])

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//a[".apk" = substring(@href, string-length(@href) - 3)]/@href').extract()

        if download_url:
            item = ApkItem()
            item['file_urls'] = download_url
            item['url'] = response.url
            yield item