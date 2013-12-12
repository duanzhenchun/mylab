# Scrapy settings for crawl_cic project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
LOG_LEVEL = 'WARNING'

BOT_NAME = 'crawl_cic'

SPIDER_MODULES = ['crawl_cic.spiders']
NEWSPIDER_MODULE = 'crawl_cic.spiders'

ITEM_PIPELINES = ['crawl_cic.pipelines.XlsPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_cic (+http://www.yourdomain.com)'
