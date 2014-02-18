# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from apkSpider.items import ApkItem
from scrapy.http import Request

class TeamApkSpider(CrawlSpider):
    name = "teamapk"
    allowed_domains = ["teamapk.co", "play.google.com", "devfiles.co"]
    start_urls = ["http://www.teamapk.co"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//h1/a[contains(@href, "android-download")]/@href').extract()

        for url in urls:
            yield Request(url, callback=self.parsePage)

        nextPage = hxs.select('//a[@class="nextpostslink"]/@href').extract()
        
        yield Request(nextPage[0]);

    def parsePage(self, response):
        hxs = HtmlXPathSelector(response)
        downloadUrl = hxs.select('//p/a[contains(@href, ".apk")]/@href').extract()
        googleUrl = hxs.select('//p/a[contains(@href, "play.google.com/store/apps")]/@href').extract()
        
        yield Request(downloadUrl[0], callback=self.parseFile)

    def parseFile(self, response):
        hxs = HtmlXPathSelector(response)
        formAction = hxs.select('//form/@action').extract()
        
        if formAction:
            return [Request(url=formAction[0], method="POST", callback=self.afterPost)]

    def afterPost(self, response):
        # Still need to store app information (author, version, etc.) here
        item = ApkItem()
        item['file_urls'] = [response.url]
        
        # Uncomment to actually download APK files
        # yield item
