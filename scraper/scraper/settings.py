BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

ITEM_PIPELINES = {
	'scraper.pipelines.SQLiteStorePipeline' : 300,
	'scraper.pipelines.APKFilesPipeline' : 800,
}

FILES_STORE = './downloads'

DOWNLOAD_DELAY = 0.25

COOKIES_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'APK File Scraper (+https://github.com/amb8805/ProjectKrutz)'