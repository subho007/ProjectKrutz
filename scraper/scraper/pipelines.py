from scrapy import log
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
from scraper.items import ApkItem, ApkDownloadItem
from os import path
import sqlite3

class SQLiteStorePipeline(object):
    filename = 'Evolution of Android Applications.sqlite'
    
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        if isinstance(item, ApkItem):
            try:
                self.conn.execute('INSERT INTO ApkInformation (Name, Version, Rating, DatePublished, FileSize, NumberOfDownloads, URL, Genre, OSSupported) VALUES(?,?,?,?,?,?,?,?,?)' , (item['name'], item['software_version'],item['score'], item['date_published'], item['file_size'], item['num_downloads'], item['come_from'], item['genre'], item['operating_systems']))
            except:
                log.msg('Failed to insert item: ' + item['name'], level=log.ERROR)
            return item
        elif isinstance(item, ApkDownloadItem):
            try:
                cursor = self.conn.execute('SELECT * FROM ApkInformation WHERE URL=\"' + item['come_from'] + '\"')
                if len(cursor.description) > 0:
                    raise DropItem('Duplicate item found: ' + item['come_from'])
            except:
                log.msg('Duplicate may exist: ' + item['come_from'], level=log.WARNING)
                return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            log.msg('File does not exist: ' + self.filename, level=log.ERROR)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None