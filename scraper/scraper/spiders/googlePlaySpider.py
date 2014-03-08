from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scraper.items import ApkItem
from play import parse_google
import re
import string
import requests

class GooglePlaySpider(CrawlSpider):
	name = 'googleplay'
	# allowed_domains = ['play.google.com', 'apps.evozi.com', 'api.evozi.com', 'storage.evozi.com']
	start_urls = [
		'https://play.google.com/store/apps'
	]
	rules = (
		# Rule(SgmlLinkExtractor(allow=('/store/apps$', )), callback='parse_category_group', follow=True),
		Rule(SgmlLinkExtractor(allow=('/store/apps/category/.*', )), callback='parse_category', follow=True),
		# Rule(SgmlLinkExtractor(allow=('/store/search\?.*', )), callback='parse_search', follow=True),
	)

	def parse_category_group(self, response):
		sel = Selector(response)
		category_groups = sel.xpath('//div[@class="padded-content3 app-home-nav"]')

		for category_group in category_groups:

			category_group_name = category_group.xpath('h2/a/text()').extract()

			categories = category_group.xpath('ul/li')
			for category in categories:
				category_name = category.xpath('a/text()').extract()
				category_url = category.xpath('a/@href').extract()[0]

		chars = string.ascii_uppercase + string.digits
		for x in chars:
			yield Request('https://play.google.com/store/search?q=' + x + '&c=apps', callback=self.parse_search)

		for x in chars:
			for y in chars:
				yield Request('https://play.google.com/store/search?q=' + x + y + '&c=apps', callback=self.parse_search)

		for x in chars:
			for y in chars:
				for z in chars:
					yield Request('https://play.google.com/store/search?q=' + x + y + z + '&c=apps', callback=self.parse_search)        

		return

	def parse_category(self, response):
		base_path = response.url.split('?')[0]   

		if '/collection/' in response.url:
			sel = Selector(response)
			apps = sel.xpath('//a[@class="title"]')
			has_app = False

			for app in apps:
				has_app = True
				app_name = app.xpath('text()').extract()
				app_url = app.xpath('@href').extract()
				yield Request('https://play.google.com' + app_url[0], callback=self.parse_app)

			if has_app:
				m = re.match(r'(.*)\?start=(\d+)&num=24', response.url)
				if m is None:
					start_number = 24                  
				else:
					start_number = int(m.group(2)) + 24
				# yield Request(base_path + '?start=' + str(start_number) + '&num=24', callback=self.parse_category)

		return

	def parse_search(self, response):
		m = re.match(r'(.*)&start=(\d+)&num=24', response.url)
		if m is None:
			base_path = response.url
			start_number = 24                  
		else:
			start_number = int(m.group(2)) + 24
			base_path = m.group(1)

		sel = Selector(response)
		apps = sel.xpath('//a[contains(@href,"/store/apps/details")]')
		has_app = False

		for app in apps:
			has_app = True
			app_url = app.xpath('@href').extract()
			yield Request('https://play.google.com' + app_url[0], callback=self.parse_app)

		if has_app:
			yield Request(base_path + '&start=' + str(start_number) + '&num=24', callback=self.parse_search)

		return

	def parse_app(self, response):
		sel = Selector(response)
		price = sel.xpath('//meta[@itemprop="price"]/@content').extract()[0]

		try:
			if int(price) == 0:
				package_name = response.url[response.url.find('id=') + 3:]
				download_page = requests.get('http://apps.evozi.com/apk-downloader/')

				var_name, var_value = re.search("var\s*fetched_desc = '';\r*\n*\s+var\s*(\w*)\s*=\s*\W*([a-zA-Z\d\-\_]*)", download_page.text, re.MULTILINE).groups()
				timestamp = re.search(", t: (\w*)", download_page.text, re.MULTILINE).group(1)

				data = {
					'fccfeadfb': var_value,
					'fetch': 'false',
					'packagename': package_name,
					't': timestamp
				}

				post_data = requests.post('http://api.evozi.com/apk-downloader/download', data=data)

				# yield Request(response.url, meta={'url': response.url, 'file_urls': [post_data.json()['url']]}, callback=parse_google)

				item = ApkItem()

				item['url'] = response.url
				item['file_urls'] = [post_data.json()['url']]

				info_container = sel.xpath('//div[@class="info-container"]')
				item['name'] = info_container.xpath('//div[@class="document-title"]/div/text()').extract()[0]
				item['developer'] = info_container.xpath('//div[@itemprop="author"]/a/span[@itemprop="name"]/text()').extract()[0]
				item['genre'] = info_container.xpath('//span[@itemprop="genre"]/text()').extract()[0]

				score_container = sel.xpath('//div[@class="score-container"]')
				item['score'] = score_container.xpath('//div[@class="score"]/text()').extract()[0]

				additional_information = sel.xpath('//div[@class="details-section metadata"]')
				item['date_published'] = additional_information.xpath('//div[@itemprop="datePublished"]/text()').extract()[0]
				item['file_size'] = additional_information.xpath('//div[@itemprop="fileSize"]/text()').extract()[0]
				item['num_downloads'] = additional_information.xpath('//div[@itemprop="numDownloads"]/text()').extract()[0]
				item['software_version'] = additional_information.xpath('//div[@itemprop="softwareVersion"]/text()').extract()[0]
				item['operating_systems'] = additional_information.xpath('//div[@itemprop="operatingSystems"]/text()').extract()[0]

				yield item
		except ValueError:
			log.msg('Not a free app: ' + response.url, log.INFO)