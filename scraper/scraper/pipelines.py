from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import sqlite3

class SQLiteStorePipeline(object):
	filename = 'data.sqlite'

	def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
		try:
            self.conn.execute('')
        except:
            log.msg('Failed to insert item: ' + item['url'], level=log.ERROR)
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            log.mst('File does not exist: ' + self.filename, level=log.ERROR)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None