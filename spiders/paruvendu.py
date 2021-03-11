import scrapy
import urllib
from scrapy.crawler import CrawlerProcess
import readers.csv as CSVReader
import json

class PVSpider(scrapy.Spider):
    name = "pvs"
    domain = "https://www.paruvendu.fr/animmos/listefo/default/default?rfam=&elargrayon=1&ray=50&idtag=&lo=France&codeINSEE=&lo=&pa=&chaine=A&ray=50&rechliste=1&raceChien=Race+du+chien&idTagRaceChien=&raceChat=Race+du+chat&idTagRaceChat=&zmd%5B%5D=VENTE&typeAnnonceur=&px0=&px1=&flagLof=&flagSexe=&moins8Sem=&filtre=&tri=&{}"
    animalList = []
    finalJSON = []
   
    def __init__(self):
        pass

    def start_requests(self):
        # Loop into animal list
        for animal in self.animalList:
            tmpURL = self.domain.format(urllib.parse.urlencode({'fulltext' : animal[0]}))
            yield scrapy.Request(url=tmpURL, callback = self.parse)

    def parse(self, response):
        for annonce in response.css('div.ergov3-annonce'):
            data = {
                'title' : annonce.css(".ergov3-txtannonce h3:first-child::text").extract_first().strip(),
                'commune' : annonce.css(".ergov3-txtannonce h3:last-child::text").extract_first().strip(),
                'link' : annonce.css('.ergov3-voirann a::attr(href)').extract_first().strip()
            }
        
            self.finalJSON.append(data) 
        