from scrapy import log
from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher
from scraper.items import ApkItem
from os import path
import sqlite3

class SQLiteStorePipeline(object):
    filename = 'Evolution of Android Applications.sqlite'
    
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    # Tries to insert the APK file's information into the database.
    # If an error occurs or the APK file is a duplicate, the APK file 
    # is not downloaded and the APK file's information is not inserted 
    # into the database.
    def process_item(self, item, spider):
        try:
            self.conn.execute('INSERT INTO ApkInformation (Name, Version, Rating, DatePublished, FileSize, NumberOfDownloads, URL, Genre, OSSupported) VALUES(?,?,?,?,?,?,?,?,?)', (item['name'], item['software_version'],item['score'], item['date_published'], item['file_size'], item['num_downloads'], item['url'], item['genre'], item['operating_systems']))
            return item
        except:
            log.msg('Failed to insert item: ' + item['url'], level=log.ERROR)
            raise DropItem(item['url'])

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