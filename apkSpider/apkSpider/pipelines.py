# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
#import pymongo
from scrapy.exceptions import DropItem
from scrapy.http import Request

#1.Verify the validity of the data.Such as whether already exists
class VerifyPipeline(object):
    """Verify the validity"""
    def __init__(self):
        pass

    def process_item(self, item, spider):
        """Usage 
        if spider.name not in ['myspider1', 'myspider2', 'myspider3']:
        if isinstance(item, FeedItem):
        """
        vaild=True
        for data in item:
            if not data:
                vaild=False
                raise DropItem("Missing %s of data from %s" %(data,item['name']))
        if vaild:
            pass
        return item


#2.download images

#3.store the data to MongoDB
# class StoreDataPipeline(object):
#     def __init__(self):
#         connection=pymongo.Connection('localhost',27017)
#         db=connection['test']
#         self.collection=db['scrapy']

#     def process_item(self, item, spider):
#         vaild=True
#         for data in item:
#             if not data:
#                 vaild=False
#                 raise DropItem("Missing %s of data from %s" %(data,item['name']))
#         if vaild:
#             self.collection.insert(dict(item))
#         return item