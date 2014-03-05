from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scraper.items import ApkDownloadItem
from scrapy.http import Request
from play import parse_google

class TeamApkSpider(CrawlSpider):
    name = "teamapk"
    start_urls = ["http://www.teamapk.co"]

    # Parses the Team APK home page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//h1/a[contains(@href, "android-download")]/@href').extract()

        for url in apk_page_urls:
            yield Request(url, callback=self.parse_page)

        next_page = sel.xpath('//a[@class="nextpostslink"]/@href').extract()
        
        yield Request(next_page[0])

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//p/a[".apk" = substring(@href, string-length(@href) - 3)]/@href').extract()
        google_play_url = sel.xpath('//p/a[contains(@href, "play.google.com/store/apps")]/@href').extract()
        
        if download_url and google_play_url:
            yield Request(download_url[0], meta={'url': response.url}, callback=self.parse_file)
            yield Request(google_play_url[0], meta={'url': response.url}, callback=parse_google)

    # Parses the URL to an actual APK file
    def parse_file(self, response):
        sel = Selector(response)
        form_action = sel.xpath('//form/@action').extract()
        
        if form_action:
            return [Request(url=form_action[0], method="POST", meta={'url': response.meta['url']}, callback=self.after_post)]

    # Download the APK file
    def after_post(self, response):
        item = ApkDownloadItem()
        item['file_urls'] = [response.url]
        item['come_from'] = response.meta['url']
        
        yield item