from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from apkSpider.items import ApkItem
from scrapy.http import Request

class TeamApkSpider(CrawlSpider):
    name = "teamapk"
    allowed_domains = ["teamapk.co", "play.google.com", "devfiles.co"]
    start_urls = ["http://www.teamapk.co"]

    # Parses the Team APK home page and subsequent pages
    def parse(self, response):
        sel = Selector(response)
        apk_page_urls = sel.xpath('//h1/a[contains(@href, "android-download")]/@href').extract()

        for url in apk_page_urls:
            yield Request(url, callback=self.parse_page)

        next_page = sel.xpath('//a[@class="nextpostslink"]/@href').extract()
        
        yield Request(next_page[0]);

    # Parses pages for individual APK files
    def parse_page(self, response):
        sel = Selector(response)
        download_url = sel.xpath('//p/a[contains(@href, ".apk")]/@href').extract()
        google_play_url = sel.xpath('//p/a[contains(@href, "play.google.com/store/apps")]/@href').extract()
        
        if download_url:
            yield Request(download_url[0], callback=self.parse_file)
            if google_play_url:
                yield Request(google_play_url[0], meta={'download_url': response.url}, callback=self.parse_google)

    # Parses the URL to an actual APK file
    def parse_file(self, response):
        sel = Selector(response)
        form_action = sel.xpath('//form/@action').extract()
        
        if form_action:
            return [Request(url=form_action[0], method="POST", callback=self.after_post)]

    # Download the APK file
    def after_post(self, response):
        item = ApkItem()
        item['file_urls'] = [response.url]
        
        yield item

    # Parse the information for an individual APK from the Google Play store
    def parse_google(self, response):
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