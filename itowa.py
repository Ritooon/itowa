#! /usr/bin/env python3
# coding: utf-8
import argparse
import logging as log
import readers.csv as CSVReader
import spiders.lbc as LBCAnalysis
# import analysis.xml as XMLAnalysis

# File selection arguments
def parseArgument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="""File path : """)
    return parser.parse_args()

if __name__ == "__main__":
    # log.basicConfig(level=log.INFO)
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
                    # lbcSpider.animalList =animalList
                    lbcSpider = LBCAnalysis.LBCSpider()

                    # for request in lbcSpider.start_requests():
                    #     print(request)

            except FileNotFoundError as e: 
                log.error('File not found')
            finally:
                log.info('#### ANALYSIS OVER ####')
    except Warning as e:
        log.warning(e)