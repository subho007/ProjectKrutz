from scrapy import log
from scrapy import signals
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

    def process_item(self, item, spider):
        if isinstance(item, ApkItem):
            try:
                self.conn.execute('''INSERT INTO ApkInformation (Name, Developer, Version, URL, Rating, Genre, DatePublished, NumberOfDownloads, OSSupported, FileSize) VALUES(?,?,?,?,?,?,?,?,?,?)''' , (item['name'], item['developer'], item['software_version'], item['download_url'], item['score'], item['genre'], item['date_published'], item['num_downloads'], item['operating_systems'], item['file_size']));
            except:
                log.msg('Failed to insert item: ' + item['name'], level=log.ERROR)
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