import scrapy
import urllib
from scrapy.crawler import CrawlerProcess

class LBCSpider(scrapy.Spider):
    name = "lbc"
    domain = "https://www.leboncoin.fr/recherche?category=75&{}"
    animalList = [['chat']]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
   
    def __init__(self):
        pass

    def start_requests(self):
        fakeHeaders = {'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'}

        for animal in self.animalList:
            tmpURL = self.domain.format(urllib.parse.urlencode({'text' : animal[0]}))
            yield scrapy.Request(url=tmpURL, headers=fakeHeaders, callback = self.parse)

    def parse(self, response):
        print("hellooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo current user-agent:{}".format(response.request.headers['User-Agent']))
        title = response.css("span#productTitle::text").extract_first().strip()
        link = response.css('a.aditem_container::href').extract_first().strip()

        print(title)
        print(link)

        # data = {"link":link,"title":title,}
        # import pdb; pdb.set_trace()
        # with open('data.json', 'w') as outfile:
        #     json.dump(data, outfile)

process = CrawlerProcess(settings={
    "FEEDS": {
        "data.json": {"format": "json"},
    },
})

process.crawl(LBCSpider)
process.start()