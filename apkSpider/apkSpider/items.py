# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ApkItem(Item):
    # define the fields for your item here like:
    name = Field()
    packageName = Field() #Unique
    company = Field()
    genre = Field()
    #rate
    rate = Field()
    votes = Field()
    #about
    datePublished = Field()
    currentVersion = Field()
    os = Field()
    category = Field()
    numDownloads = Field()
    fileSize = Field()
    price = Field()
    #image
    apkicon = Field()
    apkiconPath = Field()
    bannerimage = Field()
    bannerimagePath = Field()
    screenshot = Field()
    screenshotPath = Field()
    #video
    video = Field()
    #description
    description = Field()
    #whatsnew
    whatsnew = Field()
    #other
    tags = Field()
    downloadUrl = Field()
    apkPath = Field()
    comefrom = Field()
    file_urls = Field()
    files = Field()

class TopApkItem(Item):
    topType = Field()
    ranking = Field()
    packageName = Field()
    recordTime = Field()