#! /usr/bin/env python3
# coding: utf-8
import argparse
import logging as log
import readers.csv as CSVReader
from spiders.paruvendu import PVSpider
import api_readers.simple_api_request as ApiRequest
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import datetime
from os import path, name

# import analysis.xml as XMLAnalysis

# File selection arguments
def parseArgument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="""File path : """)
    return parser.parse_args()

def saveJsonToFile(jsonData):
    # format the datafile name 
    datafileName = 'data_{}.json'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    # determine path of the file 
    directory = path.dirname(path.dirname(__file__))
    pathToFile = path.join(directory, 'itowa/datas', datafileName)
    print(pathToFile)
    # Write json into datafile
    with open(pathToFile, 'w') as outfile:
        json.dump(jsonData, outfile)

if __name__ == "__main__":
    log.basicConfig(level=log.INFO)
    # Get user answers 
    args = parseArgument()
    # TODO: get extension from file
    args.extension = 'csv'

    try:
        # Get the file from args
        dataFile = args.file

        
        # No file selected
        if dataFile == None:
            log.error('You must select a file !')
        else:
            try:
                if args.extension == 'xml':
                    # To implement 
                    # XMLAnalysis.launchAnalysis(args.datafile)
                    log.warning('Functionnality to implement')
                elif args.extension == 'csv':
                    
                    log.info('#### ANALYSIS BEGIN ####')
                    # Read CSV and scrap over the web
                    animalList = CSVReader.getAnimalList(dataFile)

                    ### Top Annonce
                    topAnnonceReader = ApiRequest.simpleAPIRequest()
                    topAnnonceReader.animalList = animalList
                    topAnnonceReader.apiName = 'topannonces'
                    topAnnonceReader.urlTemplate = 'https://api.topannonces.fr/liste?c=A0000000&nbParPage=12&{}'
                    topAnnonceReader.launchAnalysis()
                    if len(topAnnonceReader.finalJSON) > 0:
                        saveJsonToFile(topAnnonceReader.finalJSON)

                    ### Paru Vendu         
                    PVSpider.animalList = animalList
                    process = CrawlerProcess(settings={ 'DOWNLOAD_DELAY' : 1 })
                    process.crawl(PVSpider)
                    process.start()
                    if len(PVSpider.finalJSON) > 0:
                        saveJsonToFile(PVSpider.finalJSON)


            except FileNotFoundError as e: 
                log.error('File not found')
            finally:
                log.info('#### ANALYSIS OVER ####')
    except Warning as e:
        log.warning(e)