from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scraper.items import AppCategoryItem,AppItem

class AppSpider(CrawlSpider):
    
   name = "app"
   allowed_domains = ["play.google.com"]
   start_urls = [
       "https://play.google.com/store/apps"
   ]
   
   rules = (

        Rule(SgmlLinkExtractor(allow=('/store/apps$', )), callback='parseCategoryGroup',follow=True),
        Rule(SgmlLinkExtractor(allow=('/store/apps/category/.*', )), callback='parseCategory',follow=True),
        Rule(SgmlLinkExtractor(allow=('/store/search\?.*', )), callback='parseSearch',follow=True),
    )

   def parseCategoryGroup(self, response):
       
       hxs = HtmlXPathSelector(response)
       categoryGroups = hxs.select('//div[@class="padded-content3 app-home-nav"]')

       for categoryGroup in categoryGroups:
           
           categoryGroupName = categoryGroup.select('h2/a/text()').extract()

           categories = categoryGroup.select('ul/li')
           for category in categories:
               categoryName = category.select('a/text()').extract()
               categoryURL = category.select('a/@href').extract()[0]
               print categoryName,categoryURL
               
       import string
       chars = string.ascii_uppercase + string.digits
       for x in chars :
           yield Request('https://play.google.com/store/search?q='+x+'&c=apps',callback=self.parseSearch)
           
       for x in chars :
           for y in chars :
               yield Request('https://play.google.com/store/search?q='+x+y+'&c=apps',callback=self.parseSearch)
               
       for x in chars :
           for y in chars :
               for z in chars :
                   yield Request('https://play.google.com/store/search?q='+x+y+z+'&c=apps',callback=self.parseSearch)        
       return
   
   def parseCategory(self,response):
       
       basePath = response.url.split('?')[0]   
       
       if '/collection/' in response.url:
           print response.url
           hxs = HtmlXPathSelector(response)
           apps = hxs.select('//a[@class="title"]')
           hasApp = False
           for app in apps:
               hasApp = True
               appName = app.select('text()').extract()
               appURL = app.select('@href').extract()
               print appName,appURL
               yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
            
                 
           if hasApp :
                import re
                m = re.match(r'(.*)\?start=(\d+)&num=24',response.url)
                if m is None :
                    startNumber = 24                  
                else:
                    startNumber = int(m.group(2))+24
                    print m.group()
                print startNumber
                yield Request(basePath+'?start='+str(startNumber)+'&num=24',callback=self.parseCategory)

       return
   
   def parseSearch(self,response):
       print 'parse search ----'
       import re
       m = re.match(r'(.*)&start=(\d+)&num=24',response.url)
       if m is None :
           basePath = response.url
           startNumber = 24                  
       else:
           startNumber = int(m.group(2))+24
           basePath = m.group(1)
       
       hxs = HtmlXPathSelector(response)
       apps = hxs.select('//a[contains(@href,"/store/apps/details")]')
       hasApp = False
       for app in apps:
           hasApp = True
           appURL = app.select('@href').extract()
           yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
            
       if hasApp :
           print 'next search -----'
           yield Request(basePath+'&start='+str(startNumber)+'&num=24',callback=self.parseSearch)

       return
   
   def parseApp(self,response):

       hxs = HtmlXPathSelector(response)
 
       apps = hxs.select('//a[@class="common-snippet-title"]')
       for app in apps:
           appURL = app.select('@href').extract()
           yield Request('https://play.google.com'+appURL[0] ,callback=self.parseApp)
            
       screens = hxs.select('//div[@class="screenshot-carousel-content-container"]/img')
       screenShots=''
       for screen in screens:
           screenShots = screenShots + screen.select('@src').extract()[0] + ';'
       
       item = AppItem()
       item['screenShots'] = screenShots
       metadata = hxs.select('//dl[@class="doc-metadata-list"]')
       item['name'] = metadata.select('meta[@itemprop="name"]/@content').extract()
       item['author'] = metadata.select('span[@itemprop="author"]/meta[@itemprop="name"]/@content').extract()
       item['image'] = metadata.select('meta[@itemprop="image"]/@content').extract()
       item['rating'] = metadata.select('//div[@class="ratings goog-inline-block"]/@content').extract()
       item['votes'] = metadata.select('//span[@itemprop="ratingCount"]/@content').extract()
       item['contentRating'] = metadata.select('//dd[@itemprop="contentRating"]/text()').extract()
       item['price'] = metadata.select('//meta[@itemprop="price"]/@content').extract()
       item['fileSize'] =  metadata.select('//dd[@itemprop="fileSize"]/text()').extract()
       item['downloads'] =  metadata.select('//dd[@itemprop="numDownloads"]/text()').extract()
       item['datePublished'] = metadata.select('//time[@itemprop="datePublished"]/text()').extract()
       item['version'] = metadata.select('//dd[@itemprop="softwareVersion"]/text()').extract()
       item['description'] = hxs.select('//div[@id="doc-original-text"]').extract()
       item['category'] = metadata.select('//a[contains(@href,"category")]/text()').extract()
       item['package'] = hxs.select('//a[@class="buy-link buy-button goog-inline-block buy-alternate-offer-default"]/@data-docid').extract()
       
       yield item
