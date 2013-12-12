# coding:utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawl_cic.items import FamilydoctorItem

Keyword = u'早泄'

class DmozSpider(BaseSpider):
    name = "familydoctor"
    allowed_domains = ["so.familydoctor.com.cn"]
    start_urls = [
        "http://%s%s" % (allowed_domains[0], "/kedafu.aspx?keyword=%u65E9%u6CC4"),
    ]

    def parse(self, response):
#         filename = response.url.split("/")[-2]
#         open(filename, 'wb').write(response.body)
        requests = []
        hxs = HtmlXPathSelector(response)
        aims = hxs.select('//div[@class="colMain"]/div[@class="kedafu"]')
        posts = aims.select('ul/li/h3/a/@href').extract()
        requests.extend([self.make_requests_from_url(url).replace(callback=self.parse_item)
                  for url in posts])
        
        nexts = aims.select('div[@class="endPage"]/a[@class="next"]/@href').extract()
        for url in nexts:
            requests.append(self.make_requests_from_url('http://%s%s' % (self.allowed_domains[0], url)))
        return requests

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        aim = hxs.select('//div[@class="contain"]/div[@class="colMain"]/div[@class="module mQuestion"]/div[@class="moduleContent"]')
        ws = aim.select('div[@class="questionTitle"]/h1/span[@id="lbSubject"]/a/text()').extract()
        title = get_title(ws)
        desc = ''.join(aim.select('p[@itemprop="content"]/text()').extract()).strip()
        replys = hxs.select('//div[@class="replyText"]/pre/text()').extract()
        
        item = FamilydoctorItem()
        item['url'] = response.url
        item['title'] = title.replace("\n", "")
        item['desc'] = desc.replace("\n", "")
        item['replys'] = replys
        yield item
        
def get_title(words):
    if len(words) < 2: 
        words.insert(0, '')
    title = Keyword.join(words).strip()    
    return title

