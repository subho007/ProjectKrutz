# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScraperItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class AppCategoryItem(Item):
    name = Field()
    url = Field()
    
class AppItem(Item):
    name = Field()
    screenShots = Field()
    description = Field()
    downloads = Field()
    rating = Field()
    votes = Field()
    image = Field()
    price = Field()
    category = Field()
    author = Field()
    contentRating = Field()
    fileSize = Field()
    version = Field()
    datePublished = Field()
    package = Field()
